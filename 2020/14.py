from typing import List
import re
import itertools as it


def _parse_input(raw_input: List[str]):
    for line in raw_input:
        mask = re.match(r"mask = ([01X]{36})", line)
        if mask:
            yield mask.group(1)
        mem = re.match(r"mem\[(\d+)\] = (\d+)", line)
        if mem:
            address, value = mem.group(1, 2)
            yield int(address), int(value)


class Bitmask:

    def __init__(self, program) -> None:
        self.program = program
        self.mask = ""
        self.memory = dict()

    def mask_address(self, address):
        return [address]

    def mask_value(self, value):
        bin_val = f"{value:036b}"
        masked = [b if m == 'X' else m for m, b in zip(self.mask, bin_val)]
        return int(''.join(masked), 2)

    def run(self):
        for instruction in self.program:
            if isinstance(instruction, str):
                self.mask = instruction
            else:
                address, value = instruction
                for addr in self.mask_address(address):
                    self.memory[addr] = self.mask_value(value)

    def sum_memory(self):
        return sum(self.memory.values())


class BitmaskAlt(Bitmask):

    def mask_value(self, value):
        return value

    def mask_address(self, address):
        bin_addr = f"{address:036b}"
        maskeds = [[b] if m == '0' else ['1'] if m == '1' else ['0', '1']
                   for m, b in zip(self.mask, bin_addr)]
        for masked in it.product(*maskeds):
            yield int(''.join(masked), 2)


def part1(raw_input: List[str]):
    program = _parse_input(raw_input)
    bitmask = Bitmask(program)
    bitmask.run()
    return bitmask.sum_memory()


def part2(raw_input: List[str]):
    program = _parse_input(raw_input)
    bitmask = BitmaskAlt(program)
    bitmask.run()
    return bitmask.sum_memory()
