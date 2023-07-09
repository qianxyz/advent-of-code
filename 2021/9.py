from typing import Iterator


class Heightmap:

    Position = tuple[int, int]

    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid

    def __iter__(self) -> Iterator[Position]:
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                yield x, y

    def __getitem__(self, index: Position) -> int:
        x, y = index
        # no boundary checks needed: 
        # `__iter__` and `neighbors_of` only yield valid positions
        return self.grid[x][y]

    def neighbors_of(self, p: Position) -> Iterator[Position]:
        x, y = p
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]):
                yield nx, ny


def _parse_input(raw_input: list[str]):
    return Heightmap([[int(n) for n in line] for line in raw_input])


def part1(raw_input: list[str]):
    hmap = _parse_input(raw_input)
    return sum(
        hmap[pos] + 1 for pos in hmap 
        if all(hmap[pos] < hmap[p] for p in hmap.neighbors_of(pos))
    )


def part2(raw_input: list[str]):
    hmap = _parse_input(raw_input)
    # get the sizes of connected components
    unvisited = set(p for p in hmap if hmap[p] < 9)
    areas = []
    while unvisited:
        stack = [unvisited.pop()]
        area = 0
        while stack:
            p = stack.pop()
            area += 1
            for n in hmap.neighbors_of(p):
                if n in unvisited:
                    unvisited.remove(n)
                    stack.append(n)
        areas.append(area)
    areas.sort()
    return areas[-1] * areas[-2] * areas[-3]
