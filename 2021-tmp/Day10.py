from util import Submarine

L_BR = '([{<'
R_BR = ')]}>'
BR_PAIRS = list(zip(L_BR, R_BR))
BR_DICT = dict(zip(L_BR, R_BR))


class SyntaxScoring(Submarine):

    def _parseLine(self, line):
        return line

    def __init__(self):
        self.lines = self.getInput()
        self.syntaxErrorScore = 0
        self.autocompleteScores = []
        self.syntaxErrorScoreTable = [3, 57, 1197, 25137]
        self.autocompleteScoreTable = [1, 2, 3, 4]

    def checkLine(self, line):
        stack = []
        for br in line:
            if br in L_BR:
                stack.append(br)
            else:
                if (stack[-1], br) in BR_PAIRS:
                    stack.pop()
                else:
                    self.syntaxError(br)
                    return

        closingBrackets = ''
        while stack:
            lbr = stack.pop()
            closingBrackets += BR_DICT[lbr]
        self.autocomplete(closingBrackets)

    def syntaxError(self, illegalBracket):
        scoreTable = dict(zip(R_BR, self.syntaxErrorScoreTable))
        self.syntaxErrorScore += scoreTable[illegalBracket]

    def autocomplete(self, closingBrackets):
        scoreTable = dict(zip(R_BR, self.autocompleteScoreTable))
        score = 0
        for br in closingBrackets:
            score *= 5
            score += scoreTable[br]
        self.autocompleteScores.append(score)

    def getScores(self):
        for line in self.lines:
            self.checkLine(line)
        acScores = sorted(self.autocompleteScores)
        acScore = acScores[len(acScores) // 2]
        return self.syntaxErrorScore, acScore


if __name__ == '__main__':
    submarine = SyntaxScoring()
    print(submarine.getScores())
