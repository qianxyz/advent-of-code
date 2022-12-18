import itertools as it


Position = tuple[int, int]


def _parse_input(raw_input: list[str]):
    for line in raw_input:
        yield [tuple(map(int, pair.split(","))) for pair in line.split(" -> ")]


def line_segment(start: Position, end: Position) -> list[Position]:
    (x1, y1), (x2, y2) = start, end
    if x1 == x2:
        return [(x1, y) for y in range(min(y1, y2), max(y1, y2) + 1)]
    elif y1 == y2:
        return [(x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)]
    else:
        raise ValueError


class Frame:
    def __init__(self, points: list[list[Position]]) -> None:
        self.source: Position = (500, 0)
        self.rocks: set[Position] = set()
        for line in points:
            for start, end in it.pairwise(line):
                self.rocks.update(line_segment(start, end))

        self.sands: set[Position] = set()
        self.depth = max(y for _, y in self.rocks)

    def fall_sand(self) -> Position | None:
        sand = self.source
        while sand[1] < self.depth + 1:
            below = (sand[0], sand[1] + 1)
            downleft = (sand[0] - 1, sand[1] + 1)
            downright = (sand[0] + 1, sand[1] + 1)
            if below not in self.rocks.union(self.sands):
                sand = below
            elif downleft not in self.rocks.union(self.sands):
                sand = downleft
            elif downright not in self.rocks.union(self.sands):
                sand = downright
            else:
                self.sands.add(sand)
                return sand

    def sand_capacity_with_bottom(self) -> int:
        count = 0
        curr_sands = set()
        next_sands = set()
        curr_sands.add(self.source)
        for _ in range(self.depth + 2):
            for x, y in curr_sands:
                for dx in [-1, 0, 1]:
                    support = (x + dx, y + 1)
                    if support not in self.rocks:
                        next_sands.add(support)
            count += len(curr_sands)
            curr_sands = next_sands
            next_sands = set()
        return count


def part1(raw_input: list[str]):
    input = _parse_input(raw_input)
    frame = Frame(list(input))
    count = 0
    while frame.fall_sand() is not None:
        count += 1
    return count


def part2(raw_input: list[str]):
    input = _parse_input(raw_input)
    frame = Frame(list(input))
    return frame.sand_capacity_with_bottom()
