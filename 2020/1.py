import itertools as it


def _parse_input(raw_input: list[str]):
    return [int(line) for line in raw_input]


def sum_k(nums: list[int], k=2, target=2020):
    for ns in it.combinations(nums, k):
        if sum(ns) == target:
            return ns
    assert False


def part1(raw_input: list[str]):
    nums = _parse_input(raw_input)
    n1, n2 = sum_k(nums)
    return n1 * n2


def part2(raw_input: list[str]):
    nums = _parse_input(raw_input)
    n1, n2, n3 = sum_k(nums, k=3)
    return n1 * n2 * n3
