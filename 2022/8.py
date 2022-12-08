def _parse_input(raw_input: list[str]):
    return [list(map(int, line)) for line in raw_input]


def part1(raw_input: list[str]):
    grid = _parse_input(raw_input)
    return sum(
        all(grid[x][y0] < n for x in range(x0))
        or all(grid[x][y0] < n for x in range(x0+1, len(grid)))
        or all(grid[x0][y] < n for y in range(y0))
        or all(grid[x0][y] < n for y in range(y0+1, len(row)))
        for x0, row in enumerate(grid)
        for y0, n in enumerate(row)
    )


def scenic_score(grid, x, y):
    score = 1
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        count = 0
        x0, y0 = x + dx, y + dy
        while 0 <= x0 < len(grid) and 0 <= y0 < len(grid[0]):
            count += 1
            if grid[x0][y0] >= grid[x][y]:
                break
            else:
                x0 += dx
                y0 += dy
        score *= count
    return score


def part2(raw_input: list[str]):
    grid = _parse_input(raw_input)
    return max(
        scenic_score(grid, x, y)
        for x in range(len(grid))
        for y in range(len(grid[0]))
    )
