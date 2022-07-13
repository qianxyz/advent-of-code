import itertools as it


def _parse_input(raw_input: list[str]):
    return [int(line) for line in raw_input]


def is_sum_two(nums: list[int], target: int):
    for x, y in it.combinations(nums, 2):
        if x + y == target:
            return True
    return False


def part1(raw_input: list[str]):
    nums = _parse_input(raw_input)
    for i, n in enumerate(nums):
        if i >= 25 and not is_sum_two(nums[i-25:i], n):
            return n


def part2(raw_input: list[str]):
    nums = _parse_input(raw_input)
    target = part1(raw_input)

    N = len(nums)
    # sum_grid[i][j] = sum(nums[i:j])
    sum_grid = [[0]*(N+1) for _ in range(N+1)]
    for i in range(N+1):
        for j in range(i+1, N+1):
            sum_grid[i][j] = sum_grid[i][j-1] + nums[j-1]
            if sum_grid[i][j] == target:
                return max(nums[i:j]) + min(nums[i:j])
