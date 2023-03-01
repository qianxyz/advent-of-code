from util import Submarine


class OctopusFlash(Submarine):

    def _parseLine(self, line):
        return [int(d) for d in line]

    def __init__(self):
        self.grid = self.getInput()
        self.xSize = len(self.grid)
        self.ySize = len(self.grid[0])
        self.allLocs = [(x, y) for x in range(self.xSize)
                        for y in range(self.ySize)]

    def getEnergy(self, loc):
        x, y = loc
        return self.grid[x][y]

    def isFullEnergy(self, loc):
        return self.getEnergy(loc) > 9

    def increaseEnergy(self, loc):
        x, y = loc
        self.grid[x][y] += 1

    def clearEnergy(self, loc):
        x, y = loc
        self.grid[x][y] = 0

    def isValidLoc(self, loc):
        x, y = loc
        return 0 <= x < self.xSize and 0 <= y < self.ySize

    def getAdjacentLocs(self, loc):
        DIRECTIONS = [(dx, dy) for dx in [-1, 0, 1]
                      for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]
        x, y = loc
        for dx, dy in DIRECTIONS:
            newLoc = x + dx, y + dy
            if self.isValidLoc(newLoc):
                yield newLoc

    def flash(self, loc):
        for adjLoc in self.getAdjacentLocs(loc):
            self.increaseEnergy(adjLoc)
            if self.isFullEnergy(adjLoc):
                yield adjLoc

    def step(self):
        for loc in self.allLocs:
            self.increaseEnergy(loc)

        flashed = set()
        fringe = [loc for loc in self.allLocs if self.isFullEnergy(loc)]
        while fringe:
            loc = fringe.pop()
            if loc not in flashed:
                flashed.add(loc)
                for adjFullEnergyLoc in self.flash(loc):
                    fringe.append(adjFullEnergyLoc)

        for flashedLoc in flashed:
            self.clearEnergy(flashedLoc)

        return len(flashed)

    def flashesInNSteps(self, n):
        flashes = 0
        for _ in range(n):
            flashes += self.step()
        return flashes

    def firstAllFlash(self):
        numStep = 1
        while self.step() != len(self.allLocs):
            numStep += 1
        return numStep


if __name__ == '__main__':
    submarine = OctopusFlash()
    print(submarine.flashesInNSteps(100))

    submarine = OctopusFlash()
    print(submarine.firstAllFlash())
