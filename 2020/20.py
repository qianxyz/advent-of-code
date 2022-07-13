from typing import List


def _parse_input(raw_input: List[str]):
    pieces = dict()
    for line in raw_input:
        if line.startswith("Tile"):
            tile_ID = int(line[5:-1])
            pieces[tile_ID] = []
        elif line:
            pieces[tile_ID].append(list(line))
    return pieces


class Piece:

    def __init__(self, ID, grid) -> None:
        self.ID = ID
        self.grid = grid

    def sides(self):
        sides = [self.grid[0], self.grid[-1],  # top & bottom
                 [self.grid[i][0] for i in range(len(self.grid))],  # left
                 [self.grid[i][-1] for i in range(len(self.grid))]]  # right
        sides += [s[::-1] for s in sides]  # reverses
        return set(map("".join, sides))


def part1(raw_input: List[str]):
    pieces = _parse_input(raw_input)
    pieces = [Piece(id, grid) for id, grid in pieces.items()]
    prod = 1
    for base in pieces:
        matches = sum(bool(set.intersection(base.sides(), other.sides()))
                      for other in pieces if other != base)
        if matches == 2:
            prod *= base.ID
    return prod


def part2(raw_input: List[str]):
    _ = _parse_input(raw_input)
    return NotImplemented
