from util import Submarine


class SmokeBasin(Submarine):

    def _parseLine(self, line):
        return [int(d) for d in line]

    def __init__(self):
        self.hmap = self.getInput()
        self.xSize = len(self.hmap)
        self.ySize = len(self.hmap[0])
        self.allLocs = [(x, y) for x in range(self.xSize)
                        for y in range(self.ySize)]

    def isValidLocation(self, loc):
        x, y = loc
        return 0 <= x < self.xSize and 0 <= y < self.ySize

    def getHeight(self, loc):
        x, y = loc
        return self.hmap[x][y]

    def getAdjacentLocations(self, loc):
        x, y = loc
        DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in DIRECTIONS:
            newLoc = x + dx, y + dy
            if self.isValidLocation(newLoc):
                yield newLoc

    def isLowPoint(self, loc):
        for adjLoc in self.getAdjacentLocations(loc):
            if self.getHeight(loc) >= self.getHeight(adjLoc):
                return False
        return True

    def findLowPoints(self):
        for loc in self.allLocs:
            if self.isLowPoint(loc):
                yield loc

    def getRiskLevel(self, loc):
        return 1 + self.getHeight(loc)

    def getRiskLevels(self):
        return sum(self.getRiskLevel(lowPoint)
                   for lowPoint in self.findLowPoints())

    def findBasinArea(self, lowPoint):
        closed = set()
        fringe = [lowPoint]
        while fringe:
            loc = fringe.pop()
            if loc not in closed:
                closed.add(loc)
                for adjLoc in self.getAdjacentLocations(loc):
                    if self.getHeight(adjLoc) != 9:
                        fringe.append(adjLoc)
        return len(closed)

    def findThreeLargestBasins(self):
        basinAreas = []
        for lowPoint in self.findLowPoints():
            basinAreas.append(self.findBasinArea(lowPoint))
        basinAreas.sort(reverse=True)
        return basinAreas[0] * basinAreas[1] * basinAreas[2]


if __name__ == '__main__':
    submarine = SmokeBasin()
    print(submarine.getRiskLevels())

    print(submarine.findThreeLargestBasins())
