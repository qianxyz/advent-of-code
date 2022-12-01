import itertools as it
import heapq


def _parse_input(raw_input: list[str]):
    return [list(map(int, y)) for x, y in it.groupby(raw_input, bool) if x]


def part1(raw_input: list[str]):
    input = _parse_input(raw_input)
    return max(sum(xs) for xs in input)


def part2(raw_input: list[str]):
    input = _parse_input(raw_input)
    return sum(heapq.nlargest(3, (sum(xs) for xs in input)))
