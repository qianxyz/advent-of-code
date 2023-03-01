from util import Submarine
from itertools import permutations, combinations
from collections import Counter
import numpy as np


def manhattan(xyz0, xyz1):
    return sum(abs(xyz0[i]-xyz1[i]) for i in range(3))


def generateRotations():
    AXES = {(1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)}
    for axes in permutations(AXES, 3):
        if np.linalg.det(axes) == 1:
            yield np.array(axes)


ROTATIONS = list(generateRotations())


class Scanner:

    def __init__(self, id, readings, trueReadings=None, pos=None):
        self.id = id
        self.readings = np.array(readings)
        self.trueReadings = np.array(trueReadings)
        self.pos = np.array(pos)

        # unsafe to use set here
        self.pairDists = Counter(self.generatePairDists())

    def generatePairDists(self):
        for xyz0, xyz1 in combinations(self.readings, 2):
            yield manhattan(xyz0, xyz1)

    def cmpPairDists(self, other: 'Scanner'):
        """A necessary condition for two scanners to align."""
        intersect = self.pairDists & other.pairDists
        return sum(intersect.values()) >= 66

    @staticmethod
    def arrayToListOfTuples(readings):
        return [tuple(reading) for reading in readings]

    def getReadingsAsList(self):
        return Scanner.arrayToListOfTuples(self.readings)

    def getTrueReadingsAsList(self):
        assert self.trueReadings.tolist() is not None, \
            'True readings not set'
        return Scanner.arrayToListOfTuples(self.trueReadings)

    def getPosition(self):
        assert self.pos.tolist() is not None, \
            'True position not set'
        return tuple(self.pos)

    @staticmethod
    def translation(readings, t):
        return readings + t

    @staticmethod
    def rotation(readings, r):
        return np.matmul(readings, r)

    def align(self, base: 'Scanner'):
        """Try to align self with the base scanner provided.

        If an alignment with at least 12 overlapping beacons exist,
        set self.trueReadings accordingly and return True.
        Otherwise, return False.
        """
        assert base.trueReadings is not None, \
            'Base scanner true readings not set'
        if not self.cmpPairDists(base):
            return False
        for tr0 in self.readings:
            tryReadings0 = Scanner.translation(self.readings, -tr0)
            for rot in ROTATIONS:
                tryReadings1 = Scanner.rotation(tryReadings0, rot)
                for tr1 in base.trueReadings:
                    tryReadings2 = Scanner.translation(tryReadings1, tr1)
                    if Scanner.overlaps(tryReadings2, base.trueReadings) >= 12:
                        self.trueReadings = tryReadings2
                        # set true position
                        pos = (0, 0, 0)
                        pos = Scanner.translation(pos, -tr0)
                        pos = Scanner.rotation(pos, rot)
                        pos = Scanner.translation(pos, tr1)
                        self.pos = pos
                        print('Scanner', self.id, 'aligned to', base.id,
                              'at', tuple(pos))
                        return True
        return False

    @staticmethod
    def overlaps(readings0: np.ndarray, readings1: np.ndarray):
        """Count number of overlaps."""
        re0 = Scanner.arrayToListOfTuples(readings0)
        re1 = Scanner.arrayToListOfTuples(readings1)
        re0, re1 = set(re0), set(re1)
        return len(set.intersection(re0, re1))


class AlignScanners(Submarine):

    def _parseLine(self, line):
        if 'scanner' in line:
            return int(line.split()[2])
        elif line:
            return tuple(int(n) for n in line.split(','))

    def __init__(self):
        input = self.getInput()
        input.append(None)

        self.scanners: list[Scanner] = []
        self.fixed: set[Scanner] = set()
        self.unfixed: set[Scanner] = set()
        while None in input:
            i = input.index(None)
            id = input[0]
            readings = input[1:i]
            if id == 0:
                scanner = Scanner(id, readings, readings, (0, 0, 0))
                self.fixed.add(scanner)
                self.beacons = set(readings)
            else:
                scanner = Scanner(id, readings)
                self.unfixed.add(scanner)
            self.scanners.append(scanner)
            del input[:i+1]

    def alignAll(self):
        print('Scanner 0 set at', (0, 0, 0))
        while self.unfixed:
            base = self.fixed.pop()
            for scanner in self.unfixed:
                if scanner.align(base):
                    self.fixed.add(scanner)
                    newBeacons = scanner.getTrueReadingsAsList()
                    self.beacons.update(set(newBeacons))
            self.unfixed -= self.fixed

    def getNumOfBeacons(self):
        return len(self.beacons)

    def largestManhattanDistance(self):
        distances = []
        positions = [scanner.getPosition() for scanner in self.scanners]
        for pos0, pos1 in combinations(positions, 2):
            distances.append(manhattan(pos0, pos1))
        return max(distances)


if __name__ == '__main__':
    submarine = AlignScanners()
    submarine.alignAll()
    print('Total no. of beacons:', submarine.getNumOfBeacons())
    print('Largest distance between scanners:',
          submarine.largestManhattanDistance())
