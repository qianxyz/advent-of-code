import re


def _parse_input(raw_input: list[str]):
    points, folds = set(), []
    for line in raw_input:
        if (m := re.match(r"(\d+),(\d+)", line)) is not None:
            x, y = m.groups()
            points.add((int(x), int(y)))
        elif (m := re.match(r"fold along (x|y)=(\d+)", line)) is not None:
            axis, v = m.groups()
            folds.append((axis, int(v)))
    return points, folds


Point = tuple[int, int]
Fold = tuple[str, int]


def fold(p: Point, f: Fold) -> Point:
    (x, y), (axis, n) = p, f
    match axis:
        case 'x': return (x if x <= n else 2 * n - x, y)
        case 'y': return (x, y if y <= n else 2 * n - y)
        case _: assert False


def part1(raw_input: list[str]):
    points, folds = _parse_input(raw_input)
    return len({fold(p, folds[0]) for p in points})


def part2(raw_input: list[str]):
    points, folds = _parse_input(raw_input)
    for f in folds:
        points = {fold(p, f) for p in points}
    
    # print the grid
    for y in range(max(y for _, y in points) + 1):
        for x in range(max(x for x, _ in points) + 1):
            print('#' if (x, y) in points else '.', end="")
        print("")
