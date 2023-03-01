from util import Submarine
from collections import Counter


class LanternFish(Submarine):

    def _parseLine(self, line):
        return [int(s) for s in line.split(',')]

    def __init__(self):
        self.fishes = self.getInput()[0]

    def proceedDay(self):
        newFish = 0
        for i, n in enumerate(self.fishes):
            if n > 0:
                self.fishes[i] -= 1
            else:
                self.fishes[i] = 6
                newFish += 1
        self.fishes += [8] * newFish

    def proceedDays(self, n):
        for _ in range(n):
            self.proceedDay()

    def getNumOfFish(self):
        return len(self.fishes)


class LanternFishWithDict(LanternFish):

    def __init__(self):
        super().__init__()
        self.fishDict = Counter(self.fishes)

    def proceedDay(self):
        newFishDict = Counter()
        for i in range(8):
            newFishDict[i] = self.fishDict[i+1]
        newFishDict[6] += self.fishDict[0]
        newFishDict[8] = self.fishDict[0]
        self.fishDict = newFishDict

    def getNumOfFish(self):
        # Counter.total() available in 3.10
        return sum(self.fishDict.values())


if __name__ == '__main__':
    submarine = LanternFish()
    submarine.proceedDays(80)
    print(submarine.getNumOfFish())

    submarine = LanternFishWithDict()
    submarine.proceedDays(256)
    print(submarine.getNumOfFish())
