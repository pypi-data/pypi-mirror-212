import pytest

from src.main.game.DominoRound import DominoRound
from src.main.game.Brain import RandomBrain
from src.main.game.Hand import Hand
from src.main.game.Piece import Piece


@pytest.fixture
def example_round():
    return DominoRound(RandomBrain(), RandomBrain())


@pytest.fixture
def example_round_all_options():
    round = DominoRound(RandomBrain(), RandomBrain())
    round.board.origin = Piece(5, 5)
    round.current_player.hand = Hand(
        Piece(5, 0),
        Piece(5, 1),
        Piece(5, 2),
        Piece(5, 3)
    )

    return round
