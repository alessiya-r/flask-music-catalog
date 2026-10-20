"""Музыкальный каталог: создание и настройка Web-приложения.

Модуль выполняет роль дескриптора развёртывания web.xml:
задаёт параметры инициализации и связывает сервлеты с URL-адресами.
"""

from flask import Flask, render_template

from .servlets import SongsList, get_language, load_messages


def create_app():
    """Создаёт и настраивает приложение."""
    app = Flask(__name__)

    # Параметр инициализации (аналог <init-param> в web.xml)
    app.config["MAX_SONGS"] = 5

    # Регистрация сервлета: имя, класс и URL-адрес
    # (аналог секций <servlet> и <servlet-mapping> в web.xml)
    app.add_url_rule(
        "/SongsList",
        view_func=SongsList.as_view("SongsList"),
    )

    @app.route("/")
    def index():
        """Главная HTML-страница с формой выбора жанра и языка."""
        lang = get_language()
        return render_template("index.html", lang=lang, m=load_messages(lang))

    return app
