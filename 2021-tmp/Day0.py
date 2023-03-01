from util import Submarine


class Dummy(Submarine):

    def _parseLine(self, line):
        return line

    def __init__(self):
        self.input = self.getInput()
        print(self.input)


if __name__ == '__main__':
    submarine = Dummy()
