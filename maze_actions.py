from maze_builder import MazeBuilder
from maze_solver_algo import MazeSolver

class MazeActions:
    def __init__(self, size=99):
        self.size = size
        self.start = (1, 1)
        self.end = (size - 2, size - 2)

        self.builder = MazeBuilder(size)
        self.solver = MazeSolver(self.builder.get_grid(), self.start, self.end)

        self.path = []
        self.path_iter = None
        self.prev_path_cell = None
        self.maze_built = False


    # Grid Access
    def get_grid(self):
        return self.builder.get_grid()


    # Maze State Management
    def reset(self):
        self.builder = MazeBuilder(self.size)
        self.solver = MazeSolver(self.builder.get_grid(), self.start, self.end)
        self._reset_path_state()
        self.maze_built = False

    def _reset_path_state(self):
        self.path = []
        self.path_iter = None
        self.prev_path_cell = None

    def clear_path(self):
        grid = self.get_grid()
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == 2:
                    grid[y][x] = 0

    # Solving Logic
    def solve(self, algorithm):
        if not self.maze_built:
            return
        self.clear_path()
        self._reset_path_state()

        self.solver.solve(algorithm)
        self.path = self.solver.get_path()
        self.path_iter = iter(self.path) if self.path else None

    def get_next_path_steps(self, steps=2):
        if self.path_iter is None:
            return []

        return self._collect_path_steps(steps)

    def _collect_path_steps(self, steps):
        result = []
        try:
            for _ in range(steps):
                current = next(self.path_iter)

                if self.prev_path_cell:
                    self._maybe_add_intermediate_step(result, self.prev_path_cell, current)

                result.append(current)
                self.prev_path_cell = current
        except StopIteration:
            self.path_iter = None

        return result

    def _maybe_add_intermediate_step(self, result, prev, current):
        py, px = prev
        y, x = current
        if abs(py - y) + abs(px - x) > 1:
            iy, ix = (py + y) // 2, (px + x) // 2
            result.append((iy, ix))
