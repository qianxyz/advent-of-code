import itertools as it


def _parse_input(raw_input: list[str]):
    return [line for line in raw_input]


class Cubes:

    def __init__(self, grid) -> None:
        self.actives = set((i, j, 0) for i, row in enumerate(grid)
                           for j, c in enumerate(row) if c == '#')

    def is_active(self, xyz):
        return xyz in self.actives

    def get_adjacents(self, xyz):
        x, y, z = xyz
        for dx, dy, dz in it.product(*[[-1, 0, 1]] * 3):
            if (dx, dy, dz) != (0, 0, 0):
                yield (x + dx, y + dy, z + dz)

    def active_adjacents(self, xyz):
        return sum(self.is_active(adj) for adj in self.get_adjacents(xyz))

    def relevant_positions(self):
        poss = set(self.actives)
        for xyz in self.actives:
            poss.update(self.get_adjacents(xyz))
        return poss

    def step(self):
        ons = set(xyz for xyz in self.relevant_positions()
                  if (not self.is_active(xyz)
                      and self.active_adjacents(xyz) == 3))
        offs = set(xyz for xyz in self.relevant_positions()
                   if (self.is_active(xyz)
                       and self.active_adjacents(xyz) not in [2, 3]))
        self.actives.update(ons)
        self.actives.difference_update(offs)

    def steps(self, n):
        for _ in range(n):
            self.step()

    def num_actives(self):
        return len(self.actives)


class Cubes4D(Cubes):

    def __init__(self, grid) -> None:
        self.actives = set((i, j, 0, 0) for i, row in enumerate(grid)
                           for j, c in enumerate(row) if c == '#')

    def get_adjacents(self, xyz):
        x, y, z, w = xyz
        for dx, dy, dz, dw in it.product(*[[-1, 0, 1]] * 4):
            if (dx, dy, dz, dw) != (0, 0, 0, 0):
                yield (x + dx, y + dy, z + dz, w + dw)


def part1(raw_input: list[str]):
    grid = _parse_input(raw_input)
    cubes = Cubes(grid)
    cubes.steps(6)
    return cubes.num_actives()


def part2(raw_input: list[str]):
    grid = _parse_input(raw_input)
    cubes = Cubes4D(grid)
    cubes.steps(6)
    return cubes.num_actives()
