from typing import List


def _parse_input(raw_input: List[str]):
    return [int(d) for d in raw_input[0].split(',')]


def part1(raw_input: List[str]):
    nums = _parse_input(raw_input)
    while len(nums) < 2020:
        occ = [i for i, n in enumerate(nums) if n == nums[-1]]
        if len(occ) == 1:
            nums.append(0)
        else:
            nums.append(occ[-1] - occ[-2])
    return nums[-1]


def part2(raw_input: List[str]):
    nums = _parse_input(raw_input)
    fst_occ = {n: i for i, n in enumerate(nums)}
    snd_occ = dict()
    last = nums[-1]
    count = len(nums)
    while count < 30000000:
        last = snd_occ[last] - fst_occ[last] if last in snd_occ else 0
        if last in snd_occ:
            fst_occ[last], snd_occ[last] = snd_occ[last], count
        elif last in fst_occ:
            snd_occ[last] = count
        else:
            fst_occ[last] = count
        count += 1
    return last
