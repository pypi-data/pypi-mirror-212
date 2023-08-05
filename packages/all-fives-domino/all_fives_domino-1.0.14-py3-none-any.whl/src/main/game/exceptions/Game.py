class GameWinSignal(Exception):
    """Raised when a player wins to stop the game"""
    def __init__(self, winner: "Player", loser: "Player"):
        super().__init__(f"Player wins {winner.score} - {loser.score}!")
        self.winner = winner
        self.loser = loser
