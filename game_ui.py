import pygame
from maze_actions import MazeActions

class GameUI:
    SIDEBAR_WIDTH = 200
    ALGORITHMS = ["left_wall", "dijkstra", "a_star", "dfs_backtracking"]
    CONTROL_BUTTONS = [("Play", "play"), ("Reset Maze", "reset"), ("Exit", "exit")]

    def __init__(self, size=21, cell_size=20):
        pygame.init()
        self.size = size
        self.cell_size = cell_size
        self.width = size * cell_size + self.SIDEBAR_WIDTH
        self.height = size * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Solver Visualizer")
        self.clock = pygame.time.Clock()
        self.running = True

        self.selected_algorithm = "left_wall"
        self.buttons = []
        self._reset_requested = False

        self.actions = MazeActions(size)
        self.maze_gen = self.actions.builder.build()
        self.active_cell = None

    # Event Handling

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)

    def handle_click(self, pos):
        for rect, action in self.buttons:
            if rect.collidepoint(pos):
                if action in self.ALGORITHMS:
                    self.selected_algorithm = action
                elif action == "play":
                    self.actions.solve(self.selected_algorithm)
                elif action == "reset":
                    self._reset_requested = True
                elif action == "exit":
                    self.running = False

    # Drawing

    def draw_ui(self):
        self.screen.fill((255, 255, 255))
        self.draw_grid()
        self.draw_sidebar()
        pygame.display.flip()

    def draw_sidebar(self):
        self.buttons.clear()
        font = pygame.font.SysFont(None, 24)
        pygame.draw.rect(self.screen, (240, 240, 240), (self.size * self.cell_size, 0, self.SIDEBAR_WIDTH, self.height))
        self.draw_algorithm_buttons(font)
        self.draw_control_buttons(font)

    def draw_algorithm_buttons(self, font):
        for i, algo in enumerate(self.ALGORITHMS):
            color = (100, 200, 100) if algo == self.selected_algorithm else (200, 200, 200)
            rect = pygame.Rect(self.size * self.cell_size + 20, 30 + i * 50, 160, 40)
            pygame.draw.rect(self.screen, color, rect)
            label = font.render(algo.replace("_", " ").title(), True, (0, 0, 0))
            self.screen.blit(label, (rect.x + 10, rect.y + 10))
            self.buttons.append((rect, algo))

    def draw_control_buttons(self, font):
        for i, (label, action) in enumerate(self.CONTROL_BUTTONS):
            rect = pygame.Rect(self.size * self.cell_size + 20, 250 + i * 60, 160, 40)
            pygame.draw.rect(self.screen, (180, 180, 250), rect)
            txt = font.render(label, True, (0, 0, 0))
            self.screen.blit(txt, (rect.x + 10, rect.y + 10))
            self.buttons.append((rect, action))

    def draw_grid(self):
        grid = self.actions.get_grid()
        for y in range(self.size):
            for x in range(self.size):
                color = self.get_cell_color(x, y, grid)
                self.draw_cell(x, y, color)

    def draw_cell(self, x, y, color):
        pygame.draw.rect(
            self.screen,
            color,
            pygame.Rect(
                x * self.cell_size,
                y * self.cell_size,
                self.cell_size,
                self.cell_size
            )
        )

    def get_cell_color(self, x, y, grid):
        if (y, x) == (1, 1):  # Start
            return (0, 0, 255)
        elif (y, x) == (self.size - 2, self.size - 2):  # End
            return (255, 0, 0)
        elif grid[y][x] == 1:  # Wall
            return (0, 0, 0)
        elif grid[y][x] == 2:  # Solved Path
            return (255, 215, 0)
        elif self.active_cell == (y, x):  # Current Maze Gen
            return (0, 255, 0)
        return (255, 255, 255)  # Empty

    # Maze State Management

    def process_reset(self):
        if self._reset_requested:
            self.actions.reset()
            self.maze_gen = self.actions.builder.dfs_iterative()
            self.active_cell = None
            self._reset_requested = False

    def generate_maze_step(self):
        if not self.actions.maze_built:
            try:
                self.active_cell = next(self.maze_gen)
            except StopIteration:
                self.active_cell = None
                self.actions.maze_built = True

    def animate_solver_path(self):
        for yx in self.actions.get_next_path_steps():
            y, x = yx
            self.actions.get_grid()[y][x] = 2

    # Main Loop

    def run(self):
        while self.running:
            self.handle_events()
            self.process_reset()
            self.generate_maze_step()
            self.animate_solver_path()
            self.draw_ui()
            self.clock.tick(60)

        pygame.quit()
