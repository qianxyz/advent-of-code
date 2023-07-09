from typing import Iterator


class OctopusGrid:

    Position = tuple[int, int]

    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid

    def __iter__(self) -> Iterator[Position]:
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                yield x, y

    def __getitem__(self, index: Position) -> int:
        x, y = index
        return self.grid[x][y]

    def __setitem__(self, index: Position, value: int) -> None:
        x, y = index
        self.grid[x][y] = value

    def neighbors_of(self, p: Position) -> Iterator[Position]:
        x, y = p
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if (dx, dy) == (0, 0):
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]):
                    yield nx, ny


def step(grid: OctopusGrid) -> int:
    for p in grid:
        grid[p] += 1
    
    flashed = set()
    to_flash = [p for p in grid if grid[p] > 9]
    while to_flash:
        p = to_flash.pop()
        if p not in flashed:
            flashed.add(p)
            for n in grid.neighbors_of(p):
                grid[n] += 1
                if grid[n] > 9:
                    to_flash.append(n)

    for p in flashed:
        grid[p] = 0

    return len(flashed)


def _parse_input(raw_input: list[str]):
    return OctopusGrid([[int(n) for n in line] for line in raw_input])


def part1(raw_input: list[str]):
    grid = _parse_input(raw_input)
    return sum(step(grid) for _ in range(100))


def part2(raw_input: list[str]):
    grid = _parse_input(raw_input)
    ntotal = sum(1 for _ in grid)
    t = 1
    while step(grid) != ntotal:
        t += 1
    return t
