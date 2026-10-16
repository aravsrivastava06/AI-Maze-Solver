
import random
import numpy as np

# Maze configuration
ROWS = 15
COLS = 20

# Starting and destination positions (row, column)
START = (0, 0)
GOAL = (ROWS - 1, COLS - 1)

# Probability of a cell becoming a wall
WALL_PROBABILITY = 0.28


def generate_maze():
    """
    Generate a random maze.

    0 represents an empty cell.
    1 represents a wall.

    An open route is guaranteed along the top row
    and the rightmost column.
    """
    maze = np.zeros((ROWS, COLS), dtype=int)

    # Randomly place walls
    for row in range(ROWS):
        for col in range(COLS):
            if random.random() < WALL_PROBABILITY:
                maze[row, col] = 1

    # Ensure start and goal are open
    maze[START] = 0
    maze[GOAL] = 0

    # Guarantee a route from START to GOAL
    maze[0, :] = 0
    maze[:, COLS - 1] = 0

    return maze


def get_neighbors(position, maze):
    """
    Return valid neighboring cells.

    Movement is allowed up, down, left, and right.
    Walls and out-of-bounds cells are excluded.
    """
    row, col = position

    directions = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1),   # Right
    ]

    neighbors = []

    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc

        # Check grid boundaries
        if (
            0 <= new_row < ROWS
            and 0 <= new_col < COLS
        ):
            # Only allow movement through empty cells
            if maze[new_row, new_col] == 0:
                neighbors.append((new_row, new_col))

    return neighbors
