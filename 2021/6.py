def _parse_input(raw_input: list[str]):
    count = [0] * 9
    for n in raw_input[0].split(','):
        count[int(n)] += 1
    return count


def step(ndays: int, count: list[int]) -> None:
    for _ in range(ndays):
        count[:-1], count[-1] = count[1:], count[0]  # rotate list
        count[6] += count[-1]


def part1(raw_input: list[str]):
    count = _parse_input(raw_input)
    step(80, count)
    return sum(count)


def part2(raw_input: list[str]):
    count = _parse_input(raw_input)
    step(256, count)
    return sum(count)
