from util import Submarine
import ast
from itertools import permutations
from time import perf_counter


class Tree:

    def __init__(self, val=None, left=None, right=None,
                 depth=0, last=None, next=None):
        """
        The .last and .next attributes are only used at leaves
        which form a doubly linked list.
        """
        self.val = val
        self.left = left
        self.right = right
        self.depth = depth
        self.last = last
        self.next = next

    def __add__(self, other):
        for node in self.traversal():
            node.depth += 1
        for node in other.traversal():
            node.depth += 1
        root = Tree(left=self, right=other)
        root.reduce()
        return root

    def traversal(self):
        yield self
        if self.val is None:
            yield from self.left.traversal()
            yield from self.right.traversal()

    def leafTraversal(self):
        for node in self.traversal():
            if node.val is not None:
                yield node

    def linkLeaves(self):
        leaves = dict(enumerate(self.leafTraversal()))
        for i, leaf in leaves.items():
            leaf.last = leaves.get(i-1, None)
            leaf.next = leaves.get(i+1, None)

    def reduce(self):
        self.linkLeaves()
        while self.explode() or self.split():  # 'or' is lazy
            continue

    def explode(self):
        """Return True if exploded."""
        for node in self.traversal():
            if node.val is None and node.depth >= 4:
                lastLeaf = node.left.last
                nextLeaf = node.right.next
                if lastLeaf is not None:
                    lastLeaf.val += node.left.val
                if nextLeaf is not None:
                    nextLeaf.val += node.right.val
                node.val = 0
                self.linkLeaves()
                return True
        return False

    def split(self):
        """Return True if split."""
        for leaf in self.leafTraversal():
            if leaf.val >= 10:
                lval = leaf.val // 2
                rval = leaf.val - lval
                lleaf = Tree(val=lval, depth=leaf.depth+1)
                rleaf = Tree(val=rval, depth=leaf.depth+1)
                leaf.val = None
                leaf.left, leaf.right = lleaf, rleaf
                self.linkLeaves()
                return True
        return False

    def findMagnitude(self):
        if self.val is not None:
            return self.val
        return 3 * self.left.findMagnitude() + 2 * self.right.findMagnitude()


class SnailfishTree(Submarine):

    def _parseLine(self, line):
        return ast.literal_eval(line)

    def __init__(self):
        self.nestedLists = self.getInput()

    def listToTree(self, lst, depth=0):
        if isinstance(lst, int):
            return Tree(val=lst, depth=depth)
        else:
            return Tree(left=self.listToTree(lst[0], depth+1),
                        right=self.listToTree(lst[1], depth+1),
                        depth=depth)

    def treeToList(self, tree: Tree):
        if tree.val is not None:
            return tree.val
        else:
            return [self.treeToList(tree.left),
                    self.treeToList(tree.right)]

    def sumOfAll(self):
        acc = self.listToTree(self.nestedLists[0])
        for lst in self.nestedLists[1:]:
            tr = self.listToTree(lst)
            acc = acc + tr
        return acc.findMagnitude()

    def largestSumOfTwo(self):
        sums = []
        for lst1, lst2 in permutations(self.nestedLists, 2):
            tr1 = self.listToTree(lst1)
            tr2 = self.listToTree(lst2)
            sumtr = tr1 + tr2
            sums.append(sumtr.findMagnitude())
        return max(sums)


class SnailfishLineParsing(Submarine):

    def _parseLine(self, line):
        return [s if s in '[,]' else int(s) for s in line]

    def __init__(self):
        self.nests = self.getInput()
        self.reg = None  # where side effects take place

    def reduce(self):
        while self.explode() or self.split():
            continue

    def explode(self):
        depth = 0
        for i, n in enumerate(self.reg):
            if n == '[':
                depth += 1
            elif n == ']':
                depth -= 1
            if depth > 4:
                p = i - 1
                while p >= 0 and isinstance(self.reg[p], str):
                    p -= 1
                if p >= 0:
                    self.reg[p] += self.reg[i+1]
                p = i + 5
                while p < len(self.reg) and isinstance(self.reg[p], str):
                    p += 1
                if p < len(self.reg):
                    self.reg[p] += self.reg[i+3]
                self.reg = self.reg[:i] + [0] + self.reg[i+5:]
                return True
        return False

    def split(self):
        for i, n in enumerate(self.reg):
            if isinstance(n, int) and n >= 10:
                n1 = n // 2
                n2 = n - n1
                insert = ['[', n1, ',', n2, ']']
                self.reg = self.reg[:i] + insert + self.reg[i+1:]
                return True
        return False

    def evaluateList(self, lst):
        if isinstance(lst, int):
            return lst
        return 3 * self.evaluateList(lst[0]) + 2 * self.evaluateList(lst[1])

    def evaluateReg(self):
        lststr = ''.join(str(s) for s in self.reg)
        lst = ast.literal_eval(lststr)
        return self.evaluateList(lst)

    def sumOfAll(self):
        self.reg = self.nests[0]
        for nest in self.nests[1:]:
            self.reg = ['['] + self.reg + [','] + nest + [']']
            self.reduce()
        return self.evaluateReg()

    def largestSumOfTwo(self):
        sums = []
        for nest1, nest2 in permutations(self.nests, 2):
            self.reg = ['['] + nest1 + [','] + nest2 + [']']
            self.reduce()
            sums.append(self.evaluateReg())
        return max(sums)


if __name__ == '__main__':

    start = perf_counter()
    submarine = SnailfishTree()
    print(submarine.sumOfAll())
    print(submarine.largestSumOfTwo())
    end = perf_counter()
    print('Tree time:', end-start)

    start = perf_counter()
    submarine = SnailfishLineParsing()
    print(submarine.sumOfAll())
    print(submarine.largestSumOfTwo())
    end = perf_counter()
    print('Line parsing time:', end-start)
