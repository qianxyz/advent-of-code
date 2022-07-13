import itertools as it


def _parse_input(raw_input: list[str]):
    return [list(y) for x, y in it.groupby(raw_input, bool) if x]


def count_any(group: list[str]):
    group_set = [set(s) for s in group]
    return len(set.union(*group_set))


def count_every(group: list[str]):
    group_set = [set(s) for s in group]
    return len(set.intersection(*group_set))


def part1(raw_input: list[str]):
    groups = _parse_input(raw_input)
    return sum(count_any(group) for group in groups)


def part2(raw_input: list[str]):
    groups = _parse_input(raw_input)
    return sum(count_every(group) for group in groups)
