from src.main.game.DominoRound import DominoRound
from src.main.game.Brain import AllFivesGreedyBrain, RandomBrain


def test_round_initialization():
    # Initialize a round and check there's a valid starting setup
    round = DominoRound(RandomBrain(), RandomBrain())

    assert round.board.origin is not None
    assert round.board.origin.is_double


