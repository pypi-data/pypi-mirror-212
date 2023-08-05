import random
import copy

from src.main.game.Player import Player
from src.main.game.DominoRound import DominoRound
from src.main.game.Scorer import AllFivesScorer


class Brain:
    def decide(self, round: DominoRound):
        raise NotImplementedError("The base Brain does not know how to play, please use a subclass!")


class RandomBrain(Brain):
    def decide(self, round: DominoRound):
        return random.choice(round.valid_options())


class AllFivesGreedyBrain(Brain):
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
