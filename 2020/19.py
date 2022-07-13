from typing import List
import itertools as it


def _parse_input(raw_input: List[str]):
    rules = dict()
    msgs = []
    for line in raw_input:
        if ':' in line:
            key, vals = line.split(': ')
            rules[int(key)] = vals[1:-1] if '"' in vals else [
                [int(n) for n in v.split()] for v in vals.split('|')]
        elif line:
            msgs.append(line)
    return rules, msgs


class StringMatching:

    def __init__(self, rules) -> None:
        self.rules = rules

    def matching_strs(self, rule_no: int):
        pattern = self.rules[rule_no]
        if isinstance(pattern, str):
            return {pattern}
        strs = set()
        for pat in pattern:
            strs.update("".join(ss) for ss in it.product(
                *[self.matching_strs(n) for n in pat]))
        return strs


def part1(raw_input: List[str]):
    rules, msgs = _parse_input(raw_input)
    matchings = StringMatching(rules).matching_strs(0)
    return sum(msg in matchings for msg in msgs)


def part2(raw_input: List[str]):
    rules, msgs = _parse_input(raw_input)
    strmatch = StringMatching(rules)
    pres = strmatch.matching_strs(42)
    posts = strmatch.matching_strs(31)
    matches = 0
    for msg in msgs:
        chunks = list(msg[i:i+8] for i in range(0, len(msg), 8))
        i = 0
        for i, chunk in enumerate(chunks):
            if chunk not in pres:
                break
        matches += (i > len(chunks) / 2 and
                    all(chunk in posts for chunk in chunks[i:]))
    return matches
