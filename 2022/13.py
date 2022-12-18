class Packet:
    def __init__(self, data: list | int) -> None:
        if isinstance(data, int):
            self.data = data
        elif isinstance(data, list):
            self.data = [Packet(d) for d in data]
        else:
            raise TypeError

    def __eq__(self, other: "Packet") -> bool:
        if self.data == other.data:
            return True
        elif isinstance(self.data, int) and isinstance(other.data, list):
            return Packet([self.data]) == other
        elif isinstance(self.data, list) and isinstance(other.data, int):
            return Packet([other.data]) == self
        else:
            return False

    def __lt__(self, other: "Packet") -> bool:
        d1, d2 = self.data, other.data
        if isinstance(d1, int) and isinstance(d2, int):
            return d1 < d2
        elif isinstance(d1, list) and isinstance(d2, list):
            for p1, p2 in zip(d1, d2):
                if p1 == p2:
                    continue
                else:
                    return p1 < p2
            return len(d1) < len(d2)
        elif isinstance(d1, int) and isinstance(d2, list):
            return Packet([d1]) < other
        else:  # d1 is list, d2 is int
            return self < Packet([d2])

    def __repr__(self) -> str:
        return self.data.__repr__()

def _parse_input(raw_input: list[str]):
    return [Packet(eval(l)) for l in raw_input if l]


def part1(raw_input: list[str]):
    packets = _parse_input(raw_input)
    return sum(
        i // 2 + 1 for i in range(0, len(packets), 2)
        if packets[i] < packets[i+1]
    )


def part2(raw_input: list[str]):
    packets = _parse_input(raw_input)
    div1, div2 = Packet([[2]]), Packet([[6]])
    packets += [div1, div2]
    packets.sort()
    # for p in packets: print(p)
    return (packets.index(div1) + 1) * (packets.index(div2) + 1)
