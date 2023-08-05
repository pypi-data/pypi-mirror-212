from flask import Flask

from src.main.game.Game import Game
from src.main.game.Brain import AllFivesGreedyBrain

app = Flask("Domino")

game = Game(AllFivesGreedyBrain(), AllFivesGreedyBrain())


@app.route("/status")
def get_status():
    return game.state

