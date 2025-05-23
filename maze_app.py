import pygame
class MazeApp:
    def __init__(self, builder, solver, cell_size=6):
        pygame.init()
        self.builder = builder
        self.solver = solver
        self.cell_size = cell_size
        self.size = builder.size
        self.start = solver.start if solver else (1,1)
        self.end = solver.end if solver else (self.size -2, self.size -2)
        self.grid = builder.get_grid()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.size * cell_size, self.size * cell_size))
        pygame.display.set_caption("Maze App")


    def draw_grid(self, active_x=None, active_y=None):
        for y in range(self.size):
            for x in range(self.size):
                color = (0,0,0) if self.grid[y][x]==1 else (255,255,255)
                if (y,x)==self.start:
                    color = (0,0,255)
                elif (y,x)==self.end:
                    color = (255,0,0)
                elif active_y==y and active_x==x:
                    color = (0,255,0)
                elif self.grid[y][x]==2:
                    color = (210,204,0)
                rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)

    def run_game(self, generator):
        running = True
        active_y, active_x = None, None
        while running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
            self.screen.fill((0,0,0))
            try:
                yx = next(generator)
                if yx:
                    active_y, active_x = yx
            except StopIteration:
                active_y, active_x = None, None
            self.draw_grid(active_x, active_y)
            pygame.display.flip()
            self.clock.tick(150)

    def path_generator(self, path):
        for i in range(1, len(path)):
            prev_y, prev_x = path[i-1]
            y, x = path[i]
            mid_y, mid_x = (prev_y + y)//2, (prev_x + x)//2
            self.grid[mid_y][mid_x] = 2
            self.grid[y][x] = 2
            yield y, x

    def run(self):
        self.run_game(self.builder.dfs_iterative())
        path = self.solver.get_path()
        self.run_game(self.path_generator(path))
        pygame.quit()
