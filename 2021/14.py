from collections import Counter


def _parse_input(raw_input: list[str]):
    template = raw_input[0]
    rules = dict(line.split(" -> ") for line in raw_input[2:])
    return template, rules


def helper(template: str, rules: dict[str, str], nsteps: int) -> int:
    head, *_, tail = template
    counter = Counter(template[i:i+2] for i in range(len(template) - 1))

    for _ in range(nsteps):
        new_counter = Counter()
        for pair, n in counter.items():
            mid = rules[pair]
            new_counter[pair[0] + mid] += n
            new_counter[mid + pair[1]] += n
        counter = new_counter

    elems = Counter([head, tail])
    for pair, n in counter.items():
        elems[pair[0]] += n
        elems[pair[1]] += n
    counts = elems.values()
    return (max(counts) - min(counts)) // 2


def part1(raw_input: list[str]):
    template, rules = _parse_input(raw_input)
    return helper(template, rules, 10)


def part2(raw_input: list[str]):
    template, rules = _parse_input(raw_input)
    return helper(template, rules, 40)
