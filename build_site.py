import csv
from csv import DictReader
from dataclasses import asdict
import os
from models import Game
# 1. считать csv с данными об играх
# 2. в цикле перебрать строки из файла и дополнить их
# html тегами
# <tr><td>/game/acro_fs</td>...
# 3. открыть шаблон страницы template.html
# 4. вставить туда новый html код
# 5. сохранить html файл catalogue.html

def read_csv_data() -> list[Game]:
    games = []
    with open("out/games.csv", "r", encoding="utf-8") as f:
        reader = DictReader(f, )
        for row in reader:
            games.append(Game(**row))
    return games

def build_row(game: Game) -> str:
    row = asdict(game)
    tds = ""
    for cell in row.values():
        tds += f"<td>{cell}</td>"
    print(tds)
    tr = f"<tr>{tds}</tr>"
    return tr

def main():
    data = read_csv_data()
    rows = []
    for game in data:
        row = build_row(game)
        rows.append(row)
    html = "\n".join(rows)
    with open("site/template.html", "r", encoding="utf-8") as f:
        html_template = f.read()
    html_out = html_template.replace("{{DATA}}", html)
    with open("site/catalogue.html", "w", encoding="utf-8") as f:
        f.write(html_out)


if __name__ == "__main__":
    main()


