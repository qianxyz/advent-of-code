def _parse_input(raw_input: list[str]):
    for line in raw_input:
        a, x = line.split()
        yield ord(a) - ord("A"), ord(x) - ord("W")


def part1(raw_input: list[str]):
    input = _parse_input(raw_input)
    return sum((o - t) % 3 * 3 + o for t, o in input)


def part2(raw_input: list[str]):
    input = _parse_input(raw_input)
    return sum((t + o + 1) % 3 + 1 + 3 * (o - 1) for t, o in input)
