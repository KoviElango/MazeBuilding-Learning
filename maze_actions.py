from maze_builder import MazeBuilder
from maze_solver_algo import MazeSolver

class MazeActions:
    def __init__(self, size=21):
        self.size = size
        self.builder = MazeBuilder(size)
        self.start = (1, 1)
        self.end = (size - 2, size - 2)
        self.solver = MazeSolver(self.builder.get_grid(), self.start, self.end)
        self.path = []
        self.path_iter = None
        self.prev_path_cell = None
        self.maze_built = False

    def get_grid(self):
        return self.builder.get_grid()

    def reset(self):
        self.builder = MazeBuilder(self.size)
        self.solver = MazeSolver(self.builder.get_grid(), self.start, self.end)
        self.path = []
        self.path_iter = None
        self.prev_path_cell = None
        self.maze_built = False

    def clear_path(self):
        grid = self.get_grid()
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == 2:
                    grid[y][x] = 0

    def solve(self, algorithm):
        if not self.maze_built:
            return
        self.clear_path()
        self.prev_path_cell = None
        self.solver.solve(algorithm)
        self.path = self.solver.get_path()
        self.path_iter = iter(self.path) if self.path else None

    def get_next_path_steps(self, steps=2):
        if self.path_iter is None:
            return []
        result = []
        try:
            for _ in range(steps):
                yx = next(self.path_iter)
                # Fill in intermediate cells for continuity
                if self.prev_path_cell:
                    py, px = self.prev_path_cell
                    y, x = yx
                    if abs(py - y) + abs(px - x) > 1:
                        iy, ix = (py + y) // 2, (px + x) // 2
                        result.append((iy, ix))
                result.append(yx)
                self.prev_path_cell = yx
        except StopIteration:
            self.path_iter = None
        return result
