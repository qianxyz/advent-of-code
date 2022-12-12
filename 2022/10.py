def _parse_input(raw_input: list[str]):
    return [
        int(line.split()[1]) if line.startswith("addx") else None
        for line in raw_input
    ]


def part1(raw_input: list[str]):
    input = _parse_input(raw_input)
    nums = [1, 1]
    for n in input:
        nums.append(nums[-1])
        if n is not None:
            nums.append(nums[-1] + n)
    return sum(i * nums[i] for i in [20, 60, 100, 140, 180, 220])


def part2(raw_input: list[str]):
    input = _parse_input(raw_input)
    reg, cycle, crt = 1, 0, ""
    for n in input:
        crt += '#' if abs(cycle % 40 - reg) <= 1 else '.'
        cycle += 1
        if n is not None:
            crt += '#' if abs(cycle % 40 - reg) <= 1 else '.'
            cycle += 1
            reg += n
    for i in range(0, len(crt), 40):
        print(crt[i:i+40])
