from util import Submarine
from collections import Counter


class Polymerization(Submarine):

    def _parseLine(self, line):
        if '>' in line:
            return tuple(line.split(' -> '))
        else:
            return line

    def __init__(self):
        input = self.getInput()
        self.template = input[0]
        self.rules = dict(input[2:])
        self.elementCount = Counter(self.template)
        self.pairCount = Counter(self.template[i:i+2]
                                 for i in range(len(self.template)-1))

    def step(self):
        newPairCount = Counter()
        for pair, occ in self.pairCount.items():
            c0, c2 = list(pair)
            c1 = self.rules[pair]
            newPairCount[c0+c1] += occ
            newPairCount[c1+c2] += occ
            self.elementCount[c1] += occ
        self.pairCount = newPairCount

    def diffAfterNSteps(self, n):
        for _ in range(n):
            self.step()
        sortedCount = self.elementCount.most_common()
        return sortedCount[0][1] - sortedCount[-1][1]


if __name__ == '__main__':
    submarine = Polymerization()
    print(submarine.diffAfterNSteps(10))

    submarine = Polymerization()
    print(submarine.diffAfterNSteps(40))
