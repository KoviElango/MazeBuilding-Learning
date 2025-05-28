def solve_dfs_backtracking(grid, start, end):
    height = len(grid)
    width = len(grid[0])
    visited = [[False for _ in range(width)] for _ in range(height)]
    path = []

    def dfs(y, x):
        if (y, x) == end:
            path.append((y, x))
            return True

        if y < 0 or x < 0 or y >= height or x >= width:
            return False
        if grid[y][x] == 1 or visited[y][x]:
            return False

        visited[y][x] = True
        path.append((y, x))

        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if dfs(y + dy, x + dx):
                return True

        path.pop()
        return False

    if dfs(start[0], start[1]):
        return path
    else:
        raise ValueError("No path found using DFS Backtracking")
