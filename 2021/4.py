def _parse_input(raw_input: list[str]):
    draw = [int(d) for d in raw_input[0].split(',')]
    grids = [[[int(d) for d in line.split()] for line in raw_input[i:i+5]]
             for i in range(2, len(raw_input), 6)]
    return draw, grids


class Board:

    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid

    def mark(self, n: int):
        changes = []
        for i in range(5):
            for j in range(5):
                if self.grid[i][j] == n:
                    self.grid[i][j] = -1
                    changes.append((i, j))
        return changes

    def is_win(self, changes: list[tuple[int, int]]):
        for i, j in changes:
            if self.grid[i] == [-1] * 5:
                return True
            if [self.grid[ii][j] for ii in range(5)] == [-1] * 5:
                return True
        return False

    def score(self):
        return sum(self.grid[i][j] for i in range(5) for j in range(5)
                   if self.grid[i][j] > 0)


def part1(raw_input: list[str]):
    draw, grids = _parse_input(raw_input)
    boards = [Board(grid) for grid in grids]
    for n in draw:
        for board in boards:
            if board.is_win(board.mark(n)):
                return board.score() * n


def part2(raw_input: list[str]):
    draw, grids = _parse_input(raw_input)
    boards = [Board(grid) for grid in grids]
    last_score = 0
    for n in draw:
        boards_left = []
        for board in boards:
            if board.is_win(board.mark(n)):
                last_score = board.score()
            else:
                boards_left.append(board)
        boards = boards_left
        if not boards:
            return last_score * n
