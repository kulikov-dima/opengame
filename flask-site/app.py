import csv
import os
from flask import Flask, render_template, request, abort

app = Flask(__name__)


def get_games():
    filename = os.path.join(os.path.dirname(__file__), '..', 'out', 'games.csv')
    if not os.path.exists(filename):
        filename = os.path.join(os.path.dirname(__file__), 'games.csv')

    with open(filename, encoding='utf-8', newline='') as f:
        games = list(csv.DictReader(f))

    for i, game in enumerate(games, 1):
        game['id'] = i
        game['platforms'] = game.get('platforms', '').split('~') if game.get('platforms') else []
        game['tags'] = game.get('tags', '').split('~') if game.get('tags') else []
        game['number_year'] = int(game['year'].split()[-1]) if game.get('year') and game['year'].split()[-1].isdigit() else 0
        game['number_rating'] = float(game['rating']) if game.get('rating') else -1

    return games


@app.route('/')
def index():
    games = get_games()
    platforms = sorted({p for game in games for p in game['platforms']})
    genres = sorted({tag for game in games for tag in game['tags']})
    search = request.args.get('search', '')
    platform = request.args.get('platform', '')
    selected_genres = request.args.getlist('genre')
    sort = request.args.get('sort', '')

    if search:
        games = [g for g in games if search.lower() in g['name'].lower()]
    if platform:
        games = [g for g in games if platform in g['platforms']]
    if selected_genres:
        games = [g for g in games if any(tag in g['tags'] for tag in selected_genres)]

    if sort == 'name':
        games = sorted(games, key=lambda g: g['name'].lower())
    elif sort == 'year':
        games = sorted(games, key=lambda g: g['number_year'])
    elif sort == 'rating':
        games = sorted(games, key=lambda g: g['number_rating'], reverse=True)

    return render_template('catalog.html', games=games, platforms=platforms, genres=genres,
                           search=search, platform=platform, selected_genres=selected_genres,
                           sort=sort, active='index')


@app.route('/table')
def table():
    games = get_games()
    platforms = sorted({p for game in games for p in game['platforms']})
    genres = sorted({tag for game in games for tag in game['tags']})
    search = request.args.get('search', '')
    platform = request.args.get('platform', '')
    selected_genres = request.args.getlist('genre')
    sort = request.args.get('sort', '')

    if search:
        games = [g for g in games if search.lower() in g['name'].lower()]
    if platform:
        games = [g for g in games if platform in g['platforms']]
    if selected_genres:
        games = [g for g in games if any(tag in g['tags'] for tag in selected_genres)]

    if sort == 'name':
        games = sorted(games, key=lambda g: g['name'].lower())
    elif sort == 'year':
        games = sorted(games, key=lambda g: g['number_year'])
    elif sort == 'rating':
        games = sorted(games, key=lambda g: g['number_rating'], reverse=True)

    return render_template('table.html', games=games, platforms=platforms, genres=genres,
                           search=search, platform=platform, selected_genres=selected_genres,
                           sort=sort, active='table')


@app.route('/game/<int:game_id>')
def game(game_id):
    for g in get_games():
        if g['id'] == game_id:
            return render_template('game.html', game=g)
    abort(404)


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
