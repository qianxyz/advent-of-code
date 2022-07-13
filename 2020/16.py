import re
import math


def _parse_input(raw_input: list[str]):
    fields = dict()
    tickets = []
    for line in raw_input:
        match = re.match(r"(.*): (\d+)-(\d+) or (\d+)-(\d+)", line)
        if match:
            key = match.group(1)
            a, b, c, d = map(int, match.group(2, 3, 4, 5))
            fields[key] = (range(a, b+1), range(c, d+1))
        elif line and not line.endswith(':'):
            tickets.append([int(d) for d in line.split(',')])
    return fields, tickets[0], tickets[1:]


class TicketValidation:

    def __init__(self, fields, your_ticket, nearby_tickets) -> None:
        self.fields = fields
        self.yours = your_ticket
        self.nearby = nearby_tickets

    def is_valid_value_for_field(self, value, key):
        return any(value in ran for ran in self.fields[key])

    def is_valid_value(self, value):
        return any(self.is_valid_value_for_field(value, key)
                   for key in self.fields.keys())

    def is_valid_ticket(self, ticket):
        return all(self.is_valid_value(n) for n in ticket)

    def order(self):
        valid_tickets = [t for t in self.nearby if self.is_valid_ticket(t)]
        valid_keys = [
            [key for key in self.fields.keys()
             if all(self.is_valid_value_for_field(v, key) for v in entries)]
            for entries in zip(*valid_tickets)]
        # sort to reduce backtracking
        ord_i = sorted(range(len(valid_keys)),
                       key=lambda i: len(valid_keys[i]))
        # DFS
        fringe = [[]]
        while fringe:
            current = fringe.pop()
            if set(current) == set(self.fields.keys()):
                return [c for _, c in sorted(zip(ord_i, current))]
            children = [current + [n] for n in valid_keys[ord_i[len(current)]]
                        if n not in current]
            fringe += children
        return []

    def your_ticket_as_dict(self):
        ord_fields = self.order()
        return {k: v for k, v in zip(ord_fields, self.yours)}


def part1(raw_input: list[str]):
    fields, yours, nearby = _parse_input(raw_input)
    tval = TicketValidation(fields, yours, nearby)
    return sum(n for t in nearby for n in t if not tval.is_valid_value(n))


def part2(raw_input: list[str]):
    fields, yours, nearby = _parse_input(raw_input)
    tval = TicketValidation(fields, yours, nearby)
    yours_dict = tval.your_ticket_as_dict()
    return math.prod(v for k, v in yours_dict.items()
                     if k.startswith('departure'))
