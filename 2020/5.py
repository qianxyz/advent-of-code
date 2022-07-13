from typing import List


def _parse_input(raw_input: List[str]):
    return [line for line in raw_input]


def seat_to_ID(seat: str):
    id = ['0' if c in "FL" else '1' for c in seat]
    return int(''.join(id), 2)


def part1(raw_input: List[str]):
    seats = _parse_input(raw_input)
    return max(seat_to_ID(seat) for seat in seats)


def part2(raw_input: List[str]):
    seats = _parse_input(raw_input)
    ids = [seat_to_ID(seat) for seat in seats]
    ids.sort()
    for i, n in enumerate(ids):
        if ids[i+1] == n + 2:
            return n + 1
