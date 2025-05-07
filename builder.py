import pygame
import random

def draw_grid(screen, grid, cell_size):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            color = (0, 0, 0) if grid[y][x] == 1 else (255, 255, 255)
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)

def create_grid(size):
    grid = [[1 for _ in range(size)] for _ in range(size)]
    for i in range(1, size, 2):
        for j in range(1, size, 2):
            grid[i][j] = 0
    return grid

def run_game(screen, grid, cell_size, generator):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        try:
            next(generator)
        except StopIteration:
            pass
        draw_grid(screen, grid, cell_size)
        pygame.display.flip()
    pygame.quit()


def dfs(grid, visited, y, x):
    visited[y][x] = True
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # up, down, left, right
    random.shuffle(directions)

    for dy, dx in directions:
        ny, nx = y + dy, x + dx
        if 1 <= ny < len(grid)-1 and 1 <= nx < len(grid[0])-1 and not visited[ny][nx]:
            grid[(y + ny)//2][(x + nx)//2] = 0  # knock down wall
            yield
            yield from dfs(grid, visited, ny, nx)


def main():
    pygame.init()
    size = 21
    cell_size = 20
    grid = create_grid(size)
    visited = [[False for _ in range(size)] for _ in range(size)]
    generator = dfs(grid, visited, 1, 1)

    screen = pygame.display.set_mode((size * cell_size, size * cell_size))
    pygame.display.set_caption("Maze Builder")
    run_game(screen, grid, cell_size, generator)

if __name__ == "__main__":
    main()
