from util import Submarine


class CrabAlign(Submarine):

    def _parseLine(self, line):
        return [int(s) for s in line.split(',')]

    def __init__(self):
        self.crabs = self.getInput()[0]

    def fuel(self, pos):
        return sum(abs(pos - p) for p in self.crabs)

    def leastfuel(self):
        # sum(abs(x - n) for n in ns) takes minimum
        # when x is the median of ns.
        sortedCrabs = sorted(self.crabs)
        bestPos = sortedCrabs[len(sortedCrabs) // 2]
        return self.fuel(bestPos)


class CrabAlignSqr(CrabAlign):

    def fuel(self, pos):
        return sum(abs(pos - p) * (abs(pos - p) + 1) // 2
                   for p in self.crabs)

    def leastfuel(self):
        ps = range(min(self.crabs), max(self.crabs) + 1)
        return min(self.fuel(p) for p in ps)


if __name__ == '__main__':
    submarine = CrabAlign()
    print(submarine.leastfuel())

    submarine = CrabAlignSqr()
    print(submarine.leastfuel())
