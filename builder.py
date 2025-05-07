import pygame
import random

def draw_grid(screen, grid, cell_size, active_x=None, active_y=None, start=None, end=None):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            color = (0, 0, 0) if grid[y][x] == 1 else (255, 255, 255)
            if (y, x) == start:
                color = (0, 0, 255)  # blue start
            elif (y, x) == end:
                color = (255, 0, 0)  # red end
            elif active_y == y and active_x == x:
                color = (0, 255, 0)  # green active cell
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)

def create_grid(size):
    grid = [[1 for _ in range(size)] for _ in range(size)]
    for i in range(1, size, 2):
        for j in range(1, size, 2):
            grid[i][j] = 0
    return grid

def run_game(screen, grid, cell_size, generator, start, end, clock):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        try:
            yx = next(generator)
            if yx:
                active_y, active_x = yx
        except StopIteration:
            active_y, active_x = None, None

        draw_grid(screen, grid, cell_size, active_x, active_y, start, end)
        pygame.display.flip()
        clock.tick(160)
    pygame.quit()


def dfs(grid, visited, y, x):
    visited[y][x] = True
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # up, down, left, right
    random.shuffle(directions)

    for dy, dx in directions:
        ny, nx = y + dy, x + dx
        if 1 <= ny < len(grid)-1 and 1 <= nx < len(grid[0])-1 and not visited[ny][nx]:
            grid[(y + ny)//2][(x + nx)//2] = 0  # knock down wall
            yield y,x
            yield from dfs(grid, visited, ny, nx)


def main():
    pygame.init()
    size = 51
    cell_size = 20
    start = (1, 1)
    end = (size - 2, size - 2)
    grid = create_grid(size)
    visited = [[False for _ in range(size)] for _ in range(size)]
    generator = dfs(grid, visited, 1, 1)
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((size * cell_size, size * cell_size))
    pygame.display.set_caption("Maze Builder")
    run_game(screen, grid, cell_size, generator, start, end, clock)

if __name__ == "__main__":
    main()
