"""Передача данных между запросами: файлы Cookie и переменные сессии"""

from datetime import datetime

from flask import (
    make_response, redirect, render_template, request, session, url_for,
)

# Время жизни Cookie в секундах
COOKIE_MAX_AGE = 7 * 24 * 3600      # неделя

# Доступные цвета страницы вывода
COLORS = {
    "lime": "лаймовый",
    "violet": "сиреневый",
    "orange": "оранжевый",
    "white": "белый",
}

DEFAULT_COLOR = "lime"


def prefs_form():
    """Страница запроса имени пользователя и цвета 

    Если значения уже сохранены в Cookie, они подставляются в форму
    """
    return render_template(
        "prefs_form.html",
        name=request.cookies.get("user_name", ""),
        color=request.cookies.get("page_color", DEFAULT_COLOR),
        colors=COLORS,
        message=request.args.get("message", ""),
    )


def prefs_save():
    """Обработка формы

    Проверяет имя пользователя, сохраняет имя и цвет в Cookie,
    увеличивает счётчик обращений и запоминает дату последнего
    обращения в переменных сессии, после чего передаёт управление
    странице вывода.
    """
    name = request.args.get("name", "").strip()
    color = request.args.get("color", DEFAULT_COLOR)

    # сообщение об ошибке, если имя не задано
    if not name:
        return redirect(url_for("prefs_form", message="Не задано имя пользователя"))

    if color not in COLORS:
        color = DEFAULT_COLOR

    # переменные сессии: количество обращений и дата последнего обращения
    session["visits"] = session.get("visits", 0) + 1
    session["last_visit"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    # передача управления странице вывода (аналог sendRedirect)
    response = make_response(redirect(url_for("prefs_result")))

    # сохранение значений в Cookie (аналог addCookie с setMaxAge)
    response.set_cookie("user_name", name, max_age=COOKIE_MAX_AGE)
    response.set_cookie("page_color", color, max_age=COOKIE_MAX_AGE)

    return response


def prefs_result():
    """Страница вывода

    Отображает значения, прочитанные из Cookie и из переменных
    сессии, в цвете, выбранном пользователем.
    """
    color = request.cookies.get("page_color", DEFAULT_COLOR)

    return render_template(
        "prefs_result.html",
        name=request.cookies.get("user_name", ""),
        color=color,
        color_name=COLORS.get(color, color),
        visits=session.get("visits", 0),
        last_visit=session.get("last_visit", "не зафиксирована"),
    )
