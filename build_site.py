import csv
from models import Game
import os
from bs4 import BeautifulSoup as bs4

WORKDIR = os.path.dirname(os.path.abspath(__file__))
WORKFILE = os.path.join(WORKDIR, "out", "games.csv")
TEMPLATE = os.path.join(WORKDIR, "site", "template.html")
TAG = "<!--- LABEL: DATA-->"
OUTPUT_FILE = os.path.join(WORKDIR, "site", "out.html")

def read_csv_data() -> list[Game]:
    with open(WORKFILE, 'r', encoding="utf-8") as workfile:
        reader = csv.DictReader(workfile)

        output = []
        for row in reader:
            name = row["Название"]
            url = row["Ссылка"]
            date_of_out = row["Дата выхода"]
            rating = row["Рейтинг"]
            g = Game(url, name, date_of_out, rating)
            output.append(g)
        return output
def add_html(games: list[Game]) -> str:
    out = []
    for game in games:
        out.append("\n")
        out.append("<tr>")
        out.append(f"    <td>{game.url}</td>")
        out.append(f"    <td>{game.name}</td>")
        out.append(f"    <td>{game.year}</td>")
        out.append(f"    <td>{game.rating}</td>")
        out.append("</tr>")
    return "\n".join(out)

def get_html() -> list[str]:
    with open(TEMPLATE, "r", encoding="utf-8") as template:
        html = template.read()

    return html

def mod_html(html: str, replace_html: str, tag: str):
    return html.replace(tag, replace_html)

def main(args = None):
    games = read_csv_data()
    for_add_html = add_html(games)
    html = get_html()

    moded_html = mod_html(html, for_add_html, TAG)
    soup = bs4(moded_html, "html.parser")
    out_html = soup.prettify()
    with open(OUTPUT_FILE, "w+", encoding="utf-8") as f:
        f.write(out_html)


if __name__ == "__main__":
    main()