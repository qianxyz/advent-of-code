from util import Submarine
import re


class TrickShot(Submarine):

    def _parseLine(self, line):
        return [int(n) for n in re.findall(r'-?\d+', line)]

    def __init__(self):
        L, R, D, U = self.getInput()[0]
        self.xrange = (L, R)
        self.yrange = (D, U)
        self.xv = self.yv = None
        self.xp = self.yp = None
        self.possibleInitVs = []

    def step(self):
        self.xp += self.xv
        self.yp += self.yv
        if self.xv > 0:
            self.xv -= 1
        elif self.xv < 0:
            self.xv += 1
        self.yv -= 1

    def maxHeight(self, xv0, yv0):
        """
        Launch with velocity (xv0, yv0). If the probe does enter
        the target area, return the highest point of the trajectory;
        Otherwise, return None.
        """
        self.xv, self.yv = xv0, yv0
        self.xp, self.yp = 0, 0
        trajectory = []
        while True:
            trajectory.append((self.xp, self.yp))
            self.step()
            if self.isInTargetArea():
                self.possibleInitVs.append((xv0, yv0))
                return max(y for _, y in trajectory)
            elif self.isTerminated():
                return None

    def search(self):
        heights = []
        _, R = self.xrange
        D, _ = self.yrange
        for xv0 in range(R+1):
            for yv0 in range(D, -D):
                h = self.maxHeight(xv0, yv0)
                if h is not None:
                    heights.append(h)
        return max(heights)

    def isInTargetArea(self):
        L, R = self.xrange
        D, U = self.yrange
        return L <= self.xp <= R and D <= self.yp <= U

    def isTerminated(self):
        """
        Return if the probe has fallen through the bottom boundary
        of the target area.
        """
        D, _ = self.yrange
        return self.yp < D

    def getNumPossibleInitialVelocity(self):
        return len(self.possibleInitVs)


if __name__ == '__main__':
    submarine = TrickShot()
    print(submarine.search())

    print(submarine.getNumPossibleInitialVelocity())
