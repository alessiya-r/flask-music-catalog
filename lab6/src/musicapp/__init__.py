"""Музыкальный каталог: создание и настройка Web-приложения.

Модуль задаёт параметры инициализации, связывает сервлеты с URL-адресами и
определяет защищаемые ресурсы и роли, которым они доступны.
"""

from flask import Flask, g, render_template

from .security import load_users, requires_role
from .servlets import SongsList, catalog, get_language, load_messages


def create_app():
    """Создаёт и настраивает приложение."""
    app = Flask(__name__)

    # Параметр инициализации (аналог <init-param> в web.xml)
    app.config["MAX_SONGS"] = 5

    # Регистрация сервлета
    app.add_url_rule(
        "/SongsList",
        view_func=SongsList.as_view("SongsList"),
    )

    # Защищаемый ресурс: страница каталога доступна ролям user и admin
    app.add_url_rule(
        "/catalog",
        view_func=requires_role("user", "admin")(catalog),
    )

    @app.route("/")
    def index():
        """Главная HTML-страница с формой выбора жанра и языка."""
        lang = get_language()
        return render_template("index.html", lang=lang, m=load_messages(lang))

    @app.route("/admin")
    @requires_role("admin")
    def admin_page():
        """Служебная страница со списком пользователей.

        Защищаемый ресурс, доступный только роли admin.
        """
        return render_template(
            "admin.html",
            users=load_users(),
            username=g.user["username"],
        )

    @app.errorhandler(404)
    def page_not_found(error):
        """Обработка обращения к несуществующему адресу."""
        return render_template(
            "error_manager.html",
            message="Страница не найдена. Проверьте адрес.",
        ), 404

    return app
