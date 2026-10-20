# Музыкальный каталог на Flask

Лабораторные работы по веб-программированию (СПбГЭТУ «ЛЭТИ»).

Методические указания написаны для Java (Maven, сервлеты, JSP, Apache Tomcat),
работы выполнены на Python с использованием фреймворка Flask. Соответствие средств:

| Java | Python |
|---|---|
| Apache Tomcat | сервер разработки Flask, gunicorn |
| Maven, `pom.xml` | setuptools, `pyproject.toml` |
| `.war` | `.whl` |
| Сервлет, `doGet()` | класс `MethodView`, метод `get()` |
| `web.xml` | функция `create_app()` |
| `ResourceBundle`, `.properties` | функция `load_messages()`, файлы `.json` |
| JSP | шаблоны Jinja2 |
| `tomcat-users.xml`, `security-constraint` | `users.json`, декоратор `requires_role` |
| `keytool` | `openssl` |
| Javadoc | pydoc |

## Состав

| Папка | Работа |
|---|---|
| `lab1` | Настройка среды разработки, запуск сервера, порты |
| `lab2` | Сборка проекта в дистрибутив и размещение на сервере |
| `lab3` | Обработка запросов: параметры инициализации и динамические параметры |
| `lab4` | Интернационализация: файлы ресурсов для русского и английского языков |
| `lab5` | Построение интерфейса на шаблонах: включение страниц, макросы, страница ошибок |
| `lab6` | Аутентификация и авторизация пользователей, HTTPS с самоподписанным сертификатом |

## Запуск (на примере lab6)

```bash
cd lab6
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
flask --app musicapp run --port 8080 --debug
```

Приложение открывается по адресу `http://127.0.0.1:8080/catalog`.
Учётные записи для входа заданы в `src/musicapp/users.json`.

Запуск по HTTPS требует сертификата, который создаётся командой:

```bash
mkdir -p conf
openssl req -x509 -newkey rsa:2048 -nodes -days 365 \
  -keyout conf/mystore.key -out conf/mystore.crt \
  -subj "/CN=localhost/OU=LETI/O=LETI/L=Saint-Petersburg/ST=Saint-Petersburg/C=RU"

flask --app musicapp run --port 8443 --cert conf/mystore.crt --key conf/mystore.key
```

Учебный проект: сервер разработки и самоподписанный сертификат
для реальной эксплуатации не предназначены.
