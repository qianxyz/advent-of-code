def _parse_input(raw_input: list[str]):
    for line in raw_input:
        patterns, output = line.split(' | ')
        patterns = patterns.split()
        output = output.split()
        yield patterns, output


def part1(raw_input: list[str]):
    entries = _parse_input(raw_input)
    return sum(
        1 for _, output in entries for s in output if len(s) in (2, 3, 4, 7)
    )


def decode(segments: str, patterns: list[str]) -> int:
    match len(segments):
        case 2: return 1
        case 3: return 7
        case 4: return 4
        case 7: return 8
        case 5:  # 2, 3, 5
            s1 = next(s for s in patterns if len(s) == 2)
            s4 = next(s for s in patterns if len(s) == 4)
            match len(set(s1) & set(segments)), len(set(s4) & set(segments)):
                case 1, 2: return 2
                case 2, 3: return 3
                case 1, 3: return 5
        case 6:  # 0, 6, 9
            s1 = next(s for s in patterns if len(s) == 2)
            s4 = next(s for s in patterns if len(s) == 4)
            match len(set(s1) & set(segments)), len(set(s4) & set(segments)):
                case 2, 3: return 0
                case 1, 3: return 6
                case 2, 4: return 9
    assert False


def part2(raw_input: list[str]):
    entries = _parse_input(raw_input)
    return sum(
        int("".join(str(decode(s, patterns)) for s in output))
        for patterns, output in entries
    )
