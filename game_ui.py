import pygame
from maze_actions import MazeActions

class GameUI:
    def __init__(self, size=21, cell_size=30):
        pygame.init()
        self.size = size
        self.cell_size = cell_size
        self.width = size * cell_size + 200
        self.height = size * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Solver Visualizer")
        self.clock = pygame.time.Clock()
        self.running = True

        self.selected_algorithm = "left_wall"
        self.buttons = []
        self._reset_requested = False

        self.actions = MazeActions(size)  # Renamed for clarity
        self.maze_gen = self.actions.builder.dfs_iterative()
        self.active_cell = None

    def draw_sidebar(self):
        self.buttons.clear()
        font = pygame.font.SysFont(None, 24)
        pygame.draw.rect(self.screen, (240, 240, 240), (self.size * self.cell_size, 0, 200, self.height))

        algorithms = ["left_wall", "dijkstra", "a_star"]
        for i, algo in enumerate(algorithms):
            color = (100, 200, 100) if algo == self.selected_algorithm else (200, 200, 200)
            rect = pygame.Rect(self.size * self.cell_size + 20, 30 + i * 50, 160, 40)
            pygame.draw.rect(self.screen, color, rect)
            label = font.render(algo.replace("_", " ").title(), True, (0, 0, 0))
            self.screen.blit(label, (rect.x + 10, rect.y + 10))
            self.buttons.append((rect, algo))

        controls = [("Play", "play"), ("Reset Maze", "reset"), ("Exit", "exit")]
        for i, (label, action) in enumerate(controls):
            rect = pygame.Rect(self.size * self.cell_size + 20, 250 + i * 60, 160, 40)
            pygame.draw.rect(self.screen, (180, 180, 250), rect)
            txt = font.render(label, True, (0, 0, 0))
            self.screen.blit(txt, (rect.x + 10, rect.y + 10))
            self.buttons.append((rect, action))

    def handle_click(self, pos):
        for rect, action in self.buttons:
            if rect.collidepoint(pos):
                if action in ("left_wall", "dijkstra", "a_star"):
                    self.selected_algorithm = action
                elif action == "play":
                    self.actions.solve(self.selected_algorithm)
                elif action == "reset":
                    self._reset_requested = True
                elif action == "exit":
                    self.running = False

    def draw_grid(self):
        grid = self.actions.get_grid()
        for y in range(self.size):
            for x in range(self.size):
                color = (0, 0, 0) if grid[y][x] == 1 else (255, 255, 255)
                if (y, x) == (1, 1):
                    color = (0, 0, 255)
                elif (y, x) == (self.size - 2, self.size - 2):
                    color = (255, 0, 0)
                elif grid[y][x] == 2:
                    color = (255, 215, 0)
                elif self.active_cell == (y, x):
                    color = (0, 255, 0)
                pygame.draw.rect(self.screen, color, pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def run(self):
        while self.running:
            self.screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            if self._reset_requested:
                self.actions.reset()
                self.maze_gen = self.actions.builder.dfs_iterative()
                self.active_cell = None
                self._reset_requested = False

            if not self.actions.maze_built:
                try:
                    self.active_cell = next(self.maze_gen)
                except StopIteration:
                    self.active_cell = None
                    self.actions.maze_built = True

            for yx in self.actions.get_next_path_steps():
                y, x = yx
                self.actions.get_grid()[y][x] = 2

            self.draw_grid()
            self.draw_sidebar()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
