import jsons

from src.main.game.DominoRound import DominoRound
from src.main.game.Player import Player

from src.main.game.exceptions.Game import GameWinSignal


class GameStatus:
    WAITING = "Waiting"
    RUNNING = "Running"
    OVER = "Over"


class Game:
    def __init__(self, brain1: "Brain", brain2: "Brain"):
        self.target_score = 305
        self.eggs = 0
        self.rounds = 0
        self.player1 = Player(brain1, "Player 1")
        self.player2 = Player(brain2, "Player 2")
        self.status = GameStatus.WAITING
        self.round: DominoRound = None

    def json(self):
        return {
            "targetScore": self.target_score,
            "eggs": self.eggs,
            "rounds": self.rounds,
            "player1": self.player1.json(),
            "player2": self.player2.json(),
            "status": self.status,
            "round": None if self.round is None else self.round.json()
        }

    def run(self):
        self.status = GameStatus.RUNNING
        try:
            while self.rounds < 1000:
                self.rounds += 1
                self.round = DominoRound(self.player1, self.player2)
                self.round.run()
                self.award_round_score()
        except GameWinSignal as win_signal:
            self.status = GameStatus.OVER
            print(win_signal)

    def award_round_score(self):
        player1_score = sum([piece.points for piece in self.player1.hand])
        player2_score = sum([piece.points for piece in self.player2.hand])

        if player1_score == player2_score:
            self.eggs += player1_score + player2_score
        elif player1_score < player2_score:
            self.player1.score += player2_score + self.eggs
            self.eggs = 0
        else:
            self.player2.score += player1_score + self.eggs
            self.eggs = 0
