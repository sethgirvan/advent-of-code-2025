import fileinput

grid = [list(line.rstrip()) for line in fileinput.input()]

def is_paper_roll(i: int, j: int) -> bool:
    return 0 <= i and i < len(grid) and 0 <= j and j < len(grid[i]) and grid[i][j] == "@"

def forklift_accessible(i: int, j: int) -> bool:
    if grid[i][j] != "@":
        return False

    adjacent_rolls = sum(is_paper_roll(i - 1, y) for y in range(j - 1, j + 2))
    adjacent_rolls += is_paper_roll(i, j - 1) + is_paper_roll(i, j + 1)
    adjacent_rolls += sum(is_paper_roll(i + 1, y) for y in range(j - 1, j + 2))
    return adjacent_rolls < 4

p1 = sum(forklift_accessible(i, j) for i in range(0, len(grid)) for j in range(0, len(grid[i])))
print(f"p1 answer: {p1}")

p2 = 0
while True:
    removed = 0
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            if forklift_accessible(i, j):
                removed += 1
                grid[i][j] = "x"
    if removed == 0:
        break

    p2 += removed

print(f"p2 answer: {p2}")
