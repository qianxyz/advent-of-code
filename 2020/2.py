import re


def _parse_input(raw_input: list[str]):
    for line in raw_input:
        mo = re.search(r"(\d+)-(\d+) (\w): (\w+)", line)
        assert mo is not None
        n0, n1, char, s = mo.groups()
        yield int(n0), int(n1), char, s


def part1(raw_input: list[str]):
    return sum(n0 <= s.count(char) <= n1
               for n0, n1, char, s in _parse_input(raw_input))


def part2(raw_input: list[str]):
    return sum((s[n0-1] == char) ^ (s[n1-1] == char)
               for n0, n1, char, s in _parse_input(raw_input))
