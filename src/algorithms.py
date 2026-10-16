
import heapq
from collections import deque

from src.maze import get_neighbors


def reconstruct_path(parent, goal):
    """Reconstruct the path from start to goal."""
    if goal not in parent:
        return []

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    return path[::-1]


def bfs(maze, start, goal):
    """
    Breadth-First Search.

    Explores cells level by level using a FIFO queue.
    Finds a shortest path when every move has equal cost.
    """
    queue = deque([start])
    parent = {start: None}
    explored = []

    while queue:
        current = queue.popleft()
        explored.append(current)

        if current == goal:
            break

        for neighbor in get_neighbors(current, maze):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)

    path = reconstruct_path(parent, goal)

    return explored, path


def heuristic(a, b):
    """
    Manhattan distance between two grid cells.

    h(n) = |row1 - row2| + |col1 - col2|
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(maze, start, goal):
    """
    A* Search.

    Uses f(n) = g(n) + h(n):
    g(n): cost from start to current cell
    h(n): estimated cost from current cell to goal
    """
    counter = 0

    # Priority queue entries: (f-score, counter, position)
    frontier = [
        (heuristic(start, goal), counter, start)
    ]

    parent = {start: None}
    g_score = {start: 0}
    explored = []
    closed = set()

    while frontier:
        _, _, current = heapq.heappop(frontier)

        # Ignore outdated duplicate entries
        if current in closed:
            continue

        closed.add(current)
        explored.append(current)

        if current == goal:
            break

        for neighbor in get_neighbors(current, maze):
            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(
                neighbor, float("inf")
            ):
                g_score[neighbor] = tentative_g
                parent[neighbor] = current

                counter += 1
                f_score = (
                    tentative_g + heuristic(neighbor, goal)
                )

                heapq.heappush(
                    frontier,
                    (f_score, counter, neighbor)
                )

    path = reconstruct_path(parent, goal)

    return explored, path
