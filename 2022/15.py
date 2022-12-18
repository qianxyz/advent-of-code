import re


def _parse_input(raw_input: list[str]):
    for line in raw_input:
        xs, ys, xb, yb = map(int, re.findall(r"=(-?\d+)", line))
        yield (xs, ys), (xb, yb)


def part1(raw_input: list[str]):
    input = _parse_input(raw_input)
    no_beacons = set()
    y_inspect = 2000000
    for (xs, ys), (xb, yb) in input:
        d = abs(xs - xb) + abs(ys - yb) - abs(y_inspect - ys)
        no_beacons.update(xs + x for x in range(-d, d+1))
        if y_inspect == yb:
            no_beacons.discard(xb)
    return len(no_beacons)


def part2(raw_input: list[str]):
    input = _parse_input(raw_input)
    xymax = 4000000

    # if the solution is unique, it must be surrounded by 4 edges
    edge_info = {
        "x+y>=": set(),
        "x+y<=": set(),
        "x-y>=": set(),
        "x-y<=": set(),
    }
    for (xs, ys), (xb, yb) in input:
        d = abs(xs - xb) + abs(ys - yb) + 1
        edge_info["x+y>="].add(xs + ys + d)
        edge_info["x+y<="].add(xs + ys - d)
        edge_info["x-y>="].add(xs - ys + d)
        edge_info["x-y<="].add(xs - ys - d)

    xpy = edge_info["x+y>="].intersection(edge_info["x+y<="]).pop()
    xmy = edge_info["x-y>="].intersection(edge_info["x-y<="]).pop()
    x, y = (xpy + xmy) // 2, (xpy - xmy) // 2
    return x * xymax + y
