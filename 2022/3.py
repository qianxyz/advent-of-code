def _parse_input(raw_input: list[str]):
    return [line for line in raw_input]


def priority(c):
    if 'a' <= c <= 'z':
        return ord(c) - ord('a') + 1
    elif 'A' <= c <= 'Z':
        return ord(c) - ord('A') + 27
    else:
        raise ValueError


def part1(raw_input: list[str]):
    input = _parse_input(raw_input)
    return sum(priority(set.intersection(
        set(line[:len(line) // 2]),
        set(line[len(line) // 2:])
    ).pop()) for line in input)


def part2(raw_input: list[str]):
    input = _parse_input(raw_input)
    return sum(
        priority(set(l1).intersection(l2).intersection(l3).pop())
        for (l1, l2, l3) in [input[i:i+3] for i in range(0, len(input), 3)]
    )
