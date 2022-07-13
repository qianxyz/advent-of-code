from typing import List
import itertools as it


def _parse_input(raw_input: List[str]):
    depart, buses = raw_input
    buses = [None if bus == 'x' else int(bus) for bus in buses.split(',')]
    return int(depart), buses


def part1(raw_input: List[str]):
    depart, buses = _parse_input(raw_input)
    waits = [(-depart % bus, bus) for bus in buses if bus is not None]
    min_time, bus_id = min(waits)
    return min_time * bus_id


def part2(raw_input: List[str]):
    # Chinese remainder theorem
    _, buses = _parse_input(raw_input)
    nas = [(bus, -i % bus) for i, bus in enumerate(buses) if bus is not None]
    nas.sort(reverse=True)
    nn, aa = 1, 0
    for n, a in nas:
        for akn in it.count(start=aa, step=nn):
            if akn % n == a:
                break
        aa = akn
        nn *= n
    return aa
