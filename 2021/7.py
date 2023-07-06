def _parse_input(raw_input: list[str]):
    return [int(n) for n in raw_input[0].split(',')]


def part1(raw_input: list[str]):
    xs = _parse_input(raw_input)
    xs.sort()
    x0 = xs[len(xs) // 2]
    return sum(abs(x - x0) for x in xs)


def part2(raw_input: list[str]):
    xs = _parse_input(raw_input)
    return min(
        sum(abs(x - x0) * (abs(x - x0) + 1) // 2 for x in xs)
        for x0 in range(min(xs), max(xs))
    )
