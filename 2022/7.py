from collections import defaultdict


def _parse_input(raw_input: list[str]):
    cwd = list()
    dirs = defaultdict(list)

    for line in raw_input:
        match line.split():
            case ["$", "cd", "/"]:
                cwd.clear()
            case ["$", "cd", ".."]:
                cwd.pop()
            case ["$", "cd", dir]:
                cwd.append(dir)
            case ["$", "ls"]:
                continue
            case [size, name]:
                path = "/" + "".join(s + "/" for s in cwd)
                dirs[path].append(name if size == "dir" else int(size))

    return dirs


class Helper:
    def __init__(self, dirs: dict[str, list[int | str]]) -> None:
        self.dirs = dirs
        self.memo = dict()

    def dir_size(self, dir: str) -> int:
        try:
            return self.memo[dir]
        except KeyError:
            size = 0
            for file in self.dirs[dir]:
                if isinstance(file, int):
                    size += file
                else:
                    size += self.dir_size(f"{dir}{file}/")
            self.memo[dir] = size
            return size


def part1(raw_input: list[str]):
    input = _parse_input(raw_input)
    helper = Helper(input)
    helper.dir_size("/")
    return sum(v for v in helper.memo.values() if v <= 100000)


def part2(raw_input: list[str]):
    input = _parse_input(raw_input)
    helper = Helper(input)
    total = helper.dir_size("/")
    return min(v for v in helper.memo.values() if total - v <= 40000000)
