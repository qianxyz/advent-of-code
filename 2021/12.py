from collections import defaultdict
from collections.abc import Callable


def _parse_input(raw_input: list[str]):
    graph = defaultdict(list)
    for line in raw_input:
        a, b = line.split('-')
        if b != "start" and a != "end":
            graph[a].append(b)
        if a != "start" and b != "end":
            graph[b].append(a)
    return graph


Node = str
Path = list[Node]
Graph = dict[Node, list[Node]]


def helper(graph: Graph, is_valid: Callable[[Path, Node], bool]) -> int:
    count = 0
    stack = [["start"]]
    while stack:
        path = stack.pop()
        last = path[-1]
        if last == "end":
            count += 1
            continue
        for next in graph[last]:
            if is_valid(path, next):
                stack.append(path + [next])
    return count


def part1(raw_input: list[str]):
    graph = _parse_input(raw_input)
    def is_valid(path: Path, next: Node) -> bool:
        return next.isupper() or next not in path
    return helper(graph, is_valid)


def part2(raw_input: list[str]):
    graph = _parse_input(raw_input)
    def is_valid(path: Path, next: Node) -> bool:
        if next.isupper() or next not in path:
            return True
        small_caves = [n for n in path if n.islower()]
        return len(small_caves) == len(set(small_caves))
    return helper(graph, is_valid)
