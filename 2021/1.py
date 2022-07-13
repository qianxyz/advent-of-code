from typing import List


def _parse_input(raw_input: List[str]):
    return [int(line) for line in raw_input]


def times_of_increase(nums: list[int], window_length: int = 1) -> int:
    return sum(x < y for x, y in zip(nums, nums[window_length:]))


def part1(raw_input: List[str]):
    meas = _parse_input(raw_input)
    return times_of_increase(meas)


def part2(raw_input: List[str]):
    meas = _parse_input(raw_input)
    return times_of_increase(meas, 3)

