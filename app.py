
import time

import matplotlib.pyplot as plt
import streamlit as st

from src.maze import generate_maze, START, GOAL, ROWS, COLS
from src.algorithms import bfs, astar
from src.visualization import draw_maze

# PAGE CONFIGURATION

st.set_page_config(
    page_title="AI Maze Solver | Intelligent Search",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded",
)

# PREMIUM DARK UI

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 10% 0%,
                rgba(79, 70, 229, 0.17), transparent 38%),
            radial-gradient(ellipse at 90% 15%,
                rgba(6, 182, 212, 0.10), transparent 35%),
            #0b1020;
        color: #e5e7eb;
    }

    [data-testid="stHeader"] {
        background: rgba(11, 16, 32, 0.8);
    }

    [data-testid="stSidebar"] {
        background: #10172a;
        border-right: 1px solid rgba(148, 163, 184, 0.15);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f8fafc;
    }

    h1, h2, h3 {
        color: #f8fafc !important;
        letter-spacing: -0.5px;
    }

    p, label, li {
        color: #cbd5e1;
    }

    .hero {
        padding: 28px 30px;
        border-radius: 22px;
        background: linear-gradient(
            120deg,
            rgba(79, 70, 229, 0.28),
            rgba(8, 145, 178, 0.15),
            rgba(15, 23, 42, 0.75)
        );
        border: 1px solid rgba(129, 140, 248, 0.30);
        margin-bottom: 22px;
    }

    .hero-eyebrow {
        color: #67e8f9;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .hero-title {
        font-size: clamp(28px, 4vw, 43px);
        font-weight: 800;
        line-height: 1.15;
        color: #ffffff;
        margin-bottom: 12px;
    }

    .hero-description {
        color: #cbd5e1;
        font-size: 15px;
        line-height: 1.7;
        max-width: 760px;
    }

    .section-label {
        color: #67e8f9;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.6px;
        text-transform: uppercase;
        margin: 10px 0 8px 0;
    }

    .metric-card {
        background: linear-gradient(
            145deg,
            rgba(30, 41, 59, 0.94),
            rgba(15, 23, 42, 0.96)
        );
        border: 1px solid rgba(148, 163, 184, 0.19);
        border-radius: 16px;
        padding: 18px 18px 16px 18px;
        min-height: 112px;
        margin-bottom: 12px;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        margin-bottom: 10px;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 27px;
        font-weight: 800;
        line-height: 1.25;
        overflow-wrap: anywhere;
    }

    .metric-hint {
        color: #67e8f9;
        font-size: 12px;
        margin-top: 7px;
    }

    .panel {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 18px;
        padding: 18px;
    }

    .status-pill {
        display: inline-block;
        padding: 6px 11px;
        border-radius: 999px;
        background: rgba(34, 197, 94, 0.13);
        border: 1px solid rgba(74, 222, 128, 0.3);
        color: #86efac;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .legend-item {
        color: #cbd5e1;
        font-size: 13px;
        padding: 5px 0;
    }

    div.stButton > button {
        border-radius: 11px;
        min-height: 43px;
        font-weight: 700;
        border: 1px solid rgba(129, 140, 248, 0.32);
        transition: all 0.2s ease;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(100deg, #4f46e5, #0891b2);
        color: white;
        border: none;
    }

    div.stButton > button:hover {
        border-color: #67e8f9;
        transform: translateY(-1px);
    }

    [data-testid="stDataFrame"] {
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #6366f1, #22d3ee);
    }

    hr {
        border-color: rgba(148, 163, 184, 0.16);
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# REUSABLE METRIC CARD

def metric_card(label, value, hint=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-hint">{hint}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# SESSION STATE

if "maze" not in st.session_state:
    st.session_state.maze = generate_maze()

if "results" not in st.session_state:
    st.session_state.results = {}

if "animate_algorithm" not in st.session_state:
    st.session_state.animate_algorithm = None


# HERO HEADER

st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">
            Artificial Intelligence · Search Algorithms
        </div>
        <div class="hero-title">
            Navigate the Maze.<br>Understand the Intelligence.
        </div>
        <div class="hero-description">
            Explore how Breadth-First Search and A* Search
            navigate a maze, discover possible routes, and find
            a path to the destination. Watch the exploration
            unfold and compare algorithm performance.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# SIDEBAR

with st.sidebar:
    st.markdown("## 🧩 Maze Controls")
    st.caption("Configure your search experiment.")

    algorithm = st.selectbox(
        "Search algorithm",
        ["A*", "BFS"],
    )

    animation_delay = st.slider(
        "Animation delay (seconds)",
        min_value=0.01,
        max_value=0.10,
        value=0.03,
        step=0.01,
        help="Smaller values make the animation faster.",
    )

    st.caption(
        f"Grid dimensions: {ROWS} rows × {COLS} columns"
    )

    st.divider()

    if st.button(
        "▶  Solve Maze",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.animate_algorithm = algorithm
        st.rerun()

    if st.button(
        "⚖️  Compare BFS vs A*",
        use_container_width=True,
    ):
        maze_copy = st.session_state.maze.copy()

        for name, search_function in [
            ("BFS", bfs),
            ("A*", astar),
        ]:
            start_time = time.perf_counter()

            explored, path = search_function(
                maze_copy, START, GOAL
            )

            elapsed_ms = (
                time.perf_counter() - start_time
            ) * 1000

            st.session_state.results[name] = {
                "explored": explored,
                "path": path,
                "time_ms": elapsed_ms,
            }

        st.session_state.animate_algorithm = None
        st.rerun()

    if st.button(
        "🔄  Generate New Maze",
        use_container_width=True,
    ):
        st.session_state.maze = generate_maze()
        st.session_state.results = {}
        st.session_state.animate_algorithm = None
        st.rerun()

    st.divider()

    st.markdown("### Maze Legend")

    st.markdown(
        """
        <div class="legend-item">🟩 &nbsp; Starting point</div>
        <div class="legend-item">🟥 &nbsp; Goal / destination</div>
        <div class="legend-item">⬛ &nbsp; Obstacle / wall</div>
        <div class="legend-item">🟦 &nbsp; Explored cell</div>
        <div class="legend-item">🟨 &nbsp; Final path</div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.caption(
        "Built with Python, Streamlit, NumPy and Matplotlib."
    )

# SEARCH ANIMATION

animate_algorithm = st.session_state.animate_algorithm

if animate_algorithm is not None:
    st.session_state.animate_algorithm = None

    maze = st.session_state.maze.copy()

    search_function = (
        bfs if animate_algorithm == "BFS" else astar
    )

    st.markdown(
        f'<div class="section-label">'
        f'LIVE SEARCH · {animate_algorithm}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Compute the search order first.
    start_time = time.perf_counter()

    explored, path = search_function(
        maze, START, GOAL
    )

    elapsed_ms = (
        time.perf_counter() - start_time
    ) * 1000

    # Dedicated live metric area.
    live_col1, live_col2, live_col3 = st.columns(3)

    with live_col1:
        live_nodes = st.empty()

    with live_col2:
        live_progress_text = st.empty()

    with live_col3:
        live_status = st.empty()

    progress_bar = st.progress(0)
    animation_placeholder = st.empty()

    total_steps = len(explored)

    if total_steps > 0:
        # Limit rendering overhead on larger searches.
        frame_interval = max(1, total_steps // 100)

        frame_indices = list(
            range(0, total_steps, frame_interval)
        )

        if frame_indices[-1] != total_steps - 1:
            frame_indices.append(total_steps - 1)

        for frame_number, index in enumerate(frame_indices):
            visible_explored = explored[:index + 1]
            explored_count = len(visible_explored)

            live_nodes.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Nodes explored</div>
                    <div class="metric-value">{explored_count}</div>
                    <div class="metric-hint">Search activity</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            live_progress_text.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Exploration</div>
                    <div class="metric-value">
                        {explored_count}/{total_steps}
                    </div>
                    <div class="metric-hint">Visited search states</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            live_status.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Search status</div>
                    <div class="metric-value" style="font-size:21px">
                        {"Searching..." if index < total_steps - 1 else "Finishing"}
                    </div>
                    <div class="metric-hint">{animate_algorithm} algorithm</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            fig = draw_maze(
                maze,
                START,
                GOAL,
                visible_explored,
                [],
            )

            animation_placeholder.pyplot(
                fig,
                width="stretch",
            )

            plt.close(fig)

            progress_bar.progress(
                (frame_number + 1) / len(frame_indices)
            )

            time.sleep(animation_delay)

    # Show the final solution path.
    fig = draw_maze(
        maze,
        START,
        GOAL,
        explored,
        path,
    )

    animation_placeholder.pyplot(
        fig,
        width="stretch",
    )

    plt.close(fig)

    live_status.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Search status</div>
            <div class="metric-value" style="font-size:21px">
                {"Goal reached" if path else "No path"}
            </div>
            <div class="metric-hint">
                {"Optimal path found" if path else "Try another maze"}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.session_state.results[animate_algorithm] = {
        "explored": explored,
        "path": path,
        "time_ms": elapsed_ms,
    }

    if path:
        st.success(
            f"Destination reached! "
            f"{len(path) - 1} moves · "
            f"{len(explored)} nodes explored."
        )
    else:
        st.error("No solution was found for this maze.")

    st.rerun()

# MAIN DASHBOARD

maze = st.session_state.maze
result = st.session_state.results.get(algorithm, {})

st.markdown(
    '<div class="section-label">SEARCH DASHBOARD</div>',
    unsafe_allow_html=True,
)

maze_col, stats_col = st.columns([1.8, 1])

with maze_col:
    st.markdown("### 🗺️ Maze Explorer")

    st.caption(
        "Blue cells show explored states. Yellow cells show "
        "the final route after a successful search."
    )

    fig = draw_maze(
        maze,
        START,
        GOAL,
        result.get("explored", []),
        result.get("path", []),
    )

    st.pyplot(
        fig,
        width="stretch",
    )

    plt.close(fig)

    st.caption(
        f"{ROWS} × {COLS} grid  ·  "
        f"Start {START}  ·  Goal {GOAL}"
    )

with stats_col:
    st.markdown("### Search Metrics")

    if result:
        path = result["path"]
        explored = result["explored"]

        metric_card(
            "Nodes explored",
            f"{len(explored):,}",
            f"Using {algorithm} search",
        )

        metric_card(
            "Path length",
            f"{len(path) - 1:,} moves" if path else "No path",
            "Number of moves in the solution",
        )

        metric_card(
            "Execution time",
            f'{result["time_ms"]:.3f} ms',
            "Algorithm runtime; excludes animation",
        )

        if path:
            st.success("Destination reached successfully.")
        else:
            st.warning("No valid route found.")

    else:
        metric_card(
            "Nodes explored",
            "—",
            "Solve the maze to begin",
        )

        metric_card(
            "Path length",
            "—",
            "Waiting for a solution",
        )

        metric_card(
            "Execution time",
            "—",
            "No search recorded yet",
        )

# ALGORITHM COMPARISON

results = st.session_state.results

if "BFS" in results and "A*" in results:
    st.divider()

    st.markdown(
        '<div class="section-label">PERFORMANCE ANALYSIS</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### BFS vs A*")

    bfs_result = results["BFS"]
    astar_result = results["A*"]

    bfs_path = bfs_result["path"]
    astar_path = astar_result["path"]

    comp1, comp2, comp3 = st.columns(3)

    with comp1:
        metric_card(
            "BFS explored",
            f'{len(bfs_result["explored"]):,}',
            "Breadth-first exploration",
        )

    with comp2:
        metric_card(
            "A* explored",
            f'{len(astar_result["explored"]):,}',
            "Heuristic-guided exploration",
        )

    with comp3:
        both_solved = bool(bfs_path) and bool(astar_path)

        same_length = (
            both_solved
            and len(bfs_path) == len(astar_path)
        )

        metric_card(
            "Path length",
            "Match" if same_length else (
                "Different" if both_solved else "Unsolved"
            ),
            "BFS and A* solution comparison",
        )

    comparison_data = {
        "Metric": [
            "Nodes explored",
            "Path length (moves)",
            "Execution time (ms)",
        ],
        "BFS": [
            len(bfs_result["explored"]),
            len(bfs_path) - 1 if bfs_path else "No path",
            round(bfs_result["time_ms"], 3),
        ],
        "A*": [
            len(astar_result["explored"]),
            len(astar_path) - 1 if astar_path else "No path",
            round(astar_result["time_ms"], 3),
        ],
    }

    st.dataframe(
        comparison_data,
        hide_index=True,
        width="stretch",
    )

    st.caption(
        "Runtime varies with system load. A* often explores fewer "
        "cells, but the result depends on the maze."
    )

# EDUCATIONAL SECTION

st.divider()

with st.expander("Understand the AI algorithms"):
    concept_bfs, concept_astar = st.columns(2)

    with concept_bfs:
        st.markdown(
            """
            ### Breadth-First Search

            - Uses a FIFO queue.
            - Explores the search space level by level.
            - Finds a shortest path when all moves have equal cost.
            - Time complexity: **O(V + E)**.
            - Space complexity: **O(V)**.
            """
        )

    with concept_astar:
        st.markdown(
            """
            ### A* Search

            Uses the evaluation function:

            **f(n) = g(n) + h(n)**

            - `g(n)`: actual cost from the start.
            - `h(n)`: estimated remaining cost.
            - Uses a priority queue to prioritize promising cells.
            - Manhattan distance is appropriate for four-direction
              movement with equal step costs.
            """
        )

    st.markdown(
        """
        ### How to interpret the results

        - **Nodes explored:** how many states the algorithm expanded.
        - **Path length:** how many moves the solution contains.
        - **Execution time:** time taken to compute the search result.
        - **Optimality:** BFS and correctly implemented A* with an
          admissible heuristic return a shortest path in this grid.
        """
    )

# FOOTER

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:12px; color:#94a3b8">
        <strong style="color:#cbd5e1">AI Maze Solver</strong>
        &nbsp;·&nbsp; Intelligent Search &nbsp;·&nbsp;
        Python + Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
