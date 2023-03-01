from util import Submarine


class SeaCucumber(Submarine):

    def _parseLine(self, line):
        return list(line)

    def __init__(self) -> None:
        self.grid = self.getInput()
        self.xrange = len(self.grid)
        self.yrange = len(self.grid[0])
        self.allpos = [(x, y) for x in range(self.xrange)
                       for y in range(self.yrange)]

    def checkEast(self):
        """Returns a list of east-facing movable cucumbers."""
        movable = []
        for x, y in self.allpos:
            if self.grid[x][y] == '>':
                try:
                    east = self.grid[x][y+1]
                except IndexError:
                    east = self.grid[x][0]
                if east == '.':
                    movable.append((x, y))
        return movable

    def checkSouth(self):
        """Returns a list of south-facing movable cucumbers."""
        movable = []
        for x, y in self.allpos:
            if self.grid[x][y] == 'v':
                try:
                    south = self.grid[x+1][y]
                except IndexError:
                    south = self.grid[0][y]
                if south == '.':
                    movable.append((x, y))
        return movable

    def moveEast(self, movable):
        """Move all > in movable to east."""
        for x, y in movable:
            self.grid[x][y] = '.'
            try:
                self.grid[x][y+1] = '>'
            except IndexError:
                self.grid[x][0] = '>'

    def moveSouth(self, movable):
        """Move all v in movable to south."""
        for x, y in movable:
            self.grid[x][y] = '.'
            try:
                self.grid[x+1][y] = 'v'
            except IndexError:
                self.grid[0][y] = 'v'

    def step(self):
        """Returns True iff no cucumber moved."""
        movableEast = self.checkEast()
        self.moveEast(movableEast)
        movableSouth = self.checkSouth()
        self.moveSouth(movableSouth)
        return not movableEast and not movableSouth

    def run(self):
        stepnum = 1
        while not self.step():
            stepnum += 1
        return stepnum


if __name__ == '__main__':
    submarine = SeaCucumber()
    print(submarine.run())
