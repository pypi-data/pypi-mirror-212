from flask import Flask, send_from_directory
import json

from src.main.game.Game import Game, GameStatus
from src.main.game.Brain import AllFivesGreedyBrain

app = Flask(__name__)

game = Game(AllFivesGreedyBrain(), AllFivesGreedyBrain())


@app.route("/")
def get_page():
    return send_from_directory("static", "index.html")


@app.route("/status")
def get_status():
    return game.json()


@app.route("/start")
def start_game():
    if game.status == GameStatus.WAITING:
        game.run()
        return "OK"

    return "No game waiting"
