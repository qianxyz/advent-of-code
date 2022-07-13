def _parse_input(raw_input: list[str]):
    for line in raw_input:
        yield [d if d in "+*()" else int(d) for d in line.replace(' ', '')]


class Evaluator:

    def priority(self, op):
        """Possible op in "+*(". '(' should have the lowest priority."""
        raise NotImplementedError

    def infix_to_postfix(self, infix):
        postfix = []
        opstack = []
        for token in infix:
            if isinstance(token, int):
                postfix.append(token)
            elif token in "+*":
                while (opstack and
                       self.priority(opstack[-1]) >= self.priority(token)):
                    postfix.append(opstack.pop())
                opstack.append(token)
            elif token == '(':
                opstack.append(token)
            elif token == ')':
                while opstack[-1] != '(':
                    postfix.append(opstack.pop())
                opstack.pop()
        while opstack:
            postfix.append(opstack.pop())
        return postfix

    def postfix_eval(self, postfix):
        stack = []
        for token in postfix:
            if isinstance(token, int):
                stack.append(token)
            else:
                n1 = stack.pop()
                n2 = stack.pop()
                stack.append(n1 + n2 if token == '+' else n1 * n2)
        return stack.pop()


class EvaluatorLeftToRight(Evaluator):

    def priority(self, op):
        return {'+': 1, '*': 1, '(': 0}[op]


class EvaluatorAdditionFirst(Evaluator):

    def priority(self, op):
        return {'+': 2, '*': 1, '(': 0}[op]


def part1(raw_input: list[str]):
    exprs = _parse_input(raw_input)
    ev = EvaluatorLeftToRight()
    return sum(ev.postfix_eval(ev.infix_to_postfix(infix)) for infix in exprs)


def part2(raw_input: list[str]):
    exprs = _parse_input(raw_input)
    ev = EvaluatorAdditionFirst()
    return sum(ev.postfix_eval(ev.infix_to_postfix(infix)) for infix in exprs)
