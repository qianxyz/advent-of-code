def reduce(line: str) -> str | list[str]:
    stack = []
    for c in line:
        if c in "([{<":
            stack.append(c)
        elif stack[-1] == {')': '(', ']': '[', '}': '{', '>': '<'}[c]:
            stack.pop()
        else:
            return c
    return stack


def part1(raw_input: list[str]):
    score = 0
    for line in raw_input:
        s = reduce(line)
        if isinstance(s, str):
            score += {')': 3, ']': 57, '}': 1197, '>': 25137}[s]
    return score


def part2(raw_input: list[str]):
    scores = []
    for line in raw_input:
        s = reduce(line)
        if isinstance(s, list):
            score = 0
            for c in s[::-1]:
                score *= 5
                score += {'(': 1, '[': 2, '{': 3, '<': 4}[c]
            scores.append(score)
    scores.sort()
    return scores[len(scores) // 2]
