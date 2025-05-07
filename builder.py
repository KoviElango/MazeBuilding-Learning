# builder.py
# This module contains a function to build a graph and perform DFS on it.

import matplotlib.pyplot as plt
import numpy as np

def mazebuilder():
    maze = [
    [1, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1]
    ]

    maze[0][0] = 2
    maze[-1][-1] = 3


    fig, ax = plt.subplots()
    ax.imshow(maze, cmap="gray_r")

    maze_array = np.array(maze)
    
    start_y, start_x = np.where(maze_array == 2)
    end_y, end_x = np.where(maze_array == 3)

    # Clean up the axis
    ax.set_title("Maze")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

    ax.plot(start_x, start_y, 'go')
    ax.plot(end_x, end_y, 'ro')

    plt.show()

mazebuilder()
