from flask import Flask
app = Flask(__name__)

@app.route("/")#декоратор
def index():
    return "Hello, World!"




#python3 -m venv .venv - создать виртуальное окружение
#source .venv/bin/acstivate - активация окружения
#cd ~/Desktop/лэти/web-prog/lab1