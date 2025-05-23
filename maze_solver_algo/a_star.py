from heapq import heappush, heappop

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve_a_star(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    open_set = []
    heappush(open_set, (0 + heuristic(start, end), 0, start))
    came_from = {start: None}
    g_score = {start: 0}
    visited = set()

    while open_set:
        _, cost, current = heappop(open_set)
        y, x = current

        if current in visited:
            continue
        visited.add(current)

        if current == end:
            break

        for dy, dx in directions:
            ny, nx = y + dy * 2, x + dx * 2
            mid_y, mid_x = y + dy, x + dx
            neighbor = (ny, nx)

            if (
                0 <= ny < rows and 0 <= nx < cols and
                grid[ny][nx] == 0 and grid[mid_y][mid_x] == 0
            ):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, end)
                    heappush(open_set, (f_score, tentative_g, neighbor))
                    came_from[neighbor] = current

    # Backtrack
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()
    return path
