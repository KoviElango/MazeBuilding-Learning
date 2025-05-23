# game_ui.py
import pygame
from maze_builder import MazeBuilder
from maze_solver_algo import MazeSolver

class GameUI:
    def __init__(self, size=21, cell_size=30):
        pygame.init()
        self.size = size
        self.cell_size = cell_size
        self.width = size * cell_size + 200  # extra for sidebar
        self.height = size * cell_size

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Solver Visualizer")

        self.clock = pygame.time.Clock()
        self.running = True
        self.buttons = []
        self.selected_algorithm = "left_wall"
        self.is_running = False
        self.maze_built = False

        self.builder = MazeBuilder(size)
        self.solver = MazeSolver(self.builder.get_grid(), (1, 1), (size - 2, size - 2))
        self.path_iter = None
        self.path = []
        self.prev_path_cell = None  # <-- Add this line

    def draw_sidebar(self):
        self.buttons.clear()
        font = pygame.font.SysFont(None, 24)
        pygame.draw.rect(self.screen, (240, 240, 240), (self.size * self.cell_size, 0, 200, self.height))

        options = ["left_wall", "dijkstra", "a_star"]
        for i, algo in enumerate(options):
            color = (100, 200, 100) if algo == self.selected_algorithm else (200, 200, 200)
            rect = pygame.Rect(self.size * self.cell_size + 20, 30 + i * 50, 160, 40)
            pygame.draw.rect(self.screen, color, rect)
            label = font.render(algo.replace("_", " ").title(), True, (0, 0, 0))
            self.screen.blit(label, (rect.x + 10, rect.y + 10))
            self.buttons.append((rect, algo))

        control_labels = [("Play", "play"), ("Reset Maze", "reset"), ("Exit", "exit")]
        for i, (label, action) in enumerate(control_labels):
            rect = pygame.Rect(self.size * self.cell_size + 20, 250 + i * 60, 160, 40)
            pygame.draw.rect(self.screen, (180, 180, 250), rect)
            txt = font.render(label, True, (0, 0, 0))
            self.screen.blit(txt, (rect.x + 10, rect.y + 10))
            self.buttons.append((rect, action))


    def handle_click(self, pos):
        for rect, action in self.buttons:
            if rect.collidepoint(pos):
                if action in ("left_wall", "dijkstra", "a_star"):
                    print(f"Clicked: {action}")
                    self.selected_algorithm = action
                elif action == "play":
                    print(f"Clicked: {action}")
                    self.solve_maze()
                elif action == "reset":
                    print(f"Clicked: {action}")
                    self.reset_maze()
                elif action == "exit":
                    print(f"Clicked: {action}")
                    self.running = False

    def reset_maze(self):   
        self.builder = MazeBuilder(self.size)
        self.solver = MazeSolver(self.builder.get_grid(), (1, 1), (self.size - 2, self.size - 2))
        self.path = []
        self.path_iter = None
        self.maze_built = False
        self.clear_path()
        self._reset_requested = True  # <-- ADD THIS LINE

    def solve_maze(self):
        if not self.maze_built:
            return
        self.clear_path()
        self.prev_path_cell = None  # <-- Reset when solving a new maze
        try:
            self.solver.solve(self.selected_algorithm)
            self.path = self.solver.get_path()
            self.path_iter = iter(self.path)
        except Exception as e:
            print("Solver failed:", e)
            self.path = []
            self.path_iter = None


    def clear_path(self):
        grid = self.builder.get_grid()
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == 2:
                    grid[y][x] = 0

    def run(self):
        maze_gen = self.builder.dfs_iterative()
        grid = self.builder.get_grid()
        active_cell = None
        self._reset_requested = False

        while self.running:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            if getattr(self, "_reset_requested", False):
                maze_gen = self.builder.dfs_iterative()
                grid = self.builder.get_grid()
                active_cell = None
                self.maze_built = False
                self._reset_requested = False
                self.prev_path_cell = None 

            if not self.maze_built:
                try:
                    active_cell = next(maze_gen)
                except StopIteration:
                    active_cell = None
                    self.maze_built = True

            for y in range(self.size):
                for x in range(self.size):
                    color = (0, 0, 0) if grid[y][x] == 1 else (255, 255, 255)
                    if (y, x) == (1, 1):
                        color = (0, 0, 255)
                    elif (y, x) == (self.size - 2, self.size - 2):
                        color = (255, 0, 0)
                    elif grid[y][x] == 2:
                        color = (255, 215, 0)
                    elif active_cell == (y, x):
                        color = (0, 255, 0)
                    pygame.draw.rect(
                        self.screen,
                        color,
                        pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size),
                    )

            # Draw solved path live (with intermediate cells)
            if self.path_iter:
                try:
                    for _ in range(2):  # Draw two steps per frame for smoother animation
                        y, x = next(self.path_iter)
                        grid[y][x] = 2
                        if self.prev_path_cell:
                            py, px = self.prev_path_cell
                            # Fill in intermediate cell if not adjacent
                            if abs(py - y) + abs(px - x) > 1:
                                iy, ix = (py + y) // 2, (px + x) // 2
                                grid[iy][ix] = 2
                        self.prev_path_cell = (y, x)
                except StopIteration:
                    self.path_iter = None
                    self.prev_path_cell = None

            self.draw_sidebar()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
