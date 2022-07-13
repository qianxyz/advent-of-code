def _parse_input(raw_input: list[str]):
    draw = [int(d) for d in raw_input[0].split(',')]
    grids = [[[int(d) for d in line.split()] for line in raw_input[i:i+5]]
             for i in range(2, len(raw_input), 6)]
    return draw, grids


class Board:

    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid


def part1(raw_input: list[str]):
    _ = _parse_input(raw_input)
    return NotImplemented


def part2(raw_input: list[str]):
    _ = _parse_input(raw_input)
    return NotImplemented
