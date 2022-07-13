import itertools as it
import math


def _parse_input(raw_input: list[str]):
    return [int(line) for line in raw_input]


def adjacent_differences(nums: list[int]) -> list[int]:
    nums.sort()
    nums = [0] + nums + [nums[-1]+3]
    return [nums[i+1] - nums[i] for i in range(len(nums)-1)]


def sum_n_123(n: int) -> int:
    """Return the number of lists with sum n consisting of 1, 2, 3."""
    if n == 0 or n == 1:
        return 1
    if n == 2:
        return 2
    return sum_n_123(n-1) + sum_n_123(n-2) + sum_n_123(n-3)


def part1(raw_input: list[str]):
    nums = _parse_input(raw_input)
    diffs = adjacent_differences(nums)
    return diffs.count(1) * diffs.count(3)


def part2(raw_input: list[str]):
    nums = _parse_input(raw_input)
    diffs = adjacent_differences(nums)
    contiguous_ones = [len(list(y)) for x, y in
                       it.groupby(diffs, lambda z: z == 1) if x]
    return math.prod(sum_n_123(n) for n in contiguous_ones)
