import re


def _parse_input(raw_input: list[str]):
    part = raw_input.index("")  # the position of the dividing line
    stacks = {
        int(col[0]): [c for c in col[1:] if c != ' ']
        for col in zip(*raw_input[part-1::-1]) if col[0] != ' '
    }
    moves = [list(map(int, re.findall("\d+", l))) for l in raw_input[part+1:]]
    return stacks, moves



def part1(raw_input: list[str]):
    stacks, moves = _parse_input(raw_input)
    for n, frm, to in moves:
        for _ in range(n):
            stacks[to].append(stacks[frm].pop())
    return "".join(v.pop() for v in stacks.values())


def part2(raw_input: list[str]):
    stacks, moves = _parse_input(raw_input)
    for n, frm, to in moves:
        stacks[to] += stacks[frm][-n:]
        del stacks[frm][-n:]
    return "".join(v.pop() for v in stacks.values())
