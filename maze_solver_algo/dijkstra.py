from queue import PriorityQueue

def solve_dijkstra(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    pq = PriorityQueue()
    pq.put((0, start))
    visited = set()
    parent = {start: None}

    while not pq.empty():
        dist, (y, x) = pq.get()
        if (y, x) in visited:
            continue
        visited.add((y, x))

        if (y, x) == end:
            break

        for dy, dx in directions:
            ny, nx = y + dy * 2, x + dx * 2
            mid_y, mid_x = y + dy, x + dx
            if (
                0 <= ny < rows and
                0 <= nx < cols and
                grid[ny][nx] == 0 and
                grid[mid_y][mid_x] == 0
            ):
                if (ny, nx) not in visited:
                    pq.put((dist + 1, (ny, nx)))
                    parent[(ny, nx)] = (y, x)

    # Backtrack
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path
