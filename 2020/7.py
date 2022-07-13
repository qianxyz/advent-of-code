from typing import Dict, List
import re
from collections import defaultdict


def _parse_input(raw_input: List[str]):
    for line in raw_input:
        m = re.match(r"(.*?) bags", line)
        assert m is not None
        outer = m.group(1)
        inners = re.findall(r"(\d+) (.*?) bag", line)
        inners = [(int(d), s) for d, s in inners]
        yield outer, inners


def bags_inside(outin: Dict, type: str) -> int:
    if not outin[type]:
        return 0
    return sum(n * (1 + bags_inside(outin, t)) for n, t in outin[type])


def part1(raw_input: List[str]):
    inout = defaultdict(list)
    for outer, inners in _parse_input(raw_input):
        for _, inner in inners:
            inout[inner].append(outer)

    closed = set()
    fringe = inout['shiny gold']
    while fringe:
        type = fringe.pop()
        closed.add(type)
        fringe += inout[type]
    return len(closed)


def part2(raw_input: List[str]):
    outin = {outer: inners for outer, inners in _parse_input(raw_input)}
    return bags_inside(outin, 'shiny gold')
