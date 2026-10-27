
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

from src.maze import ROWS, COLS


def draw_maze(maze, start, goal, explored=None, path=None):
    """
    Draw the maze, explored cells, and final path.

    Cell colours:
    White  - open cell
    Dark   - wall
    Blue   - explored cell
    Yellow - final path
    Green  - start
    Red    - goal
    """

    display = maze.copy()

    explored = explored or []
    path = path or []

    # Mark cells visited by the search algorithm.
    for row, col in explored:
        if display[row, col] == 0:
            display[row, col] = 2

    # Mark the final route.
    for row, col in path:
        if (row, col) != start and (row, col) != goal:
            display[row, col] = 3

    # Keep start and goal visible.
    display[start] = 4
    display[goal] = 5

    # A restrained, easy-to-read colour palette.
    colors = [
        "#FFFFFF",  # Open cells
        "#454A45",  # Walls
        "#C7D9E8",  # Explored cells
        "#F0D77A",  # Final path
        "#64865B",  # Start
        "#C85D52",  # Goal
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    ax.imshow(
        display,
        cmap=ListedColormap(colors),
        vmin=0,
        vmax=5,
        interpolation="nearest",
    )

    # Draw a thin border around every cell.
    ax.set_xticks(np.arange(-0.5, COLS, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, ROWS, 1), minor=True)
    ax.grid(
        which="minor",
        color="#D9DDD7",
        linewidth=0.6,
    )

    ax.tick_params(
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )

    ax.set_title(
        "Maze search",
        fontsize=13,
        color="#292E27",
        pad=12,
    )

    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout(pad=1.0)
    return fig
