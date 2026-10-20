"""Сервлеты музыкального каталога с поддержкой нескольких языков."""

import json
from pathlib import Path

from flask import current_app, render_template, request
from flask.views import MethodView

# Каталог файлов ресурсов (аналог каталога ресурсов Java-проекта)
RESOURCES_DIR = Path(__file__).parent / "resources"

# Поддерживаемые языки интерфейса
LANGUAGES = ["ru", "en"]
DEFAULT_LANGUAGE = "ru"


# Данные предметной области: список музыкальных композиций
SONGS = [
    {"title": "Bohemian Rhapsody", "artist": "Queen", "genre": "rock", "year": 1975},
    {"title": "Smells Like Teen Spirit", "artist": "Nirvana", "genre": "rock", "year": 1991},
    {"title": "Billie Jean", "artist": "Michael Jackson", "genre": "pop", "year": 1982},
    {"title": "Blinding Lights", "artist": "The Weeknd", "genre": "pop", "year": 2019},
    {"title": "Take Five", "artist": "Dave Brubeck", "genre": "jazz", "year": 1959},
    {"title": "So What", "artist": "Miles Davis", "genre": "jazz", "year": 1959},
]


def get_language():
    """Возвращает код языка интерфейса из динамического параметра lang."""
    lang = request.args.get("lang", DEFAULT_LANGUAGE)
    if lang not in LANGUAGES:
        lang = DEFAULT_LANGUAGE
    return lang


def load_messages(lang):
    """Загружает надписи интерфейса для указанного языка.

    Аналог класса ResourceBundle в Java: читает файл ресурсов
    messages_<язык>.json и возвращает набор пар "ключ - надпись".
    """
    path = RESOURCES_DIR / f"messages_{lang}.json"
    with open(path, encoding="utf-8") as file:
        return json.load(file)


class SongsList(MethodView):
    """Сервлет, выводящий список музыкальных композиций.

    Обрабатывает запросы по адресу /SongsList. Принимает параметр
    инициализации MAX_SONGS и динамические параметры genre (жанр)
    и lang (язык интерфейса).
    """

    def get(self):
        """Обработчик GET-запроса (аналог метода doGet).

        Определяет язык интерфейса, загружает соответствующий файл
        ресурсов, отбирает композиции по жанру и возвращает страницу.
        """
        lang = get_language()                  # динамический параметр lang
        messages = load_messages(lang)         # надписи выбранного языка

        genre = request.args.get("genre", "")  # динамический параметр genre
        max_songs = current_app.config["MAX_SONGS"]   # параметр инициализации

        if genre:
            songs = [song for song in SONGS if song["genre"] == genre]
        else:
            songs = SONGS
        songs = songs[:max_songs]

        return render_template(
            "songs.html",
            songs=songs,
            genre=genre,
            lang=lang,
            m=messages,
        )
