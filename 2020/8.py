from typing import List


def _parse_input(raw_input: List[str]):
    return [(line.split()[0], int(line.split()[1]))
            for line in raw_input]


def run(instructions):
    ptr, acc = 0, 0
    visited = set()
    try:
        while ptr not in visited:
            visited.add(ptr)
            op, d = instructions[ptr]
            ptr += d if op == "jmp" else 1
            acc += d if op == "acc" else 0
        return False, acc
    except IndexError:
        return True, acc


def alt_instructions(instructions):
    for i, (op, d) in enumerate(instructions):
        if op == "nop":
            yield instructions[:i] + [("jmp", d)] + instructions[i+1:]
        elif op == "jmp":
            yield instructions[:i] + [("nop", d)] + instructions[i+1:]


def part1(raw_input: List[str]):
    instructions = _parse_input(raw_input)
    _, acc = run(instructions)
    return acc


def part2(raw_input: List[str]):
    instructions = _parse_input(raw_input)
    for alt_instrs in alt_instructions(instructions):
        is_terminated, acc = run(alt_instrs)
        if is_terminated:
            return acc
