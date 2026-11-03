from flask import Flask, request, render_template
import os
import csv
import json

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "games.csv")
FILEDNAMES = [
    "Ссылка",
    "Название",
    "Дата выхода",
    "Рейтинг"
]
app = Flask(__name__)

@app.route("/")
def table():
    games = get_games()
    return render_template("table.html", games=games, active="table")

def get_games() -> list[dict]:
    with open(CSV_FILE, "r", encoding="utf-8", newline='') as file:
        reader = csv.DictReader(file, FILEDNAMES)
        g = []
        
        for i, row in enumerate(reader):
            if not i:
                continue
            t = {}
            t["url"] = row["Ссылка"]
            t["name"] = row["Название"]
            t["date"] = row["Дата выхода"]
            t["rating"] = row["Рейтинг"]
            g.append(t)
        return g
        
def main(host: str, port: int, threaded: bool, debug: bool):
    app.run(host=host, port=port, threaded=threaded, debug=debug)

@app.route("/about/")
def about():
    return render_template("about.html", active="about")

@app.route("/catalog/")
def catalog():
    return render_template("catalog.html", active="catalog")

@app.route("/index/")
def index():
    return render_template("catalog.html", active="index")

@app.route("/game/<int:id>")
def game(id):
    return render_template("game.html")

@app.route("/redirect/<path:url>")
def redirect(url):
    return app.redirect(f"https://stopgame.ru/{url}")