def solve_left_wall(grid, start, end):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
    y, x = start
    dir = 1  # Start facing right
    path = [(y, x)]
    rows, cols = len(grid), len(grid[0])
    visited = set()

    while (y, x) != end:
        if (y, x, dir) in visited:
            raise ValueError("Infinite loop detected")
        visited.add((y, x, dir))

        # Turn left
        left_dir = (dir - 1) % 4
        dy, dx = directions[left_dir]
        ny, nx = y + dy * 2, x + dx * 2
        mid_y, mid_x = y + dy, x + dx
        if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == 0 and grid[mid_y][mid_x] == 0:
            dir = left_dir
            y, x = ny, nx
            path.append((y, x))
            continue

        # Move forward
        dy, dx = directions[dir]
        ny, nx = y + dy * 2, x + dx * 2
        mid_y, mid_x = y + dy, x + dx
        if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == 0 and grid[mid_y][mid_x] == 0:
            y, x = ny, nx
            path.append((y, x))
            continue

        # Turn right
        right_dir = (dir + 1) % 4
        dy, dx = directions[right_dir]
        ny, nx = y + dy * 2, x + dx * 2
        mid_y, mid_x = y + dy, x + dx
        if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == 0 and grid[mid_y][mid_x] == 0:
            dir = right_dir
            y, x = ny, nx
            path.append((y, x))
            continue

        # Turn back
        dir = (dir + 2) % 4

    return path
