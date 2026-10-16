
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

from src.maze import ROWS, COLS


def draw_maze(maze, start, goal, explored=None, path=None):
    """
    Draw the maze using colors.

    Empty = white
    Wall = dark
    Explored = blue
    Solution path = yellow
    Start = green
    Goal = red
    """
    display = maze.copy()

    explored = explored or []
    path = path or []

    # Mark explored cells
    for row, col in explored:
        if display[row, col] == 0:
            display[row, col] = 2

    # Mark the final path
    for row, col in path:
        if (row, col) != start and (row, col) != goal:
            display[row, col] = 3

    # Start and goal must remain visible
    display[start] = 4
    display[goal] = 5

    colors = [
        "#F8FAFC",  # 0: Empty
        "#1E293B",  # 1: Wall
        "#93C5FD",  # 2: Explored
        "#FACC15",  # 3: Final path
        "#22C55E",  # 4: Start
        "#EF4444",  # 5: Goal
    ]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.imshow(
        display,
        cmap=ListedColormap(colors),
        vmin=0,
        vmax=5,
    )

    ax.set_xticks(np.arange(-0.5, COLS, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, ROWS, 1), minor=True)

    ax.grid(
        which="minor",
        color="#CBD5E1",
        linewidth=0.5,
    )

    ax.tick_params(
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )

    ax.set_title("AI Maze Search Visualization")
    fig.tight_layout()

    return fig
