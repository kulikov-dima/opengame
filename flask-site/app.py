from flask import Flask, render_template
from csv import DictReader

app = Flask(__name__)

def read_csv_data() -> list[dict]:
    with open("out/games.csv", "r", encoding="utf-8") as f:
        reader = DictReader(f)
        return list(reader)

@app.route("/")
def index():
    games = read_csv_data()
    return render_template("template.html", games=games)


if __name__ == "__main__":
    app.run(debug=True)
