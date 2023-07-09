from dataclasses import dataclass
from math import prod


@dataclass
class Packet:
    version: int
    type_id: int
    data: int | list["Packet"]

    def sum_version(self) -> int:
        if isinstance(self.data, int):
            return self.version
        else:
            return self.version + sum(p.sum_version() for p in self.data)

    def eval(self) -> int:
        if isinstance(self.data, int):
            return self.data
        match self.type_id:
            case 0: return sum(p.eval() for p in self.data)
            case 1: return prod(p.eval() for p in self.data)
            case 2: return min(p.eval() for p in self.data)
            case 3: return max(p.eval() for p in self.data)
            case 5: return int(self.data[0].eval() > self.data[1].eval())
            case 6: return int(self.data[0].eval() < self.data[1].eval())
            case 7: return int(self.data[0].eval() == self.data[1].eval())
        assert False


class Parser:

    def __init__(self, s: str) -> None:
        self.s = s
        self.pp = 0  # parse point

    def advance(self, n: int) -> int:
        p = self.pp
        self.pp += n
        return int(self.s[p:self.pp], base=2)

    def parse(self) -> Packet:
        version = self.advance(3)
        type_id = self.advance(3)
        if type_id == 4:
            data = 0
            while True:
                v = self.advance(5)
                data = (data << 4) + (v & 0xF)
                if not v & (1 << 4):
                    break
        else:
            data = []
            if self.advance(1):
                nsub = self.advance(11)
                for _ in range(nsub):
                    data.append(self.parse())
            else:
                length = self.advance(15)
                curr = self.pp
                while self.pp - curr < length:
                    data.append(self.parse())
        return Packet(version, type_id, data)


def _parse_input(raw_input: list[str]):
    s = ''.join(format(int(d, 16), '0>4b') for d in raw_input[0])
    return Parser(s).parse()


def part1(raw_input: list[str]):
    packet = _parse_input(raw_input)
    return packet.sum_version()


def part2(raw_input: list[str]):
    packet = _parse_input(raw_input)
    return packet.eval()
