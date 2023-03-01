from util import Submarine
import heapq


class Chiton(Submarine):

    def _parseLine(self, line):
        return [int(d) for d in line]

    def __init__(self):
        map = self.getInput()
        self.map = self.plotMap(map)
        self.xSize = len(self.map)
        self.ySize = len(self.map[0])
        self.start = (0, 0)
        self.goal = (self.xSize - 1, self.ySize - 1)
        self.allLocs = [(x, y) for x in range(self.xSize)
                        for y in range(self.ySize)]

    def plotMap(self, map):
        return map

    def isValidLoc(self, loc):
        x, y = loc
        return 0 <= x < self.xSize and 0 <= y < self.ySize

    def getAdjacentLocs(self, loc):
        DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        x, y = loc
        for dx, dy in DIRECTIONS:
            newLoc = x + dx, y + dy
            if self.isValidLoc(newLoc):
                yield newLoc

    def getRiskLevel(self, loc):
        x, y = loc
        return self.map[x][y]

    def search(self):
        closed = set()
        fringe = []
        startNode = (0, self.start)
        heapq.heappush(fringe, startNode)
        while fringe:
            cost, loc = heapq.heappop(fringe)
            if loc == self.goal:
                return cost
            if loc not in closed:
                closed.add(loc)
                for child in self.getAdjacentLocs(loc):
                    childCost = cost + self.getRiskLevel(child)
                    childNode = (childCost, child)
                    heapq.heappush(fringe, childNode)


class ChitonFullMap(Chiton):

    def plotMap(self, map):
        xSize, ySize = len(map), len(map[0])
        self.scale = 5
        fullMap = [[0] * (self.scale * ySize)
                   for _ in range(self.scale * xSize)]
        for xChunk in range(self.scale):
            for yChunk in range(self.scale):
                for x in range(xSize):
                    for y in range(ySize):
                        v = map[x][y] + xChunk + yChunk
                        v = (v - 1) % 9 + 1
                        newx = xChunk * xSize + x
                        newy = yChunk * ySize + y
                        fullMap[newx][newy] = v
        return fullMap


if __name__ == '__main__':
    submarine = Chiton()
    print(submarine.search())

    submarine = ChitonFullMap()
    print(submarine.search())
