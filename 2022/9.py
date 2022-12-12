def _parse_input(raw_input: list[str]):
    return "".join(l.split()[0] * int(l.split()[1]) for l in raw_input)


class Rope:
    def __init__(self, knots: int = 2) -> None:
        self.knots = [[0, 0] for _ in range(knots)]
        self.tail_visited = set()

    def step(self, direction: str):
        # move head
        head = self.knots[0]
        match direction:
            case 'U': head[1] += 1
            case 'D': head[1] -= 1
            case 'L': head[0] -= 1
            case 'R': head[0] += 1

        # knot follows
        for i, knot in enumerate(self.knots[1:]):
            dx, dy = self.knots[i][0] - knot[0], self.knots[i][1] - knot[1]
            if abs(dx) <= 1 and abs(dy) <= 1:
                continue
            knot[0] += 1 if dx > 0 else 0 if dx == 0 else -1
            knot[1] += 1 if dy > 0 else 0 if dy == 0 else -1

        # register the new tail position
        self.tail_visited.add(tuple(self.knots[-1]))


def part1(raw_input: list[str]):
    input = _parse_input(raw_input)
    rope = Rope()
    for direction in input:
        rope.step(direction)
    return len(rope.tail_visited)


def part2(raw_input: list[str]):
    input = _parse_input(raw_input)
    rope = Rope(10)
    for direction in input:
        rope.step(direction)
    return len(rope.tail_visited)
