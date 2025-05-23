from maze_builder import MazeBuilder
from maze_solver_algo import MazeSolver
from maze_app import MazeApp
import pygame

def clear_path_marks(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 2:
                grid[y][x] = 0

if __name__ == "__main__":
    size = 21
    builder = MazeBuilder(size)
    app = MazeApp(builder, None, cell_size=30)

    # Build maze
    app.run_game(builder.dfs_iterative())

    # Left wall solver
    solver = MazeSolver(builder.get_grid(), start=(1, 1), end=(size - 2, size - 2))
    try:
        solver.solve("left_wall")
        print("Left Wall path length:", len(solver.get_path()))
        app.solver = solver
        app.run_game(app.path_generator(solver.get_path()))
    except ValueError as e:
        print("Left Wall Solver failed:", e)

    # Dijkstra solver
    clear_path_marks(builder.get_grid())
    solver.solve("dijkstra")
    print("Dijkstra path length:", len(solver.get_path()))
    app.run_game(app.path_generator(solver.get_path()))

    pygame.quit()
