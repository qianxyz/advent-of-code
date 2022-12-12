import re, math
from dataclasses import dataclass


@dataclass
class Monkey:
    items: list[int]
    operation: str
    divisor: int
    throw_true: int
    throw_false: int
    inspects: int = 0

    def inspect(self, div3 = True) -> list[tuple[int, int]]:
        """Return a list of (monkey_id, worry_level)."""
        ret = []
        for item in self.items:
            scope = {"old": item}
            exec(self.operation, scope)
            worry_level = scope["new"]
            if div3:
                worry_level //= 3
            throw = (
                self.throw_true if worry_level % self.divisor == 0
                else self.throw_false
            )
            ret.append((throw, worry_level))
            self.inspects += 1
        self.items.clear()
        return ret


def _parse_input(raw_input: list[str]):
    pattern = re.compile(r"""Monkey (\d+):
  Starting items: (.*)$
  Operation: (.*)$
  Test: divisible by (\d+)
    If true: throw to monkey (\d+)
    If false: throw to monkey (\d+)""", re.MULTILINE)
    matches = re.findall(pattern, "\n".join(raw_input))

    monkeys: dict[int, Monkey] = dict()
    for id, items, operation, divisor, throw_true, throw_false in matches:
        monkeys[int(id)] = Monkey(
            list(map(int, items.split(", "))),
            operation, int(divisor), int(throw_true), int(throw_false)
        )
    return monkeys


def part1(raw_input: list[str]):
    monkeys = _parse_input(raw_input)
    for _ in range(20):
        for monkey in monkeys.values():
            throws = monkey.inspect()
            for id, worry_level in throws:
                monkeys[id].items.append(worry_level)
    inspects = sorted(monkey.inspects for monkey in monkeys.values())
    return inspects[-1] * inspects[-2]


def part2(raw_input: list[str]):
    monkeys = _parse_input(raw_input)
    lcm = math.prod(monkey.divisor for monkey in monkeys.values())
    for _ in range(10000):
        for monkey in monkeys.values():
            throws = monkey.inspect(div3=False)
            for id, worry_level in throws:
                monkeys[id].items.append(worry_level % lcm)
    inspects = sorted(monkey.inspects for monkey in monkeys.values())
    return inspects[-1] * inspects[-2]
