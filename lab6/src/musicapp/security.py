"""Аутентификация и авторизация пользователей.

Модуль заменяет настройки безопасности сервера Apache Tomcat:
файл users.json соответствует tomcat-users.xml, а декоратор
requires_role - секции security-constraint в файле web.xml.
"""

import json
from functools import wraps
from pathlib import Path

from flask import Response, g, render_template, request
from werkzeug.security import check_password_hash

# Файл с пользователями, паролями и ролями (аналог tomcat-users.xml)
USERS_FILE = Path(__file__).parent / "users.json"

# Контекст аутентификации, отображаемый в окне входа (аналог realm-name)
REALM = "Music Catalog"


def load_users():
    """Читает список пользователей из файла."""
    with open(USERS_FILE, encoding="utf-8") as file:
        return json.load(file)["users"]


def check_user(username, password):
    """Проверяет имя пользователя и пароль.

    Возвращает пользователя, если пароль верен, иначе None.
    Пароли хранятся в виде хеша, поэтому сравниваются не строки,
    а результат хеширования введённого пароля.
    """
    for user in load_users():
        if user["username"] == username:
            if check_password_hash(user["password_hash"], password):
                return user
    return None


def request_auth():
    """Возвращает ответ 401 с требованием базовой аутентификации.

    Получив такой ответ, браузер показывает стандартное окно
    ввода имени пользователя и пароля (аналог auth-method BASIC).
    """
    return Response(
        "Требуется аутентификация",
        401,
        {"WWW-Authenticate": f'Basic realm="{REALM}"'},
    )


def requires_role(*roles):
    """Защищает ресурс и разрешает доступ только указанным ролям.

    Аналог секции security-constraint в файле web.xml: задаёт
    защищаемый ресурс и список ролей, которым он доступен.
    """
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            auth = request.authorization

            # имя и пароль не переданы - запрашиваем аутентификацию
            if auth is None:
                return request_auth()

            user = check_user(auth.username, auth.password)

            # пароль неверен - запрашиваем аутентификацию повторно
            if user is None:
                return request_auth()

            # пользователь известен, но роль не подходит - доступ запрещён
            if not set(roles) & set(user["roles"]):
                return render_template(
                    "forbidden.html",
                    username=user["username"],
                ), 403

            g.user = user
            return view(*args, **kwargs)

        return wrapper
    return decorator
