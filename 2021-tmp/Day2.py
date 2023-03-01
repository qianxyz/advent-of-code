from util import Submarine


class Dive(Submarine):

    def _parseLine(self, line):
        command, units = line.split()
        return (command, int(units))

    def __init__(self):
        self.commands = self.getInput()
        self.hpos = 0
        self.depth = 0

    def forward(self, units):
        self.hpos += units

    def up(self, units):
        self.depth -= units

    def down(self, units):
        self.depth += units

    def run(self):
        for command, units in self.commands:
            runCommand = getattr(self, command)
            runCommand(units)
        return self.hpos, self.depth


class DiveWithAim(Dive):

    def __init__(self):
        super().__init__()
        self.aim = 0

    def forward(self, units):
        self.hpos += units
        self.depth += self.aim * units

    def up(self, units):
        self.aim -= units

    def down(self, units):
        self.aim += units


if __name__ == '__main__':
    submarine = Dive()
    hpos, depth = submarine.run()
    print(hpos * depth)

    submarine = DiveWithAim()
    hpos, depth = submarine.run()
    print(hpos * depth)
