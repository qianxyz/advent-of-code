from typing import Iterator
from collections import deque


Position = tuple[int, int]
State = tuple[Position, int]


class Search:
    def __init__(self, grid: list[str]) -> None:
        self.grid = grid

    @staticmethod
    def elevation(c: str) -> int:
        match c:
            case 'S': return ord('a')
            case 'E': return ord('z')
            case c: return ord(c)

    def start_state(self) -> State:
        for i, row in enumerate(self.grid):
            for j, c in enumerate(row):
                if c == 'S':
                    return ((i, j), 0)
        raise ValueError

    def start_states(self) -> Iterator[State]:
        for i, row in enumerate(self.grid):
            for j, c in enumerate(row):
                if c == 'S' or c == 'a':
                    yield ((i, j), 0)

    def is_end_state(self, state: State) -> bool:
        (i, j), _ = state
        return self.grid[i][j] == 'E'

    def child_states(self, state: State) -> Iterator[State]:
        (i, j), cost = state
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            i1, j1 = i + di, j + dj
            if 0 <= i1 < len(self.grid) and 0 <= j1 < len(self.grid[0]):
                c, c1 = self.grid[i][j], self.grid[i1][j1]
                if self.elevation(c1) - self.elevation(c) <= 1:
                    yield ((i1, j1), cost + 1)

    def bfs(self, start: State) -> int:
        queue = deque()
        visited: set[Position] = set()
        visited.add(start[0])
        queue.append(start)
        while queue:
            state = queue.popleft()
            if self.is_end_state(state):
                return state[1]
            for child in self.child_states(state):
                if child[0] not in visited:
                    visited.add(child[0])
                    queue.append(child)
        raise ValueError


def _parse_input(raw_input: list[str]):
    return Search(raw_input)


def part1(raw_input: list[str]):
    search = _parse_input(raw_input)
    start = search.start_state()
    return search.bfs(start)


def part2(raw_input: list[str]):
    search = _parse_input(raw_input)
    starts = search.start_states()
    best = float("inf")
    for start in starts:
        try:
            best = min(best, search.bfs(start))
        except ValueError:
            continue
    return best
