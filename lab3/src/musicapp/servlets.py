"""Сервлеты музыкального каталога"""

from flask import current_app, render_template, request
from flask.views import MethodView


# Данные предметной области: список музыкальных композиций
SONGS = [
    {"title": "Bohemian Rhapsody", "artist": "Queen", "genre": "rock", "year": 1975},
    {"title": "Smells Like Teen Spirit", "artist": "Nirvana", "genre": "rock", "year": 1991},
    {"title": "Billie Jean", "artist": "Michael Jackson", "genre": "pop", "year": 1982},
    {"title": "Blinding Lights", "artist": "The Weeknd", "genre": "pop", "year": 2019},
    {"title": "Take Five", "artist": "Dave Brubeck", "genre": "jazz", "year": 1959},
    {"title": "So What", "artist": "Miles Davis", "genre": "jazz", "year": 1959},
]


class SongsList(MethodView):
    """Сервлет, выводящий список музыкальных композиций"""

    def get(self):
        """Обработчик GET-запроса

        Читает динамический параметр genre, отбирает композиции
        указанного жанра и возвращает HTML-страницу со списком
        """
        # динамический параметр из строки запроса: /SongsList?genre=rock
        genre = request.args.get("genre", "")

        # параметры инициализации
        catalog_name = current_app.config["CATALOG_NAME"]
        max_songs = current_app.config["MAX_SONGS"]

        # отбор композиций по жанру
        if genre:
            songs = [song for song in SONGS if song["genre"] == genre]
        else:
            songs = SONGS

        # ограничение количества по параметру инициализации
        songs = songs[:max_songs]

        return render_template(
            "songs.html",
            songs=songs,
            genre=genre,
            catalog_name=catalog_name,
        )

    # flask --app musicapp run --port 8080 --debug
    #source .venv/bin/acstivate
