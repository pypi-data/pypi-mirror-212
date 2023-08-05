import random
import copy
import time

from src.main.game.Player import Player
from src.main.game.DominoRound import DominoRound
from src.main.game.Scorer import AllFivesScorer


class Brain:
    def decide(self, round: DominoRound):
        """Decide which option to play. Each Brain class has a different way of determining this choice."""
        raise NotImplementedError("The base Brain does not know how to play, please use a subclass!")


class RandomBrain(Brain):
    """Picks an option at random"""

    def decide(self, round: DominoRound):
        return random.choice(round.valid_options())


class PlayerBrain(Brain):
    """Waits for a player to pick an option"""

    def __init__(self):
        super().__init__()
        self.decision = None

    def decide(self, round: DominoRound):
        counter = 600
        while self.decision is None and counter > 0:
            time.sleep(0.1)
            counter -= 1

        if self.decision is None:
            return random.choice(round.valid_options())

        decision = self.decision
        self.decision = None
        return round.valid_options()[decision]


class AllFivesGreedyBrain(Brain):
    """Picks the option that gives the most points on this turn"""

    def decide(self, round: DominoRound):
        best_option = None
        best_score = 0
        options = round.valid_options()

        for option in options:
            piece, origin, close = option
            board = copy.deepcopy(round.board)

            if board is round.board:
                raise Exception("Board is round board")
            if board.origin is round.board.origin:
                raise Exception("Same origin")

            board.play(piece, origin, close)

            score = AllFivesScorer.board_score(board)

            if score >= best_score:
                best_option = option
                best_score = score

        return best_option
