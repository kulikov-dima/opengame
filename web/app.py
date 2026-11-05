from flask import Flask, request, render_template
import os
import csv
import json
from client import StopGameClient
from reference import update_platforms, update_genres
from dataclasses import asdict
from models import Tag, Game, Platform

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "games.csv")
FILEDNAMES = [
    "Ссылка",
    "Название",
    "Дата выхода",
    "Рейтинг"
]

client = StopGameClient()
TAGS = client.fetch_tags()
PLATFORMS = client.fetch_platforms()

app = Flask(__name__)

@app.route("/")
def table():

    
    games = get_games()
    print(json.dumps(PLATFORMS , indent=4, ensure_ascii=False))
    return render_template("table.html", games=games, active="table", tags=TAGS, platforms=PLATFORMS)

def get_games() -> list[dict]:
    with open(CSV_FILE, "r", encoding="utf-8", newline='') as file:
        reader = csv.DictReader(file, FILEDNAMES)
        g = []
        
        for i, row in enumerate(reader):
            print(row)
            if not i:
                continue
            t = {}
            t["url"] = row["Ссылка"]
            t["name"] = row["Название"]
            t["date"] = row["Дата выхода"]
            t["rating"] = row["Рейтинг"]
            try:
                t["genres"] = row["Жанры"]
            except KeyError:
                t["genres"] = row[None][0]
            try:
                t["platforms"] = row["Платформы"]
            except KeyError:
                t["platforms"] = row[None][1]
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


    games = get_games()
    for i in range(len(games)):
        games[i]["genres"] = [Tag(*genre) for genre in decode_string(games[i]["genres"])]
        games[i]["platforms"] = [Platform(*genre) for genre in decode_string(games[i]["platforms"])]


    for i in range(len(games)):
        if i+1 == id:
            game = games[i]
            break
    return render_template("game.html", game=game)

@app.route("/redirect/<path:url>")
def redirect(url):
    return app.redirect(f"https://stopgame.ru/{url}")


def decode_string(string: str) -> tuple[str, str]:  
    datas = string.split(" ")
    result = []
    
    for data in datas:

        parts = string.split('=')

        print(f"\033[1;31m{data=}\033[0m\n")
        code = parts[0]
        name = parts[1].replace("~", " ")
        print(f"\033[1;31m{name=}\n{code=}\033[0m\n")
        result.append((code, name))
    return result