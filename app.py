
import time

import pandas as pd
import streamlit as st

from src.maze import generate_maze, START, GOAL, ROWS, COLS
from src.algorithms import bfs, astar
from src.visualization import draw_maze


# --------------------------------------------------
# Page setup
# --------------------------------------------------

st.set_page_config(
    page_title="AI Maze Solver",
    page_icon="assets/maze-icon.png",
    layout="wide",
)

# --------------------------------------------------
# Session state
# --------------------------------------------------

if "maze" not in st.session_state:
    st.session_state.maze = generate_maze()

if "result" not in st.session_state:
    st.session_state.result = None

if "comparison" not in st.session_state:
    st.session_state.comparison = None


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def solve_maze(algorithm_name, maze, animate=False, delay=0.02):
    """Run a search algorithm and optionally animate its exploration."""

    search_function = bfs if algorithm_name == "BFS" else astar

    start_time = time.perf_counter()
    explored, path = search_function(maze, START, GOAL)
    elapsed_time = time.perf_counter() - start_time

    # Animate the cells explored by the algorithm.
    if animate:
        maze_placeholder = st.empty()
        progress = st.progress(0)
        status = st.empty()

        total = max(len(explored), 1)

        # Limit redraws for large searches while retaining the final result.
        update_every = max(1, total // 100)

        for i in range(0, len(explored), update_every):
            visible_explored = explored[:i + update_every]

            fig = draw_maze(
                maze,
                START,
                GOAL,
                explored=visible_explored,
            )
            maze_placeholder.pyplot(fig, width="stretch")
            import matplotlib.pyplot as plt
            plt.close(fig)

            progress.progress(min(len(visible_explored) / total, 1.0))
            status.caption(
                f"Explored {min(len(visible_explored), total)} "
                f"of {len(explored)} cells"
            )

            if delay > 0:
                time.sleep(delay)

        progress.empty()
        status.empty()

    return {
        "algorithm": algorithm_name,
        "explored": explored,
        "path": path,
        "nodes": len(explored),
        "path_length": len(path) - 1 if path else None,
        "time": elapsed_time,
        "found": bool(path),
    }


def show_maze(maze, explored=None, path=None):
    """Render and release the Matplotlib figure."""

    import matplotlib.pyplot as plt

    fig = draw_maze(
        maze,
        START,
        GOAL,
        explored=explored,
        path=path,
    )
    st.pyplot(fig, width="stretch")
    plt.close(fig)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------


with st.sidebar:
    icon_col, title_col = st.columns([1, 4])

    with icon_col:
        st.image("assets/maze-icon.png", width=48)

    with title_col:
        st.markdown(
            """
            <div style="padding-top: 5px; font-size: 21px;
                        font-weight: 700; white-space: nowrap;">
                AI Maze Solver
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption("A small project exploring pathfinding algorithms.")
    st.divider()


    st.subheader("Controls")

    algorithm = st.selectbox(
        "Search algorithm",
        ["A*", "BFS"],
        help="Choose which algorithm should find a route.",
    )

    animate = st.checkbox(
        "Animate the search",
        value=True,
    )

    delay = st.slider(
        "Animation speed",
        min_value=0.00,
        max_value=0.10,
        value=0.02,
        step=0.01,
        help="Time to pause between animation updates.",
    )

    st.caption(f"Grid size: {ROWS} rows × {COLS} columns")

    st.divider()

    solve_clicked = st.button(
        "Solve maze",
        type="primary",
        use_container_width=True,
    )

    compare_clicked = st.button(
        "Compare BFS and A*",
        use_container_width=True,
    )

    new_maze_clicked = st.button(
        "Generate new maze",
        use_container_width=True,
    )

    st.divider()

    st.subheader("Legend")

    st.markdown(
        """
        <span style="color:#64865B;">■</span> Start<br>
        <span style="color:#C85D52;">■</span> Destination<br>
        <span style="color:#454A45;">■</span> Wall<br>
        <span style="color:#C7D9E8;">■</span> Explored cell<br>
        <span style="color:#F0D77A;">■</span> Final path
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# Handle actions
# --------------------------------------------------

if new_maze_clicked:
    st.session_state.maze = generate_maze()
    st.session_state.result = None
    st.session_state.comparison = None

if solve_clicked:
    st.session_state.comparison = None

    with st.spinner(f"Running {algorithm}..."):
        st.session_state.result = solve_maze(
            algorithm,
            st.session_state.maze,
            animate=animate,
            delay=delay,
        )

if compare_clicked:
    st.session_state.result = None
    comparison_results = []

    for name, function in [("BFS", bfs), ("A*", astar)]:
        start_time = time.perf_counter()
        explored, path = function(
            st.session_state.maze,
            START,
            GOAL,
        )
        elapsed = time.perf_counter() - start_time

        comparison_results.append({
            "Algorithm": name,
            "Nodes explored": len(explored),
            "Path length": len(path) - 1 if path else "No path",
            "Time (ms)": round(elapsed * 1000, 3),
            "Path found": "Yes" if path else "No",
        })

    st.session_state.comparison = comparison_results


# --------------------------------------------------
# Main page
# --------------------------------------------------

st.title("AI Maze Solver")

st.markdown(
    """
    I built this app to see how two search algorithms find their way
    through a maze. Choose an algorithm, watch the search, and compare
    the route it finds with the other approach.
    """
)

st.divider()

maze_column, results_column = st.columns(
    [1.8, 1],
    gap="large",
)

with maze_column:
    st.subheader("The maze")
    st.caption(
        "The green cell is the start, the red cell is the destination, "
        "and the yellow cells show the route when one is found."
    )

    result = st.session_state.result

    if result is None:
        show_maze(st.session_state.maze)
    else:
        show_maze(
            st.session_state.maze,
            explored=result["explored"],
            path=result["path"],
        )

with results_column:
    st.subheader("Results")

    result = st.session_state.result

    if result is None:
        st.info("Solve the maze to see the results.")

        st.metric("Cells explored", "—")
        st.metric("Path length", "—")
        st.metric("Search time", "—")

    else:
        if result["found"]:
            st.success(f"{result['algorithm']} found a route.")
        else:
            st.warning("No route to the destination was found.")

        st.metric(
            "Cells explored",
            result["nodes"],
        )

        st.metric(
            "Path length",
            result["path_length"]
            if result["path_length"] is not None
            else "No path",
        )

        st.metric(
            "Search time",
            f"{result['time'] * 1000:.3f} ms",
        )

        if result["found"]:
            st.caption(
                "Path length counts the number of moves between cells, "
                "not the number of cells in the route."
            )

st.divider()


# --------------------------------------------------
# Algorithm comparison
# --------------------------------------------------

st.subheader("BFS vs. A*")

st.write(
    "Both algorithms search for a route, but they decide which cell "
    "to explore next differently."
)

if st.session_state.comparison is not None:
    comparison_df = pd.DataFrame(st.session_state.comparison)

    st.dataframe(
        comparison_df,
        hide_index=True,
        use_container_width=True,
    )

    st.caption(
        "Execution times vary between runs. For this small maze, "
        "differences of a few milliseconds may not be meaningful."
    )
else:
    st.caption(
        "Select **Compare BFS and A*** in the sidebar to run both "
        "algorithms on the same maze."
    )


# --------------------------------------------------
# Short explanation
# --------------------------------------------------

with st.expander("How do the algorithms work?"):
    st.markdown(
        """
        **Breadth-First Search (BFS)**

        BFS explores cells level by level using a queue. When every
        move has the same cost, it finds a shortest path if one exists.
        It may explore many cells before reaching the destination.

        **A* Search**

        A* uses a priority queue to choose promising cells. It combines
        the distance already travelled with a heuristic estimate of
        the remaining distance. Here, the heuristic is Manhattan
        distance, which suits movement up, down, left, and right.

        **What to look for**

        - Compare how many cells each algorithm explores.
        - Check whether both find a route of the same length.
        - Compare execution times, keeping in mind that small timing
          differences can be caused by normal system overhead.
        """
    )

st.divider()

st.caption(
    "Built with Python, Streamlit, NumPy and Matplotlib."
)
