"""Музыкальный каталог: создание и настройка Web-приложения.

Модуль выполняет роль дескриптора развёртывания web.xml:
задаёт параметры инициализации и связывает сервлеты с URL-адресами.
"""

from flask import Flask, render_template

from .servlets import SongsList, catalog, get_language, load_messages


def create_app():
    """Создаёт и настраивает приложение."""
    app = Flask(__name__)

    # Параметр инициализации (аналог <init-param> в web.xml)
    app.config["MAX_SONGS"] = 5

    # Регистрация сервлета из лабораторной работы № 3
    app.add_url_rule(
        "/SongsList",
        view_func=SongsList.as_view("SongsList"),
    )

    # Регистрация страницы каталога (аналог JSP-страницы BookList.jsp)
    app.add_url_rule("/catalog", view_func=catalog)

    @app.route("/")
    def index():
        """Главная HTML-страница с формой выбора жанра и языка."""
        lang = get_language()
        return render_template("index.html", lang=lang, m=load_messages(lang))

    @app.errorhandler(404)
    def page_not_found(error):
        """Обработка обращения к несуществующему адресу.

        Выводит страницу ошибки (аналог ErrorManager.jsp).
        """
        return render_template(
            "error_manager.html",
            message="Страница не найдена. Проверьте адрес.",
        ), 404

    return app
