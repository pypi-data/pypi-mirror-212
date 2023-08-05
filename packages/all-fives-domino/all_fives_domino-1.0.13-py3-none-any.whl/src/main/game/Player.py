from src.main.game.Hand import Hand


class Player:
    def __init__(self, brain: "Brain", round: "DominoRound"):
        self.hand = Hand()
        self.score = 0
        self.brain = brain
        self.round = round

    def decide(self):
        return self.brain.decide(self, self.round)

    def draw(self):
        piece = self.round.pool.pop()
        self.hand.add(piece)
