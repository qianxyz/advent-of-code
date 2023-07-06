import re
from collections import Counter


def _parse_input(raw_input: list[str]):
    for line in raw_input:
        match = re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line)
        if match:
            x1, y1, x2, y2 = map(int, match.groups())
            yield (x1, y1), (x2, y2)


Point = tuple[int, int]


def is_along_axis(p1: Point, p2: Point) -> bool:
    return p1[0] == p2[0] or p1[1] == p2[1]


def points_on_line(p1: Point, p2: Point) -> list[Point]:
    if p1 > p2:  # lexicographical order
        p1, p2 = p2, p1
    (x1, y1), (x2, y2) = p1, p2
    if x1 == x2:
        return [(x1, y) for y in range(y1, y2 + 1)]
    elif y1 == y2:
        return [(x, y1) for x in range(x1, x2 + 1)]
    elif y1 < y2:
        return [(x1 + d, y1 + d) for d in range(x2 - x1 + 1)]
    else:
        return [(x1 + d, y1 - d) for d in range(x2 - x1 + 1)]


def part1(raw_input: list[str]):
    pairs = _parse_input(raw_input)
    c = Counter()
    for p1, p2 in pairs:
        if is_along_axis(p1, p2):
            c.update(points_on_line(p1, p2))
    return sum(1 for v in c.values() if v >= 2)


def part2(raw_input: list[str]):
    pairs = _parse_input(raw_input)
    c = Counter()
    for p1, p2 in pairs:
        c.update(points_on_line(p1, p2))
    return sum(1 for v in c.values() if v >= 2)
