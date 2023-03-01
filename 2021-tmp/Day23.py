from util import Submarine
import heapq
from time import perf_counter


def manhattan(xy1, xy2):
    x1, y1 = xy1
    x2, y2 = xy2
    return abs(x1 - x2) + abs(y1 - y2)


class BurrowState:
    """A state of the burrow.

    Positions are packed into tuples (x, y) as in the 2d grid:
      y:0123456789...
    x:0 #############
      1 #...........#
      2 ###.#.#.#.###
      3   #.#.#.#.#   - bottom(=3|5)
      4   #########
    """

    HOME_COL = {'A': 3,
                'B': 5,
                'C': 7,
                'D': 9}
    COST = {'A': 1,
            'B': 10,
            'C': 100,
            'D': 1000}

    def __init__(self, amphipods):
        """Construct a grid dict {position: type}."""
        self.grid = dict()
        for pos, type in amphipods:
            self.grid[pos] = type
        self.bottom = max(row for row, _ in self.grid)

    def isGoal(self):
        for (row, col), type in self.grid.items():
            if row == 1:
                return False
            if col != BurrowState.HOME_COL[type]:
                return False
        return True

    def legalDestinations(self, pos, type):
        row, col = pos

        if row == 1:  # in hallway; go home
            # to the home column
            hcol = BurrowState.HOME_COL[type]
            dcol = 1 if hcol > col else -1
            while col != hcol:
                col += dcol
                if (row, col) in self.grid:
                    return []
            # reached outside home, go down
            for hrow in range(self.bottom, 1, -1):
                if (hrow, hcol) not in self.grid:
                    return [(hrow, hcol)]
                if self.grid[(hrow, hcol)] != type:
                    return []

        # in room; go to hallway
        if (row - 1, col) in self.grid:  # upper tile blocked
            return []
        reachables = []
        left = col - 1
        while (1, left) not in self.grid and left > 0:
            if left not in {3, 5, 7, 9}:
                reachables.append((1, left))
            left -= 1
        right = col + 1
        while (1, right) not in self.grid and right < 12:
            if right not in {3, 5, 7, 9}:
                reachables.append((1, right))
            right += 1
        return reachables

    def legalMoves(self):
        for oldpos, type in self.grid.items():
            for newpos in self.legalDestinations(oldpos, type):
                cost = manhattan(oldpos, newpos) * BurrowState.COST[type]
                yield type, oldpos, newpos, cost

    def result(self, action):
        """Return a *new* BurrowState object after the action.
        action: (type, oldpos, newpos, cost)"""
        type, oldpos, newpos, _ = action
        newState = BurrowState(self.grid.items())
        del newState.grid[oldpos]
        newState.grid[newpos] = type
        return newState

    def heuristic(self):
        h = 0
        for pos, type in self.grid.items():
            row, col = pos
            hcol = BurrowState.HOME_COL[type]
            if row == 1:
                h += manhattan(pos, (2, hcol)) * BurrowState.COST[type]
            elif col != hcol:
                h += (manhattan(pos, (2, hcol))+2) * BurrowState.COST[type]
        return h

    def __eq__(self, other: 'BurrowState') -> bool:
        return set(self.grid.items()) == set(other.grid.items())

    def __hash__(self) -> int:
        return hash(str(sorted(self.grid.items())))

    def __getAsciiString(self):
        lines = ['#############',
                 '#...........#',
                 '###.#.#.#.###',
                 *('  #.#.#.#.#  ' for _ in range(self.bottom-2)),
                 '  #########  ']
        lines = [list(line) for line in lines]
        for (row, col), type in self.grid.items():
            lines[row][col] = type
        lines = [''.join(line) for line in lines]
        return '\n'.join(lines)

    def __str__(self) -> str:
        return self.__getAsciiString()


class PriorityQueue:

    def __init__(self) -> None:
        self.heap = []
        self.count = 0  # tie-breaker

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        _, _, item = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0


class AmphipodSearch(Submarine):

    def _parseLine(self, line):
        return line

    def __init__(self, isFull=False) -> None:
        map = self.getInput()
        if not isFull:
            rooms = [(x, y) for x in [2, 3] for y in [3, 5, 7, 9]]
        else:
            insert = ['  #D#C#B#A#',
                      '  #D#B#A#C#']
            map = map[:3] + insert + map[3:]
            rooms = [(x, y) for x in [2, 3, 4, 5] for y in [3, 5, 7, 9]]
        amphipods = [((row, col), map[row][col])
                     for row, col in rooms]
        self.puzzle = BurrowState(amphipods)

    def getStartState(self):
        return self.puzzle

    def isGoalState(self, state: BurrowState):
        return state.isGoal()

    def getChildren(self, state: BurrowState):
        """Return a list of (state, action, stepcost)."""
        succ = []
        for action in state.legalMoves():
            stepcost = action[-1]
            childState = state.result(action)
            succ.append((childState, action, stepcost))
        return succ

    def printActions(self, actions):
        state = self.puzzle
        print(state, '\n')
        cost = 0
        for action in actions:
            type, oldpos, newpos, stepcost = action
            state = state.result(action)
            cost += stepcost
            print(f'{type} from {oldpos} to {newpos}, cost {stepcost}')
            print(state, '\n')
        print(f'Total cost: {cost}')

    def astar(self):
        closed = set()
        fringe = PriorityQueue()
        startState = self.getStartState()
        startNode = (startState, [], 0)
        fringe.push(startNode, startState.heuristic())

        while not fringe.isEmpty():
            currState, actions, cost = fringe.pop()
            if self.isGoalState(currState):
                self.printActions(actions)
                return None
            if currState not in closed:
                closed.add(currState)
                for childState, a, stepcost in self.getChildren(currState):
                    childNode = (childState, actions + [a], cost + stepcost)
                    fringe.push(childNode,
                                childNode[-1] + childState.heuristic())


if __name__ == '__main__':
    start = perf_counter()
    submarine = AmphipodSearch()
    submarine.astar()
    end = perf_counter()
    print(f'Time: {end-start}', '\n')

    start = perf_counter()
    submarine = AmphipodSearch(isFull=True)
    submarine.astar()
    end = perf_counter()
    print(f'Time: {end-start}')
