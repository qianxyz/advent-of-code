from util import Submarine
import re
import itertools as it
from time import perf_counter


class ReactorReboot(Submarine):

    def _parseLine(self, line):
        onoff, cuboid = line.split()
        onoff = True if onoff == 'on' else False
        cuboid = [int(n) for n in re.findall(r'-?\d+', cuboid)]
        x0, x1, y0, y1, z0, z1 = cuboid
        return onoff, ((x0, x1+1), (y0, y1+1), (z0, z1+1))

    def __init__(self, isFullReboot=False):
        self.steps = self.getInput()
        if not isFullReboot:
            self.steps = self.steps[:20]

    def reboot(self):
        start = perf_counter()

        # create partition
        print('Initializing chunk partition ...')
        xs, ys, zs = [], [], []
        for _, ((x0, x1), (y0, y1), (z0, z1)) in self.steps:
            xs += [x0, x1]
            ys += [y0, y1]
            zs += [z0, z1]
        xs.sort()
        ys.sort()
        zs.sort()
        N = len(xs)
        chunkGrid = [[[False]*N for _ in range(N)] for _ in range(N)]

        # carry out steps
        ons = 0
        for i, (onoff, cuboid) in enumerate(self.steps):
            print(f'Step {i}, {"on" if onoff else "off"}, {cuboid}')
            (x0, x1), (y0, y1), (z0, z1) = cuboid
            xi0 = xs.index(x0)
            xi1 = xs.index(x1)
            yi0 = ys.index(y0)
            yi1 = ys.index(y1)
            zi0 = zs.index(z0)
            zi1 = zs.index(z1)
            for xi, yi, zi in it.product(range(xi0, xi1),
                                         range(yi0, yi1),
                                         range(zi0, zi1)):
                if chunkGrid[xi][yi][zi] ^ onoff:
                    ons += ((xs[xi+1] - xs[xi])
                            * (ys[yi+1] - ys[yi])
                            * (zs[zi+1] - zs[zi])
                            * (1 if onoff else -1))
                chunkGrid[xi][yi][zi] = onoff

        print(f'No. of lit cubes: {ons}')

        end = perf_counter()
        print(f'Time: {end-start}')
        return ons


if __name__ == '__main__':
    submarine = ReactorReboot()
    submarine.reboot()

    submarine = ReactorReboot(isFullReboot=True)
    submarine.reboot()
