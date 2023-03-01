from util import Submarine
from time import perf_counter

DIRECTIONS = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]]


class Safelist(list):
    """List that rejects negative indices."""

    def __getitem__(self, index):
        if index < 0:
            raise IndexError('Safelist do not accept negative index')
        return super().__getitem__(index)


class TrenchMap(Submarine):

    def _parseLine(self, line):
        return [0 if c == '.' else 1 for c in line]

    def __init__(self):
        input = self.getInput()
        self.algo = input[0]
        self.grid = Safelist(Safelist(lst) for lst in input[2:])
        self.xrange = len(self.grid)
        self.yrange = len(self.grid[0])
        self.memo = dict()

    def getPixel(self, x, y, t):
        """Return the pixel at (x, y) at time t."""
        if t == 0:
            try:
                return self.grid[x][y]
            except IndexError:
                return 0
        else:
            try:
                return self.memo[(x, y, t)]
            except KeyError:
                s = ''
                for dx, dy in DIRECTIONS:
                    s += str(self.getPixel(x+dx, y+dy, t-1))
                i = int(s, 2)
                self.memo[(x, y, t)] = self.algo[i]
                return self.algo[i]

    def printGrid(self, t, padding=0):
        for x in range(-padding, self.xrange+padding):
            s = ''
            for y in range(-padding, self.yrange+padding):
                s += '.' if self.getPixel(x, y, t) == 0 else '#'
            print(s)

    def countLitPadding(self, t, padding=0):
        return sum(self.getPixel(x, y, t)
                   for x in range(-padding, self.xrange+padding)
                   for y in range(-padding, self.yrange+padding))

    def countLit(self, t):
        counts = []
        for padding in range(100):
            c = self.countLitPadding(t, padding)
            if counts and counts[-1] == c:
                print('Converged at padding', padding)
                return c
            else:
                counts.append(c)
        print('Does not converge. Increase padding')


if __name__ == '__main__':
    submarine = TrenchMap()
    start = perf_counter()
    print(submarine.countLit(50))
    end = perf_counter()
    print('time:', end-start)
