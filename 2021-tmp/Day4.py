from util import Submarine


class Bingo(Submarine):

    def _parseLine(self, line):
        strs = line.replace(',', ' ').split()
        return [int(s) for s in strs]

    def __init__(self):
        input = self.getInput()
        self.rand = input[0]
        self.boards = [input[i:i+5] for i in range(2, len(input), 6)]

    def playGame(self):
        self.score = None
        for num in self.rand:
            self.step(num)
            if self.score is not None:
                return self.score

    def step(self, num):
        self.currentNum = num
        for n in range(len(self.boards)):
            for i in range(5):
                for j in range(5):
                    if self.boards[n][i][j] == num:
                        self.boards[n][i][j] = -1
                        self.checkWin((n, i, j))

    def checkWin(self, indices):
        n, i, j = indices
        if self.boards[n][i] == [-1] * 5:
            self.registerScore(n)
        elif [self.boards[n][k][j] for k in range(5)] == [-1] * 5:
            self.registerScore(n)

    def registerScore(self, n):
        self.score = self.calculateScore(n)

    def calculateScore(self, n):
        return sum(self.boards[n][i][j]
                   for i in range(5) for j in range(5)
                   if self.boards[n][i][j] != -1) * self.currentNum


class BingoLastWin(Bingo):

    def playGame(self):
        self.lastWinBoardIndex = None
        self.scores = [None] * len(self.boards)
        for num in self.rand:
            self.step(num)
        return self.scores[self.lastWinBoardIndex]

    def registerScore(self, n):
        if self.scores[n] is None:
            self.lastWinBoardIndex = n
            self.scores[n] = self.calculateScore(n)


if __name__ == '__main__':
    submarine = Bingo()
    print(submarine.playGame())

    submarine = BingoLastWin()
    print(submarine.playGame())
