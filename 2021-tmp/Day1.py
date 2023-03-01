from util import Submarine


class SonarSweep(Submarine):

    def _parseLine(self, line):
        return int(line)

    def __init__(self):
        self.depths = self.getInput()
        print(self.depths)

    def timesOfIncrease(self, lenWindow):
        return sum(self.depths[i] > self.depths[i - lenWindow]
                   for i in range(lenWindow, len(self.depths)))


if __name__ == '__main__':
    submarine = SonarSweep()
    print(submarine.timesOfIncrease(1))
    print(submarine.timesOfIncrease(3))
