import __main__
import os


class Submarine:

    def getInput(self):
        dayNo = __main__.__file__[3:-3]
        inputFile = os.path.join('inputs', 'input' + dayNo + '.txt')
        with open(inputFile) as f:
            return [self._parseLine(line.rstrip()) for line in f.readlines()]

    def _parseLine(self, line):
        pass
