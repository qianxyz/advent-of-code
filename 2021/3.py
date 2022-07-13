from collections import Counter


def _parse_input(raw_input: list[str]):
    return [line for line in raw_input]


def part1(raw_input: list[str]):
    input = _parse_input(raw_input)
    gamma = ['1' if digits.count('1') >= digits.count('0') else '0'
             for digits in zip(*input)]
    epsilon = ['1' if digits.count('1') < digits.count('0') else '0'
               for digits in zip(*input)]
    gamma = int(''.join(gamma), 2)
    epsilon = int(''.join(epsilon), 2)
    return gamma * epsilon


def filter(input: list[str], is_most_common=True):
    candidate = input
    for i, _ in enumerate(input[0]):
        c = Counter(s[i] for s in candidate)
        criteria = '1' if (c['1'] >= c['0']) == is_most_common else '0'
        if len(candidate) == 1:
            break
        candidate = [s for s in candidate if s[i] == criteria]
    return int(candidate[0], 2)


def part2(raw_input: list[str]):
    input = _parse_input(raw_input)
    o2 = filter(input)
    co2 = filter(input, is_most_common=False)
    return o2 * co2
