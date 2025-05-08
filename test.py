grid = [['.' for _ in range(7)] for _ in range(7)]
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

y, x = 1, 1
dir = 1
grid[y][x] = 'S'

for _ in range(2):
    dy, dx = directions[dir]
    y, x = y + dy, x + dx
    grid[y][x] = '*'

dir = (dir + 1) % 4

for _ in range(2):
    dy, dx = directions[dir]
    y, x = y + dy, x + dx
    grid[y][x] = '*'

dir = (dir + 1) % 4

for _ in range(2):
    dy, dx = directions[dir]
    y, x = y + dy, x + dx
    grid[y][x] = '*'

dir = (dir - 1) % 4

for _ in range(1):
    dy, dx = directions[dir]
    y, x = y + dy, x + dx
    grid[y][x] = '*'

dir = (dir + 2) % 4

for _ in range(2):
    dy, dx = directions[dir]
    y, x = y + dy, x + dx
    grid[y][x] = '*'

dir = (dir - 1) % 4

for _ in range(2):
    dy, dx = directions[dir]
    y, x = y + dy, x + dx
    grid[y][x] = '*'

for row in grid:
    print(' '.join(row))