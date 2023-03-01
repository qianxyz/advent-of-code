from util import Submarine
from collections import Counter


class SevenSegment(Submarine):

    def _parseLine(self, line):
        patterns, digits = line.split('|')
        patterns = patterns.split()
        digits = digits.split()
        return patterns, digits

    def __init__(self):
        self.segStrs = self.getInput()

    def count1478(self):
        count = 0
        for _, digits in self.segStrs:
            for digit in digits:
                if len(digit) in {2, 3, 4, 7}:
                    count += 1
        return count

    def decryptDict(self, patterns):
        """
        Return a 1-1 correspondence (dict) between a-g and A-G.
        Warning: messy logic ahead!
        """
        encDict = dict()

        c = Counter(''.join(patterns))
        invc = dict()
        for seg, occ in c.items():
            invc.setdefault(occ, set()).add(seg)
        encDict['F'] = invc[9].pop()
        encDict['B'] = invc[6].pop()
        encDict['E'] = invc[4].pop()

        seg1 = set([p for p in patterns if len(p) == 2][0])
        seg4 = set([p for p in patterns if len(p) == 4][0])
        encDict['A'] = (invc[8] - seg1).pop()
        encDict['C'] = invc[8].intersection(seg1).pop()
        encDict['G'] = (invc[7] - seg4).pop()
        encDict['D'] = invc[7].intersection(seg4).pop()

        decDict = {v: k for k, v in encDict.items()}
        return decDict

    def decrypt(self, digits, decDict):
        SEG_TO_DIGIT = {'ABCEFG':  '0',
                        'CF':      '1',
                        'ACDEG':   '2',
                        'ACDFG':   '3',
                        'BCDF':    '4',
                        'ABDFG':   '5',
                        'ABDEFG':  '6',
                        'ACF':     '7',
                        'ABCDEFG': '8',
                        'ABCDFG':  '9'}

        numStr = ''
        for loStr in digits:
            upStr = ''
            for loChar in loStr:
                upStr += decDict[loChar]
            numStr += SEG_TO_DIGIT[''.join(sorted(upStr))]
        return int(numStr)

    def decryptAll(self):
        decryptedNums = []
        for patterns, digits in self.segStrs:
            decDict = self.decryptDict(patterns)
            decryptedNums.append(self.decrypt(digits, decDict))
        return sum(decryptedNums)


if __name__ == '__main__':
    submarine = SevenSegment()
    print(submarine.count1478())

    print(submarine.decryptAll())
