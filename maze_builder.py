import pygame
import random

class MazeBuilder:
    def __init__(self, size):
        self.size = size
        self.grid = self.create_grid()
        self.visited = [[False for _ in range(size)] for _ in range(size)]

    def create_grid(self):
        grid = [[1 for _ in range(self.size)] for _ in range(self.size)]
        for i in range(1, self.size, 2):
            for j in range(1, self.size, 2):
                grid[i][j] = 0
        return grid

    def dfs_iterative(self, start_y=1, start_x=1):
        stack = [(start_y, start_x)]
        directions = [(-2,0), (2,0), (0,-2), (0,2)]

        self.visited[start_y][start_x] = True
        while stack:
            y, x = stack.pop()
            yield y, x
            random.shuffle(directions)
            for dy, dx in directions:
                ny, nx = y + dy, x + dx
                between_y, between_x = (y + ny)//2, (x + nx)//2
                if 1 <= ny < self.size-1 and 1 <= nx < self.size-1 and not self.visited[ny][nx]:
                    self.visited[ny][nx] = True
                    self.grid[between_y][between_x] = 0
                    stack.append((ny, nx))

    def get_grid(self):
        return self.grid