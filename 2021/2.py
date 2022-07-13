from typing import List


def _parse_input(raw_input: List[str]):
    for line in raw_input:
        op, x = line.split()
        yield op, int(x)


def part1(raw_input: List[str]):
    commands = _parse_input(raw_input)
    horizontal_position = depth = 0
    for op, x in commands:
        if op == "forward":
            horizontal_position += x
        elif op == "down":
            depth += x
        elif op == "up":
            depth -= x
    return horizontal_position * depth


def part2(raw_input: List[str]):
    commands = _parse_input(raw_input)
    horizontal_position = depth = aim = 0
    for op, x in commands:
        if op == "forward":
            horizontal_position += x
            depth += aim * x
        elif op == "down":
            aim += x
        elif op == "up":
            aim -= x
    return horizontal_position * depth

