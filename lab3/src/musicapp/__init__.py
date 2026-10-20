"""Музыкальный каталог: создание и настройка Web-приложения"""

from flask import Flask, render_template
from .servlets import SongsList


def create_app():
    """Создаёт и настраивает приложение."""
    app = Flask(__name__)

    # Параметры инициализации сервлета
    app.config["CATALOG_NAME"] = "Музыкальный каталог"
    app.config["MAX_SONGS"] = 5

    # Регистрация сервлета: имя, класс и URL-адрес
    app.add_url_rule(
        "/SongsList",                               # url-pattern
        view_func=SongsList.as_view("SongsList"),   # servlet-name и servlet-class
    )

    @app.route("/")
    def index():
        """Главная HTML-страница с формой выбора жанра"""
        return render_template("index.html", catalog_name=app.config["CATALOG_NAME"])

    return app
