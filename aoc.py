import os
import sys
import time
import requests
import argparse
import importlib
import shutil
from typing import List, Tuple, Callable

_TEMPLATE = "_template.py"
_SESSION = ".session"
_YEARS = range(2015, 2030)
_DAYS = range(1, 26)


def get_session():
    try:
        with open(_SESSION) as f:
            return f.read()
    except FileNotFoundError:
        session = input("Enter your session number:\n")
        with open(_SESSION, 'w') as f:
            f.write(session)
        return session


def get_raw_input(year: int, day: int) -> List[str]:
    local = os.path.join(f"{year}", "inputs", f"{day}.txt")

    if not os.path.exists(local):
        url = f"https://adventofcode.com/{year}/day/{day}/input"
        print(f"Local input file {local} not found.")
        print(f"Getting input from {url} ...")
        with requests.get(url, cookies={"session": get_session()}) as response:
            response.raise_for_status()  # raise HTTPError except for 200
            os.makedirs(os.path.dirname(local), exist_ok=True)
            with open(local, 'w') as f:
                f.write(response.text)
        print(f"Input file saved at {local}")

    with open(local) as f:
        return [line.rstrip('\n') for line in f.readlines()]


def get_solution(year: int, day: int) -> Tuple[Callable, Callable]:
    script = os.path.join(f"{year}", f"{day}.py")

    if not os.path.exists(script):
        print(f"Solution {script} not found. Copying from {_TEMPLATE} ...")
        os.makedirs(os.path.dirname(script), exist_ok=True)
        shutil.copy(_TEMPLATE, script)
        print("Code template created. Happy Coding!")
        sys.exit()

    module = importlib.import_module(f"{year}.{day}")
    part1 = getattr(module, "part1")
    part2 = getattr(module, "part2")
    return part1, part2


def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int, choices=_YEARS, metavar="year",
                        help="Allowed values from 2015 to 2029.")
    parser.add_argument("day", type=int, choices=_DAYS, metavar="day",
                        help="Allowed values from 1 to 25.")
    args = parser.parse_args()
    return args


def main():
    args = parse_arg()
    raw_input = get_raw_input(**vars(args))
    part1, part2 = get_solution(**vars(args))

    start = time.perf_counter()
    ans1 = part1(raw_input)
    elapsed = time.perf_counter() - start
    print(f"Part 1 answer: {ans1}")
    print(f"Part 1 time: {elapsed:.2f}s")

    start = time.perf_counter()
    ans2 = part2(raw_input)
    elapsed = time.perf_counter() - start
    print(f"Part 2 answer: {ans2}")
    print(f"Part 2 time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
