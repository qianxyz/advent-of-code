from typing import List


def _parse_input(raw_input: List[str]):
    return [line for line in raw_input]


def part1(raw_input: List[str]):
    input = _parse_input(raw_input)
    gamma = ['1' if digits.count('1') >= digits.count('0') else '0'
             for digits in zip(*input)]
    epsilon = ['1' if digits.count('1') < digits.count('0') else '0'
               for digits in zip(*input)]
    gamma = int(''.join(gamma), 2)
    epsilon = int(''.join(epsilon), 2)
    return gamma * epsilon


def part2(raw_input: List[str]):
    _ = _parse_input(raw_input)
    return NotImplemented
