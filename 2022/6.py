def _parse_input(raw_input: list[str]):
    return raw_input[0]


def helper(s: str, n: int) -> int:
    for i in range(n, len(s)):
        if len(set(s[i-n:i])) == n:
            return i
    return -1


def part1(raw_input: list[str]):
    input = _parse_input(raw_input)
    return helper(input, 4)


def part2(raw_input: list[str]):
    input = _parse_input(raw_input)
    return helper(input, 14)
