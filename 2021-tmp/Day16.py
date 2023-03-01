from util import Submarine


class PacketDecoder(Submarine):

    def _parseLine(self, line):
        return line

    def __init__(self):
        self.hexStr = self.getInput()[0]
        self.binStr = self.hexToBin(self.hexStr)
        self.pointer = 0
        self.versions = []

    def hexToBin(self, hexStr):
        return ''.join(format(int(d, 16), '0>4b') for d in hexStr)

    def getBitsStr(self, n):
        p = self.pointer
        binStr = self.binStr[p:p+n]
        self.pointer += n
        return binStr

    def getBitsDec(self, n):
        binStr = self.getBitsStr(n)
        return int(binStr, 2)

    def parse(self):
        packetVersion = self.getBitsDec(3)
        self.versions.append(packetVersion)
        packetType = self.getBitsDec(3)
        if packetType == 4:
            return self.parseLiteralValue()
        else:
            lengthTypeID = self.getBitsStr(1)
            if lengthTypeID == '0':
                subpackets = self.parseFixedLength()
            else:
                subpackets = self.parseFixedNum()
            return self.evaluateOperation(packetType, subpackets)

    def evaluateOperation(self, op, subpackets):
        if op == 0:
            return sum(subpackets)
        elif op == 1:
            val = 1
            for n in subpackets:
                val *= n
            return val
        elif op == 2:
            return min(subpackets)
        elif op == 3:
            return max(subpackets)
        else:
            fst, snd = subpackets
            if op == 5:
                return int(fst > snd)
            elif op == 6:
                return int(fst < snd)
            elif op == 7:
                return int(fst == snd)

    def parseLiteralValue(self):
        valStr = ''
        while True:
            valBlock = self.getBitsStr(5)
            valStr += valBlock[1:]
            if valBlock[0] == '0':
                break
        val = int(valStr, 2)
        return val

    def parseFixedLength(self):
        length = self.getBitsDec(15)
        pStart = self.pointer
        while self.pointer < pStart + length:
            yield self.parse()

    def parseFixedNum(self):
        num = self.getBitsDec(11)
        for _ in range(num):
            yield self.parse()

    def printVersionSum(self):
        print(sum(self.versions))


if __name__ == '__main__':
    submarine = PacketDecoder()
    print(submarine.parse())
    submarine.printVersionSum()
