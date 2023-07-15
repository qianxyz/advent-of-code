import re
from dataclasses import dataclass


@dataclass
class TargetArea:
    xmin: int
    xmax: int
    ymin: int
    ymax: int

    def __contains__(self, point: tuple[int, int]) -> bool:
        x, y = point
        return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax


def pass_target(vx: int, vy: int, ta: TargetArea) -> bool:
    px = py = 0
    while py >= ta.ymin:
        if (px, py) in ta:
            return True
        px += vx
        py += vy
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1
    return False


def _parse_input(raw_input: list[str]):
    assert (match := re.match(
        r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", raw_input[0]
    )) is not None
    return TargetArea(*map(int, match.groups()))


def part1(raw_input: list[str]):
    ta = _parse_input(raw_input)
    for vy in range(-ta.ymin, ta.ymin - 1, -1):
        for vx in range(ta.xmax + 1):
            if pass_target(vx, vy, ta):
                return vy * (vy + 1) // 2


def part2(raw_input: list[str]):
    ta = _parse_input(raw_input)
    return sum(
        1 
        for vy in range(-ta.ymin, ta.ymin - 1, -1)
        for vx in range(ta.xmax + 1) 
        if pass_target(vx, vy, ta)
    )
