from typing import List


def _parse_input(raw_input: List[str]):
    return [list(line) for line in raw_input]


class SeatGrid:

    def __init__(self, grid) -> None:
        self.grid = grid
        self.xmax = len(grid)
        self.ymax = len(grid[0])
        self.xys = [(x, y) for x in range(self.xmax) for y in range(self.ymax)]

    def get_grid(self, xy):
        x, y = xy
        return self.grid[x][y]

    def set_grid(self, xy, c):
        x, y = xy
        self.grid[x][y] = c

    def is_valid_xy(self, xy):
        x, y = xy
        return 0 <= x < self.xmax and 0 <= y < self.ymax

    def get_adjacents(self, xy):
        directions = [(dx, dy) for dx in [-1, 0, 1]
                      for dy in [-1, 0, 1] if dx or dy]
        x, y = xy
        for dx, dy in directions:
            newxy = (x + dx, y + dy)
            if self.is_valid_xy(newxy):
                yield newxy

    def adjacent_occupied(self, xy) -> int:
        return sum(self.get_grid(newxy) == '#'
                   for newxy in self.get_adjacents(xy))

    def step(self, tolerance=4):
        to_occupy = [xy for xy in self.xys
                     if self.get_grid(xy) == 'L'
                     and self.adjacent_occupied(xy) == 0]
        to_empty = [xy for xy in self.xys
                    if self.get_grid(xy) == '#'
                    and self.adjacent_occupied(xy) >= tolerance]
        for xy in to_occupy:
            self.set_grid(xy, '#')
        for xy in to_empty:
            self.set_grid(xy, 'L')
        return not to_occupy and not to_empty  # True iff stable

    def count_occupied(self):
        return sum(self.get_grid(xy) == '#' for xy in self.xys)

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.grid])


class SeatGridVisible(SeatGrid):

    def get_adjacents(self, xy):
        directions = [(dx, dy) for dx in [-1, 0, 1]
                      for dy in [-1, 0, 1] if dx or dy]
        x, y = xy
        for dx, dy in directions:
            newxy = (x + dx, y + dy)
            while self.is_valid_xy(newxy) and self.get_grid(newxy) == '.':
                newx, newy = newxy
                newxy = (newx + dx, newy + dy)
            if self.is_valid_xy(newxy):
                yield newxy


def part1(raw_input: List[str]):
    grid = _parse_input(raw_input)
    seats = SeatGrid(grid)
    while not seats.step():
        continue
    return seats.count_occupied()


def part2(raw_input: List[str]):
    grid = _parse_input(raw_input)
    seats = SeatGridVisible(grid)
    while not seats.step(tolerance=5):
        continue
    return seats.count_occupied()
