from .left_wall import solve_left_wall
from .dijkstra import solve_dijkstra
from .a_star import solve_a_star
from .dfs_backtracking import solve_dfs_backtracking
from .tremaux import solve_tremaux

class MazeSolver:
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.path = []

    def solve(self, method="left_wall"):
        if method == "left_wall":
            self.path = solve_left_wall(self.grid, self.start, self.end)
        elif method == "dijkstra":
            self.path = solve_dijkstra(self.grid, self.start, self.end)
        elif method == "a_star":
            self.path = solve_a_star(self.grid, self.start, self.end)
        elif method == "dfs_backtracking":
            self.path = solve_dfs_backtracking(self.grid, self.start, self.end)
        elif method == "tremaux":  # <-- Add this block
            self.path = solve_tremaux(self.grid, self.start, self.end)
        else:
            raise ValueError(f"Unknown method: {method}")

    def get_path(self):
        return self.path
