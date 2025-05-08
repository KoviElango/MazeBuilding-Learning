from maze_builder import MazeBuilder
from maze_solver import MazeSolver
from maze_app import MazeApp

import pygame

if __name__ == "__main__":
    size = 51
    builder = MazeBuilder(size)
    app = MazeApp(builder, None, cell_size=10)
    
    # Build the maze and visualize it
    app.run_game(builder.dfs_iterative())
    
    # Solve the maze
    solver = MazeSolver(builder.get_grid(), start=(1,1), end=(size-2, size-2))
    try:
        solver.solve_left_wall()
    except ValueError as e:
        print("Solver failed:", e)
        exit()
    
    # Update app with solver and show solution
    app.solver = solver
    app.run_game(app.path_generator(solver.get_path()))
    
    pygame.quit()
