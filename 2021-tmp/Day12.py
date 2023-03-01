from util import Submarine
import string
from collections import Counter

LOWERCASE = set(string.ascii_lowercase)


class PassagePathing(Submarine):

    def _parseLine(self, line):
        return tuple(line.split('-'))

    def __init__(self):
        edges = self.getInput()
        self.nodes = set(p for edge in edges for p in edge)
        self.edges = dict()
        for p in self.nodes:
            self.edges[p] = [q for q in self.nodes
                             if (p, q) in edges or (q, p) in edges]
        self.ongoingPaths = [['start']]
        self.finishedPaths = []

    def isSmall(self, node):
        return set(node).issubset(LOWERCASE)

    def search(self):
        while self.ongoingPaths:
            currentPath = self.ongoingPaths.pop()
            head = currentPath[-1]
            if head == 'end':
                self.finishedPaths.append(currentPath)
                continue
            for child in self.edges[head]:
                if self.isValidNextNode(currentPath, child):
                    newPath = currentPath + [child]
                    self.ongoingPaths.append(newPath)

    def isValidNextNode(self, path, node):
        return not (self.isSmall(node) and node in path)

    def printValidPaths(self):
        self.search()
        # for path in self.finishedPaths:
        #     print(','.join(path))
        print('No. of paths:', len(self.finishedPaths))


class PassagePathingSmallTwice(PassagePathing):

    def isValidNextNode(self, path, node):
        if node == 'start':
            return False
        return not (self.isVisitedSmallTwice(path)
                    and self.isSmall(node)
                    and node in path)

    def isVisitedSmallTwice(self, path):
        c = Counter(path)
        for node in c:
            if self.isSmall(node) and c[node] > 1:
                return True
        return False


if __name__ == '__main__':
    submarine = PassagePathing()
    submarine.printValidPaths()

    submarine = PassagePathingSmallTwice()
    submarine.printValidPaths()
