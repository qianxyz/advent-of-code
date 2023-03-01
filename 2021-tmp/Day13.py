from util import Submarine


class TransparentOrigami(Submarine):

    def _parseLine(self, line):
        if '=' in line:
            axis, n = line.split()[-1].split('=')
            return axis, int(n)
        elif line:
            return tuple(int(n) for n in line.split(','))

    def __init__(self):
        input = self.getInput()
        breakline = input.index(None)
        self.marks = set(input[:breakline])
        self.instructions = input[breakline+1:]

    def foldSingleMark(self, instruction, mark):
        axis, foldLine = instruction
        x, y = mark
        if axis == 'x':
            newx = x if x < foldLine else 2 * foldLine - x
            newy = y
        else:
            newx = x
            newy = y if y < foldLine else 2 * foldLine - y
        return newx, newy

    def foldOnce(self, instruction):
        newMarks = set(self.foldSingleMark(instruction, mark)
                       for mark in self.marks)
        self.marks = newMarks

    def marksAfterFirstFold(self):
        self.foldOnce(self.instructions[0])
        return len(self.marks)

    def foldAll(self):
        for instruction in self.instructions:
            self.foldOnce(instruction)

    def printGrid(self):
        self.foldAll()
        xMax = max(x for x, _ in self.marks) + 1
        yMax = max(y for _, y in self.marks) + 1
        grid = [['.'] * xMax for _ in range(yMax)]

        for x, y in self.marks:
            grid[y][x] = '#'

        for line in grid:
            print(''.join(line))


if __name__ == '__main__':
    submarine = TransparentOrigami()
    print(submarine.marksAfterFirstFold())

    submarine.printGrid()
