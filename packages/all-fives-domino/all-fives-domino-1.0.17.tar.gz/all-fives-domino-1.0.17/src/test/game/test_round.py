from src.main.game.DominoRound import DominoRound
from src.main.game.Brain import AllFivesGreedyBrain, RandomBrain
from src.main.game.Player import Player


def test_round_initialization():
    # Initialize a round and check there's a valid starting setup
    round = DominoRound(Player(RandomBrain()), Player(RandomBrain()))

    assert round.board.origin is not None
    assert round.board.origin.is_double


