import heapq
from typing import Iterator


class Grid:

    Position = tuple[int, int]

    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid
        self.start = (0, 0)
        self.end = (len(grid) - 1, len(grid[0]) - 1)

    def __getitem__(self, index: Position) -> int:
        x, y = index
        return self.grid[x][y]

    def neighbors_of(self, p: Position) -> Iterator[Position]:
        x, y = p
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]):
                yield nx, ny


def bfs(grid: Grid) -> int:
    heap = [(0, grid.start)]
    visited = {grid.start}
    while heap:
        cost, position = heapq.heappop(heap)
        if position == grid.end:
            return cost
        for n in grid.neighbors_of(position):
            if n not in visited:
                visited.add(n)
                heapq.heappush(heap, (cost + grid[n], n))


def _parse_input(raw_input: list[str]):
    return [[int(n) for n in line] for line in raw_input]


def part1(raw_input: list[str]):
    grid = _parse_input(raw_input)
    grid = Grid(grid)
    return bfs(grid)


def part2(raw_input: list[str]):
    grid = _parse_input(raw_input)
    grid = [
        [
            (grid[x][y] + i + j - 1) % 9 + 1 
            for j in range(5) for y in range(len(grid[0]))
        ]
        for i in range(5) for x in range(len(grid))
    ]
    grid = Grid(grid)
    return bfs(grid)
