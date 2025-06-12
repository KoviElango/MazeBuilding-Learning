def solve_tremaux(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    stack = [start]
    parent = {start: None}
    marks = {}

    while stack:
        y, x = stack[-1]
        if (y, x) == end:
            break

        found = False
        for dy, dx in directions:
            ny, nx = y + dy * 2, x + dx * 2
            mid_y, mid_x = y + dy, x + dx
            if (
                0 <= ny < rows and 0 <= nx < cols and
                grid[ny][nx] == 0 and grid[mid_y][mid_x] == 0
            ):
                if marks.get((ny, nx), 0) < 2:
                    marks[(ny, nx)] = marks.get((ny, nx), 0) + 1
                    marks[(y, x)] = marks.get((y, x), 0) + 1
                    parent[(ny, nx)] = (y, x)
                    stack.append((ny, nx))
                    found = True
                    break
        if not found:
            stack.pop()

    # Backtrack to build path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent.get(current)
    path.reverse()
    return path