import jsons

from src.main.game.DominoRound import DominoRound
from src.main.game.Player import Player

from src.main.game.exceptions.Game import GameWinSignal

class GameState:
    WAITING = "Waiting"
    RUNNING = "Running"
    OVER = "Over"


class Game:
    def __init__(self, brain1: "Brain", brain2: "Brain"):
        self.target_score = 305
        self.eggs = 0
        self.rounds = 0
        self.player1 = Player(brain1)
        self.player2 = Player(brain2)
        self.status = GameState.WAITING
        self.round: DominoRound = None

    def run(self):
        self.status = GameState.RUNNING
        try:
            while self.rounds < 1000:
                self.rounds += 1
                self.round = DominoRound(self.player1, self.player2)
                self.round.run()
        except GameWinSignal as win_signal:
            self.status = GameState.OVER
            print(win_signal)

    @property
    def state(self):
        state = {
            "status": self.status,
            "player1": self.player1,
            "player2": self.player2,
            "eggs": self.eggs,
            "targetScore": self.target_score,
            "rounds": self.rounds
        }

        if self.round is not None:
            state["board"] = self.round.board
            state["options"] = self.round.valid_options()

        return state
