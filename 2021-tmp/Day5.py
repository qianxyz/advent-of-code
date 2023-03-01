from util import Submarine


class HydrothermalVenture(Submarine):

    def _parseLine(self, line):
        strs = line.replace(' -> ', ',').split(',')
        x0, y0, x1, y1 = map(int, strs)
        return ((x0, y0), (x1, y1))

    def __init__(self):
        self.pairs = self.getInput()
        self.mapSize = 1000
        self.map = [[0] * self.mapSize for _ in range(self.mapSize)]

    def drawMap(self):
        for pair in self.pairs:
            self.drawLine(pair)

    def drawLine(self, pair):
        ((x0, y0), (x1, y1)) = pair
        if x0 == x1:
            for y in range(min(y0, y1), max(y0, y1) + 1):
                self.map[x0][y] += 1
        elif y0 == y1:
            for x in range(min(x0, x1), max(x0, x1) + 1):
                self.map[x][y0] += 1

    def checkDanger(self):
        self.drawMap()
        return sum(self.map[x][y] >= 2
                   for x in range(self.mapSize)
                   for y in range(self.mapSize))


class HydrothermalVentureDiag(HydrothermalVenture):

    def drawLine(self, pair):
        ((x0, y0), (x1, y1)) = pair
        xs = self.interval(x0, x1)
        ys = self.interval(y0, y1)
        for x, y in zip(xs, ys):
            self.map[x][y] += 1

    def interval(self, x0, x1):
        """
        Returns a list of consecutive integers including x0 and x1.
        Special case: when x0 == x1, return a long list of x0
        so zip() works properly.
        """
        if x0 == x1:
            return [x0] * self.mapSize
        sign = 1 if x1 > x0 else -1
        return list(range(x0, x1 + sign, sign))


if __name__ == '__main__':
    submarine = HydrothermalVenture()
    print(submarine.checkDanger())

    submarine = HydrothermalVentureDiag()
    print(submarine.checkDanger())
