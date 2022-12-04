import re


def _parse_input(raw_input: list[str]):
    return [list(map(int, re.findall(r"\d+", line))) for line in raw_input]


def part1(raw_input: list[str]):
    input = _parse_input(raw_input)
    return sum(a <= c <= d <= b or c <= a <= b <= d for a, b, c, d in input)


def part2(raw_input: list[str]):
    input = _parse_input(raw_input)
    return sum(not(b < c or d < a) for a, b, c, d in input)
