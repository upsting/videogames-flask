import requests
from flask import Flask, render_template, abort

# Bronvermelding staat in BRONVERMELDING.md.
API_URL = "https://my-json-server.typicode.com/upsting/videogames-api"

app = Flask(__name__)

@app.route('/')
def index():
    games = requests.get(f"{API_URL}/games").json()
    categories = requests.get(f"{API_URL}/categories").json()
    cat_dict = {c['id']: c['name'] for c in categories}
    for game in games:
        game['category'] = cat_dict.get(game['category_id'], 'Onbekend')
    return render_template('index.html', games=games)

@app.route('/game/<int:game_id>')
def game_detail(game_id):
    game = requests.get(f"{API_URL}/games/{game_id}").json()
    if not game or 'id' not in game:
        abort(404)
    categories = requests.get(f"{API_URL}/categories").json()
    cat_dict = {c['id']: c['name'] for c in categories}
    game['category'] = cat_dict.get(game['category_id'], 'Onbekend')
    return render_template('detail.html', game=game)

if __name__ == '__main__':
    app.run(debug=True)
