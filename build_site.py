import csv
import os
from main import OUT_DIR
SITE_DIR = "site"
TEMPLATE = os.path.join(SITE_DIR,"template.html")
OUTPUT = os.path.join(SITE_DIR,"catalog.html")


def load_games(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def make_row(game: dict):
    cells = game.values()
    tds = "".join(f"<td>{c}</td>" for c in cells)
    return f"<tr>{tds}</tr>"


def main():

    games = load_games(os.path.join(OUT_DIR, "games.csv"))

    rows = "\n".join(make_row(g) for g in games)

    with open(TEMPLATE, encoding="utf-8") as f:
        page = f.read()
    page = page.replace("{{ROWS}}", rows)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Готово: {len(games)} игр -> {OUTPUT}")


if __name__ == "__main__":
    main()