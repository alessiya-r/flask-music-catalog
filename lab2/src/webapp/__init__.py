from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app





#rm -rf dist                            # (удаляем старую сборку, чтобы собрать заново)
#python -m build                        # (СБОРКА проекта в архив - аналог команды Maven install)
#ls dist                                # (показываем результат: файл .whl — аналог .war)
#unzip -l dist/webapp-0.1.0-py3-none-any.whl   # (состав архива: код, страница, служебная папка)

#deactivate                             # (выключаем окружение проекта)
#cd ../server                           # (переходим в папку сервера — аналог каталога webapps у Tomcat)
#source .venv/bin/activate              # (включаем окружение сервера)
#cp ../lab2/dist/webapp-0.1.0-py3-none-any.whl .    # (копируем архив на сервер)
#pip install --force-reinstall webapp-0.1.0-py3-none-any.whl gunicorn   # (устанавливаем приложение и сервер)
#gunicorn --bind 127.0.0.1:8080 --env SCRIPT_NAME=/webapp "webapp:create_app()"   # (запуск приложения на сервере gunicorn — аналог запуска Tomcat)
