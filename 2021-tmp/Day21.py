from util import Submarine
import re
from copy import deepcopy


class DeterministicDice:

    def __init__(self, faces=100):
        self.outcome = None
        self.faces = faces
        self.count = 0

    def roll(self):
        self.count += 1
        if self.outcome is None or self.outcome == self.faces:
            self.outcome = 1
        else:
            self.outcome += 1
        return self.outcome


class Player:

    def __init__(self, id, pos):
        self.id = id
        self.pos = pos
        self.score = 0

    def move(self, steps):
        oldpos = self.pos
        newpos = (oldpos + steps - 1) % 10 + 1  # mod hack
        self.pos = newpos
        self.score += newpos


class Game(Submarine):

    def _parseLine(self, line):
        return tuple(int(d) for d in re.findall(r'\d+', line))

    def __init__(self):
        input = self.getInput()

        self.player1 = Player(*input[0])
        self.player2 = Player(*input[1])
        # players are switched at the start of the turn
        self.currentPlayer = self.player2

    def getOpponent(self, player: Player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def turn(self, steps):
        # switch player
        self.currentPlayer = self.getOpponent(self.currentPlayer)
        # move current player
        self.currentPlayer.move(steps)

    def getInfo(self):
        currentId = self.currentPlayer.id
        infoP1 = (self.player1.pos, self.player1.score)
        infoP2 = (self.player2.pos, self.player2.score)
        return currentId, infoP1, infoP2


class PracticeGame(Game):

    def __init__(self):
        super().__init__()
        self.dice = DeterministicDice()

    def runGame(self):
        while self.currentPlayer.score < 1000:
            steps = sum(self.dice.roll() for _ in range(3))
            self.turn(steps)
        loser = self.getOpponent(self.currentPlayer)
        print(loser.score * self.dice.count)


class DiracGame:

    # Possible sum of 3 rolls are 3, 4, 5, 6, 7, 8, 9
    # which corresponds to different no. of universe
    WEIGHTS = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    MEMO = dict()

    @classmethod
    def countUniverse(cls, game: Game):
        info = game.getInfo()
        _, (_, score1), (_, score2) = info

        if score1 >= 21:
            return 1, 0
        if score2 >= 21:
            return 0, 1

        try:
            return cls.MEMO[info]
        except KeyError:
            p1wins, p2wins = 0, 0
            for steps, weight in cls.WEIGHTS.items():
                newGame = deepcopy(game)
                newGame.turn(steps)
                p1, p2 = cls.countUniverse(newGame)
                p1wins += p1 * weight
                p2wins += p2 * weight
            cls.MEMO[info] = (p1wins, p2wins)
            return p1wins, p2wins


if __name__ == '__main__':
    submarine = PracticeGame()
    submarine.runGame()

    gameStart = Game()
    print(max(DiracGame.countUniverse(gameStart)))
