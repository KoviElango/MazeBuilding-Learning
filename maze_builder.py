import random

class MazeBuilder:
    def __init__(self, size):
        self.size = size
        self.grid = self._initialize_grid()
        self.visited = self._initialize_visited()
        self._directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    def _initialize_grid(self):
        """Creates a grid with walls (1s) and carveable cells (0s)."""
        grid = [[1 for _ in range(self.size)] for _ in range(self.size)]
        for y in range(1, self.size, 2):
            for x in range(1, self.size, 2):
                grid[y][x] = 0
        return grid

    def _initialize_visited(self):
        """Initializes a visited matrix."""
        return [[False for _ in range(self.size)] for _ in range(self.size)]

    def _is_valid_cell(self, y, x):
        """Checks if a cell is within bounds and unvisited."""
        return 1 <= y < self.size - 1 and 1 <= x < self.size - 1 and not self.visited[y][x]

    def _carve_passage(self, y, x, ny, nx):
        """Carves a passage between current and next cell."""
        between_y, between_x = (y + ny) // 2, (x + nx) // 2
        self.grid[between_y][between_x] = 0

    def _dfs_maze_generator(self, start_y=1, start_x=1):
        """Yields cells as maze is being generated."""
        stack = [(start_y, start_x)]
        self.visited[start_y][start_x] = True

        while stack:
            y, x = stack.pop()
            yield y, x

            random.shuffle(self._directions)
            for dy, dx in self._directions:
                ny, nx = y + dy, x + dx
                if self._is_valid_cell(ny, nx):
                    self.visited[ny][nx] = True
                    self._carve_passage(y, x, ny, nx)
                    stack.append((ny, nx))

    def build(self):
        """Public gateway to start the maze building generator."""
        return self._dfs_maze_generator()

    def get_grid(self):
        """Returns the final grid."""
        return self.grid
