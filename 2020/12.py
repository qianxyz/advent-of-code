from typing import List
import numpy as np


def _parse_input(raw_input: List[str]):
    return [(line[0], int(line[1:])) for line in raw_input]


class Ship:

    DIRECTIONS = {'N': np.array([0, 1]),
                  'S': np.array([0, -1]),
                  'W': np.array([-1, 0]),
                  'E': np.array([1, 0])}
    ROTATIONS = {'R': np.array([[0, -1],
                                [1, 0]]),
                 'L': np.array([[0, 1],
                                [-1, 0]])}

    def __init__(self, instructions) -> None:
        self.instructions = instructions
        self.orientation = np.array([1, 0])
        self.position = np.array([0, 0])

    def run(self):
        for op, num in self.instructions:
            if op in "NSWE":
                self.position += num * self.DIRECTIONS[op]
            elif op in "RL":
                for _ in range(num // 90):
                    self.orientation = np.matmul(self.orientation,
                                                 self.ROTATIONS[op])
            elif op == 'F':
                self.position += num * self.orientation

    def manhattan_distance(self):
        return sum(abs(self.position))


class ShipWithWaypoint(Ship):

    def __init__(self, instructions) -> None:
        super().__init__(instructions)
        self.waypoint = np.array([10, 1])

    def run(self):
        for op, num in self.instructions:
            if op in "NSWE":
                self.waypoint += num * self.DIRECTIONS[op]
            elif op in "RL":
                for _ in range(num // 90):
                    self.waypoint = np.matmul(self.waypoint,
                                              self.ROTATIONS[op])
            elif op == 'F':
                self.position += num * self.waypoint


def part1(raw_input: List[str]):
    instructions = _parse_input(raw_input)
    ship = Ship(instructions)
    ship.run()
    return ship.manhattan_distance()


def part2(raw_input: List[str]):
    instructions = _parse_input(raw_input)
    ship = ShipWithWaypoint(instructions)
    ship.run()
    return ship.manhattan_distance()
