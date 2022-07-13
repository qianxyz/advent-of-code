import math


def _parse_input(raw_input: list[str]):
    return [line for line in raw_input]


def count_tree(map: list[str], right=3, down=1):
    xmax, ymax = len(map), len(map[0])
    trail = [(down*t, (right*t) % ymax)
             for t in range(1, xmax) if down*t < xmax]
    return sum(map[x][y] == '#' for x, y in trail)


def part1(raw_input: list[str]):
    map = _parse_input(raw_input)
    return count_tree(map)


def part2(raw_input: list[str]):
    map = _parse_input(raw_input)
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    return math.prod(count_tree(map, r, d) for r, d in slopes)
