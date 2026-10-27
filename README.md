# AI Maze Solver

A small micro Python project that explores how search algorithms can find a path through a maze.

I built this project to understand how **Breadth-First Search (BFS)** and **A* Search** work in practice. Instead of only looking at the algorithms in code, this app lets you watch them explore a maze and compare their results.

**Live demo:** https://ai-maze-solver-arav.streamlit.app/

## What does it do?

The app generates a random maze with a starting point and a destination. You can choose a search algorithm, watch its exploration, and see whether it finds a route.

Here are the main features:

- **Random maze generation:** Create a new maze whenever you want to try another layout.
- **BFS search:** Explore cells level by level to find a shortest path.
- **A* search:** Use a heuristic to prioritize cells that appear closer to the destination.
- **Search animation:** Watch the algorithm explore the maze step by step.
- **Performance comparison:** Compare the number of cells explored, path length, and execution time for BFS and A*.
- **Visual results:** See the explored cells and the final route directly on the grid.

## A quick look at the project

The maze is displayed as a grid of open cells and walls.

| Colour | Meaning |

| Green | Starting point |
| Red | Destination |
| Dark grey | Wall |
| Light blue | Explored cell |
| Yellow | Final path |

The goal is to move from the top-left corner to the bottom-right corner without passing through walls.

## Algorithms used

### 1. Breadth-First Search (BFS)

BFS explores neighbouring cells level by level using a queue. Since every move has the same cost, it finds a shortest path whenever a route exists.

It is useful as a baseline for understanding how an uninformed search algorithm explores a maze.

### 2. A* Search

A* uses a priority queue to decide which cell to explore next. It considers both the distance travelled so far and an estimate of the distance remaining.

This project uses **Manhattan distance** as its heuristic:

`h(n) = |row - goal_row| + |column - goal_column|`

Because movement is limited to up, down, left, and right, Manhattan distance is a suitable heuristic for this grid.

### What I wanted to compare

I wanted to see whether A* could reach the destination while exploring fewer cells than BFS. The results depend on the maze layout, so neither algorithm should be assumed to explore fewer cells in every possible case.

## Tech Stack

- **Python** — implementing the search algorithms and application logic
- **Streamlit** — building the interactive web interface
- **NumPy** — representing the maze as a grid
- **Matplotlib** — drawing the maze and visualizing the search
- **Pandas** — displaying the algorithm comparison in a table
- **Git and GitHub** — version control and source code hosting
- **Streamlit Community Cloud** — deploying the app

## Running the project locally

If you want to run the project on your own machine, follow these steps.

### 1. Clone the repository

```bash
git clone https://github.com/aravsrivastava06/AI-Maze-Solver.git
cd AI-Maze-Solver
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

Streamlit will print a local URL in the terminal. Open that URL in your browser to use the app.

## Project structure

```text
AI-Maze-Solver/
├── .streamlit/
│   └── config.toml
├── assets/
│   └── maze-icon.png
├── src/
│   ├── __init__.py
│   ├── algorithms.py
│   ├── maze.py
│   └── visualization.py
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

- `app.py` contains the Streamlit interface, controls, results, and comparison logic.
- `src/maze.py` generates the maze and identifies valid neighbouring cells.
- `src/algorithms.py` implements BFS and A* and reconstructs the route.
- `src/visualization.py` draws the grid, explored cells, and final path.
- `assets/maze-icon.png` contains the custom project icon.
- `.streamlit/config.toml` defines the app's theme.
- `requirements.txt` lists the Python packages needed to run the project.

## Things I learned

Working on this project helped me connect search algorithms with a visual example. It also gave me practice with Python modules, priority queues, queues, grid-based problems, basic data visualization, and building a small interactive application with Streamlit.

One thing worth remembering when comparing the results is that execution time can vary between runs. For a relatively small maze, a tiny timing difference does not necessarily indicate a meaningful performance improvement.

## Possible improvements

There are a few things I would like to explore further:

- Add more search algorithms, such as Depth-First Search and Dijkstra's algorithm.
- Let users draw their own walls and choose the start and destination.
- Allow users to change the maze size.
- Improve the animation controls.
- Run more experiments on different maze layouts to compare search performance.

## Try it out

You can use the deployed version here:

**https://ai-maze-solver-arav.streamlit.app/**


