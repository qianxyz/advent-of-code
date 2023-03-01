from util import Submarine


class BinaryDiagnostic(Submarine):

    def _parseLine(self, line):
        return line

    def __init__(self):
        self.binStrs = self.getInput()

    def findPowerRates(self):
        N, L = len(self.binStrs), len(self.binStrs[0])
        gamma = epsilon = ''
        for j in range(L):
            num0 = sum(self.binStrs[i][j] == '0' for i in range(N))
            num1 = N - num0
            gamma += '1' if num1 >= num0 else '0'
            epsilon += '0' if num1 >= num0 else '1'
        gamma = int(gamma, 2)
        epsilon = int(epsilon, 2)
        return gamma, epsilon

    def findLifeRatesHelper(self, isMostCommon=True):
        L = len(self.binStrs[0])
        bStrs = self.binStrs
        for j in range(L):
            if len(bStrs) == 1:
                break
            bStrs0 = [s for s in bStrs if s[j] == '0']
            bStrs1 = [s for s in bStrs if s[j] == '1']
            num0, num1 = len(bStrs0), len(bStrs1)
            if isMostCommon:
                bStrs = bStrs1 if num1 >= num0 else bStrs0
            else:
                bStrs = bStrs0 if num1 >= num0 else bStrs1
        return int(bStrs[0], 2)

    def findLifeRates(self):
        o2 = self.findLifeRatesHelper(isMostCommon=True)
        co2 = self.findLifeRatesHelper(isMostCommon=False)
        return o2, co2


if __name__ == '__main__':
    submarine = BinaryDiagnostic()

    gamma, epsilon = submarine.findPowerRates()
    print(gamma * epsilon)

    o2, co2 = submarine.findLifeRates()
    print(o2 * co2)
