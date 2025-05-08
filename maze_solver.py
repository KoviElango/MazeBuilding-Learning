class MazeSolver:
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.path = []

    def solve_left_wall(self):
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
        y, x = self.start
        dir = 1  # Start facing right
        self.path.append((y, x))
        rows, cols = len(self.grid), len(self.grid[0])
        visited = set()

        while (y, x) != self.end:
            # Track visited cells + direction
            if (y, x, dir) in visited:
                raise ValueError("Infinite loop detected")
            visited.add((y, x, dir))

            # Try to turn left
            left_dir = (dir - 1) % 4
            dy, dx = directions[left_dir]
            ny, nx = y + dy * 2, x + dx * 2
            mid_y, mid_x = y + dy, x + dx
            if 0 <= ny < rows and 0 <= nx < cols and self.grid[ny][nx] == 0 and self.grid[mid_y][mid_x] == 0:
                dir = left_dir
                y, x = ny, nx
                self.path.append((y, x))
                continue

            # Move forward if possible
            dy, dx = directions[dir]
            ny, nx = y + dy * 2, x + dx * 2
            mid_y, mid_x = y + dy, x + dx
            if 0 <= ny < rows and 0 <= nx < cols and self.grid[ny][nx] == 0 and self.grid[mid_y][mid_x] == 0:
                y, x = ny, nx
                self.path.append((y, x))
                continue

            # Try to turn right
            right_dir = (dir + 1) % 4
            dy, dx = directions[right_dir]
            ny, nx = y + dy * 2, x + dx * 2
            mid_y, mid_x = y + dy, x + dx
            if 0 <= ny < rows and 0 <= nx < cols and self.grid[ny][nx] == 0 and self.grid[mid_y][mid_x] == 0:
                dir = right_dir
                y, x = ny, nx
                self.path.append((y, x))
                continue

            # Turn back if no other options
            dir = (dir + 2) % 4

    def get_path(self):
        return self.path
