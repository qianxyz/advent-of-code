from typing import List, Dict
import re
import itertools as it


def _parse_input(raw_input: List[str]):
    spl = [' '.join(y) for x, y in it.groupby(raw_input, bool) if x]
    for entry in spl:
        yield {k: v for k, v in re.findall(r"(\S+):(\S+)", entry)}


def is_valid1(pp: Dict):
    fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    return fields.issubset(pp.keys())


def is_valid2(pp: Dict):
    return (is_valid1(pp)
            and pp["byr"] in [str(y) for y in range(1920, 2003)]
            and pp["iyr"] in [str(y) for y in range(2010, 2021)]
            and pp["eyr"] in [str(y) for y in range(2020, 2031)]
            and pp["hgt"] in ([f"{h}cm" for h in range(150, 194)]
                              + [f"{h}in" for h in range(59, 77)])
            and re.fullmatch(r"#[0-9a-f]{6}", pp["hcl"]) is not None
            and pp["ecl"] in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
            and re.fullmatch(r"\d{9}", pp["pid"]) is not None)


def part1(raw_input: List[str]):
    pps = _parse_input(raw_input)
    return sum(is_valid1(pp) for pp in pps)


def part2(raw_input: List[str]):
    pps = _parse_input(raw_input)
    return sum(is_valid2(pp) for pp in pps)
