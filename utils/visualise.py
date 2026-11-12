# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# The operation report: debugging visuals for every stage.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

import math
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.widgets import Slider

from graph.graph import Graph
from mst.kruskals import kruskals
from mst.prims import prims

# ---- theme -------------------------------------------------------
BG      = "#0d0d14"
PANEL   = "#12121c"
CYAN    = "#00e5ff"
MAGENTA = "#ff2bd6"
AMBER   = "#ffb300"
GREEN   = "#00ff88"
RED     = "#ff4d4d"
GREY    = "#5a5a6e"
TEXT    = "#d8d8e8"
BLUE    = "#2244cc"          # never-computed memo cells

WHITE_RED  = LinearSegmentedColormap.from_list("wr", ["#ffffff", "#ff2222"])
BLUE_WHITE = LinearSegmentedColormap.from_list("bw", [BLUE, "#ffffff"])

SPECIAL_COLOURS = {"Entrance": GREEN, "Power Unit": AMBER, "Roof": RED}

# Numeric memo tables switch to a pure heatmap beyond this size.
MAX_NUMERIC_ROWS = 16
MAX_NUMERIC_COLS = 28


# ---- layouts -----------------------------------------------------

def _layout(graph: Graph) -> dict[int, tuple[float, float]]:
    """
    Chooses node positions for drawing: a circle for small networks,
    a grid for medium ones, and a force-directed arrangement for
    large ones.

    @param graph: The graph to lay out.
    @returns: A mapping from vertex index to an (x, y) position.
    """
    vertices = graph.get_vertices()
    n = len(vertices)
    if n <= 15:
        return {v.index: (math.cos(2 * math.pi * i / n),
                          math.sin(2 * math.pi * i / n))
                for i, v in enumerate(vertices)}
    if n <= 50:
        cols = math.ceil(math.sqrt(n))
        rows = math.ceil(n / cols)
        return {v.index: ((i % cols) / max(cols - 1, 1),
                          -(i // cols) / max(rows - 1, 1))
                for i, v in enumerate(vertices)}
    return _force_layout(graph)


def _force_layout(graph: Graph, iterations: int = 150
                  ) -> dict[int, tuple[float, float]]:
    """
    Spring layout: every pair of nodes repels, connected nodes
    attract, and the temperature falls over the iterations.

    @param graph: The graph to lay out.
    @param iterations: How many relaxation steps to run.
    @returns: A mapping from vertex index to an (x, y) position.
    """
    import random
    rng = random.Random(0)
    vertices = graph.get_vertices()
    pos = {v.index: (rng.uniform(-1, 1), rng.uniform(-1, 1))
           for v in vertices}
    k = 1.0 / math.sqrt(len(vertices))
    temp = 1.0
    for _ in range(iterations):
        disp = {v.index: [0.0, 0.0] for v in vertices}
        for i, u in enumerate(vertices):
            for v in vertices[i + 1:]:
                dx = pos[u.index][0] - pos[v.index][0]
                dy = pos[u.index][1] - pos[v.index][1]
                dist = max(math.hypot(dx, dy), 1e-3)
                f = k * k / dist
                disp[u.index][0] += dx / dist * f
                disp[u.index][1] += dy / dist * f
                disp[v.index][0] -= dx / dist * f
                disp[v.index][1] -= dy / dist * f
        for u in vertices:
            for nb, _ in graph.get_neighbours(u):
                dx = pos[u.index][0] - pos[nb.index][0]
                dy = pos[u.index][1] - pos[nb.index][1]
                dist = max(math.hypot(dx, dy), 1e-3)
                f = dist * dist / k
                disp[u.index][0] -= dx / dist * f
                disp[u.index][1] -= dy / dist * f
        for idx, (dx, dy) in disp.items():
            length = max(math.hypot(dx, dy), 1e-9)
            step = min(length, temp)
            pos[idx] = (pos[idx][0] + dx / length * step,
                        pos[idx][1] + dy / length * step)
        temp *= 0.95
    return pos


# ---- panels ------------------------------------------------------

def _draw_network(ax, graph: Graph, pos, title: str,
                  highlight=None, hl_colour=CYAN, show_weights=True) -> None:
    """
    Draws the network, optionally highlighting a set of connections
    (used for the two MST panels).

    @param ax: The matplotlib axes to draw on.
    @param graph: The graph to draw.
    @param pos: Vertex positions from _layout.
    @param title: The panel title.
    @param highlight: Optional set of frozenset({u_idx, v_idx}) pairs
                      to draw emphasised.
    @param hl_colour: The colour used for highlighted connections.
    @param show_weights: Whether to label connections with firewalls.
    @returns: None
    """
    ax.set_facecolor(PANEL)
    small = graph.num_vertices() <= 25
    for e in graph.get_edges():
        x1, y1 = pos[e.u.index]
        x2, y2 = pos[e.v.index]
        hl = highlight is not None and frozenset({e.u.index, e.v.index}) in highlight
        ax.plot([x1, x2], [y1, y2],
                color=hl_colour if hl else GREY,
                lw=2.6 if hl else 0.9,
                alpha=1.0 if hl else 0.5, zorder=1)
        if show_weights and small:
            ax.text((x1 + x2) / 2, (y1 + y2) / 2, str(e.weight),
                    color=TEXT, fontsize=7, ha="center", va="center",
                    zorder=3,
                    bbox=dict(boxstyle="round,pad=0.12", fc=PANEL, ec="none"))
    for v in graph.get_vertices():
        colour = SPECIAL_COLOURS.get(v.name, CYAN)
        x, y = pos[v.index]
        ax.scatter([x], [y], s=430 if small else 60, c=PANEL,
                   edgecolors=colour, linewidths=1.8, zorder=4)
        if small:
            label = {"Entrance": "ENT", "Power Unit": "PWR",
                     "Roof": "ROOF"}.get(v.name, v.name)
            ax.text(x, y, label, color=colour, fontsize=6.5, ha="center",
                    va="center", zorder=5, fontweight="bold")
    ax.set_title(title, color=TEXT, fontsize=10, pad=6)
    ax.axis("off")


def _draw_structure(ax, graph: Graph, graph_type: str) -> None:
    """
    Draws the graph's own representation: linked-list chains for the
    adjacency list, or the matrix grid for the adjacency matrix.

    @param ax: The matplotlib axes to draw on.
    @param graph: The graph whose structure is drawn.
    @param graph_type: 'list' or 'matrix' (controls the rendering).
    @returns: None
    """
    ax.set_facecolor(PANEL)
    ax.axis("off")
    vertices = graph.get_vertices()
    n = len(vertices)
    if n > 20:
        ax.set_title(f"YOUR STRUCTURE (graph_type = \"{graph_type}\")",
                     color=TEXT, fontsize=10, pad=6)
        ax.text(0.5, 0.5, f"{n} nodes — too large to draw.\n"
                          "Use print_struct = true for the console dump.",
                transform=ax.transAxes, color=GREY, fontsize=9,
                ha="center", va="center")
        return
    ax.set_title(f"YOUR STRUCTURE (graph_type = \"{graph_type}\")",
                 color=TEXT, fontsize=10, pad=6)
    if graph_type == "matrix":
        names = [v.name for v in vertices]
        mat = [[graph.get_edge_weight(u, v) for v in vertices]
               for u in vertices]
        cell = 1.0 / (n + 1)
        for j, name in enumerate(names):
            ax.text((j + 1.5) * cell, 1 - 0.5 * cell, name,
                    transform=ax.transAxes, color=AMBER, fontsize=6.2,
                    ha="center", va="center", rotation=45)
        for i, name in enumerate(names):
            ax.text(0.5 * cell, 1 - (i + 1.5) * cell, name,
                    transform=ax.transAxes, color=AMBER, fontsize=6.2,
                    ha="center", va="center")
            for j in range(n):
                w = mat[i][j]
                ax.text((j + 1.5) * cell, 1 - (i + 1.5) * cell,
                        str(w), transform=ax.transAxes,
                        color=TEXT if w else GREY, fontsize=6.2,
                        ha="center", va="center")
    else:
        for row, v in enumerate(vertices):
            y = 0.97 - (row + 0.5) * (0.94 / n)
            ax.text(0.02, y, f"[{row}] {v.name}", transform=ax.transAxes,
                    color=AMBER, fontsize=7.2, family="monospace",
                    va="center")
            chain = "  ".join(f"→({nb.name},{w})"
                              for nb, w in graph.get_neighbours(v))
            ax.text(0.26, y, chain + "  → ∅", transform=ax.transAxes,
                    color=TEXT, fontsize=6.8, family="monospace",
                    va="center")


def _memo_slice(memo: dict, bricks_n: int, cap_c: int,
                level: int | None) -> np.ndarray:
    """
    Extracts one 2D layer of the memo as an array of record values,
    with NaN wherever a sub-problem was never computed.

    @param memo: The loader's memo dictionary.
    @param bricks_n: The number of databricks in the haul.
    @param cap_c: The freighter's weight capacity.
    @param level: The volume level to slice at, or None for a 2D memo.
    @returns: A (bricks_n+1) x (cap_c+1) array of values with NaN gaps.
    """
    grid = np.full((bricks_n + 1, cap_c + 1), np.nan)
    for key, (value, _) in memo.items():
        if level is None:
            i, c = key
            grid[i, c] = value
        elif key[2] == level:
            grid[key[0], key[1]] = value
    return grid


def _draw_memo(ax, grid: np.ndarray, title: str, vmax: float) -> None:
    """
    Draws one memo layer: numbers when the layer is small enough to
    read, a white-to-red heatmap otherwise. Cells that were never
    computed are drawn blue in both modes.

    @param ax: The matplotlib axes to draw on.
    @param grid: The layer from _memo_slice.
    @param title: The panel title.
    @param vmax: The value mapped to full red.
    @returns: None
    """
    ax.clear()
    ax.set_facecolor(PANEL)
    ax.imshow(np.where(np.isnan(grid), 0, 1), cmap=BLUE_WHITE,
              vmin=0, vmax=1, aspect="auto")
    ax.imshow(np.ma.masked_invalid(grid), cmap=WHITE_RED,
              vmin=0, vmax=max(vmax, 1), aspect="auto")
    rows, cols = grid.shape
    if rows <= MAX_NUMERIC_ROWS and cols <= MAX_NUMERIC_COLS:
        for i in range(rows):
            for c in range(cols):
                if not np.isnan(grid[i, c]):
                    ax.text(c, i, str(int(grid[i, c])), ha="center",
                            va="center", fontsize=6.5, color="#111")
    ax.set_title(title, color=TEXT, fontsize=9, pad=6)
    ax.set_xlabel("remaining weight capacity c", color=TEXT, fontsize=8)
    ax.set_ylabel("first i databricks", color=TEXT, fontsize=8)
    ax.tick_params(colors=GREY, labelsize=6)
    for s in ax.spines.values():
        s.set_color(GREY)


def _draw_manifest(ax, config: dict, load_result, bricks_total: int) -> None:
    """
    Draws the freighter manifest: what was loaded, the records freed,
    and gauges for the weight and volume limits.

    @param ax: The matplotlib axes to draw on.
    @param config: The validated configuration dictionary.
    @param load_result: The loader's result tuple.
    @param bricks_total: How many databricks were in the haul.
    @returns: None
    """
    selected, value, weight, volume, _ = load_result
    ax.set_facecolor(PANEL)
    ax.set_title("FREIGHTER MANIFEST", color=TEXT, fontsize=10, pad=6)
    ax.axis("off")
    y = 0.94
    ax.text(0.03, y, f"LOADED : {len(selected)} of {bricks_total} databricks",
            transform=ax.transAxes, color=TEXT, fontsize=9,
            family="monospace")
    y -= 0.08
    ax.text(0.03, y, f"RECORDS FREED : {value}", transform=ax.transAxes,
            color=GREEN, fontsize=10, family="monospace", fontweight="bold")
    if len(selected) <= 10:
        for b in selected:
            y -= 0.062
            ax.text(0.06, y, f"{b.name:>4}  {b.records:>4} rec  "
                             f"{b.weight:>2}kg  {b.volume:>2}L",
                    transform=ax.transAxes, color=TEXT, fontsize=8,
                    family="monospace")
    gauges = [("WEIGHT", weight, config["weight_capacity"], CYAN)]
    if config["volume_capacity"] is not None:
        gauges.append(("VOLUME", volume, config["volume_capacity"], AMBER))
    for label, used, cap, colour in gauges:
        y -= 0.11
        ax.text(0.03, y, f"{label}  {used}/{cap}", transform=ax.transAxes,
                color=TEXT, fontsize=8, family="monospace")
        ax.barh([y - 0.045], [0.9], left=0.03, height=0.035,
                color="#222233", transform=ax.transAxes)
        frac = min(used / cap, 1.0) if cap else 0.0
        ax.barh([y - 0.045], [0.9 * frac], left=0.03, height=0.035,
                color=colour if used <= cap else RED,
                transform=ax.transAxes)
    if config["volume_capacity"] is None:
        y -= 0.1
        ax.text(0.03, y, "VOLUME — (no volume limit)",
                transform=ax.transAxes, color=GREY, fontsize=8,
                family="monospace")


# ---- reports -----------------------------------------------------

def operation_report(config: dict, fold, mst_result, load_result) -> None:
    """
    Builds, shows, and saves the operation report.

    Two figures are produced. The network report draws The Fold, its
    stored structure, and the two minimum spanning trees side by side
    with their firewall totals. The cargo report draws the loader's
    memo table beside the freighter manifest; when both freighter
    limits are active the memo is three-dimensional, so a slider
    below the table scrubs through the volume levels one layer at a
    time. The saved image captures whichever layer the slider was on
    when the window closed.

    @param config: The validated configuration dictionary.
    @param fold: The Fold to draw.
    @param mst_result: The (tree, total) pair from the MST stage.
    @param load_result: The loader's result tuple, or None.
    @returns: None
    """
    os.makedirs("visuals", exist_ok=True)
    base = os.path.join("visuals", config["visual_filename"])
    graph = fold.get_graph()
    pos = _layout(graph)

    # ---------------- network report ------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9), facecolor=BG)
    _draw_network(axes[0][0], graph, pos,
                  f"THE FOLD — {graph.num_vertices()} nodes, "
                  f"{graph.num_edges()} connections")
    _draw_structure(axes[0][1], graph, config["graph_type"])

    def _safe_mst(solver):
        """Run an MST solver, returning None if it is not yet implemented."""
        try:
            return solver(graph)
        except NotImplementedError:
            return None

    k_result = _safe_mst(kruskals)
    p_result = _safe_mst(prims)

    if k_result is not None:
        k_tree, k_total = k_result
        _draw_network(axes[1][0], graph, pos,
                      f"KRUSKAL'S MST — total firewalls = {k_total}",
                      highlight={frozenset({e.u.index, e.v.index})
                                 for e in k_tree},
                      hl_colour=MAGENTA)
    else:
        _draw_network(axes[1][0], graph, pos,
                      "KRUSKAL'S MST — not implemented yet")

    if p_result is not None:
        p_tree, p_total = p_result
        _draw_network(axes[1][1], graph, pos,
                      f"PRIM'S MST — total firewalls = {p_total}",
                      highlight={frozenset({e.u.index, e.v.index})
                                 for e in p_tree},
                      hl_colour=CYAN)
    else:
        _draw_network(axes[1][1], graph, pos,
                      "PRIM'S MST — not implemented yet")

    if k_result is not None and p_result is not None:
        verdict = ("totals agree \u2713" if k_total == p_total
                   else "TOTALS DISAGREE \u2717 — check your Kruskal's")
        axes[1][1].text(0.5, -0.04, verdict, transform=axes[1][1].transAxes,
                        color=GREEN if k_total == p_total else RED,
                        fontsize=10, ha="center", fontweight="bold")
    fig.suptitle("NEUROMANCER // operation report — network",
                 color=CYAN, fontsize=13, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    # ---------------- cargo report --------------------------------
    fig2 = None
    if load_result is not None:
        selected, value, weight, volume, memo = load_result
        bricks = fold.get_databricks()
        fig2 = plt.figure(figsize=(13, 6.2), facecolor=BG)
        gs = fig2.add_gridspec(2, 2, width_ratios=[1.35, 1],
                               height_ratios=[12, 1], hspace=0.35)
        ax_memo = fig2.add_subplot(gs[0, 0])
        ax_man = fig2.add_subplot(gs[0, 1])
        _draw_manifest(ax_man, config, load_result, len(bricks))

        if memo is None:
            ax_memo.set_facecolor(PANEL)
            ax_memo.axis("off")
            ax_memo.text(0.5, 0.5,
                         "brute-force loader: no memo table to draw.\n\n"
                         "Set \"loader\": \"task_d\" in the config\n"
                         "to see your Task D memo table here.",
                         transform=ax_memo.transAxes, color=GREY,
                         fontsize=10, ha="center", va="center")
        else:
            cap_c = config["weight_capacity"]
            cap_l = config["volume_capacity"]
            vmax = max((v for v, _ in memo.values()), default=1)
            computed = len(memo)
            if cap_l is None:
                grid = _memo_slice(memo, len(bricks), cap_c, None)
                total_cells = (len(bricks) + 1) * (cap_c + 1)
                _draw_memo(ax_memo, grid,
                           f"MEMO TABLE — computed {computed:,}/"
                           f"{total_cells:,} sub-problems", vmax)
            else:
                total_cells = (len(bricks) + 1) * (cap_c + 1) * (cap_l + 1)

                def show(level: int) -> None:
                    grid = _memo_slice(memo, len(bricks), cap_c, level)
                    at_level = int(np.sum(~np.isnan(grid)))
                    _draw_memo(ax_memo, grid,
                               f"MEMO SLICE — volume level l = {level}/"
                               f"{cap_l}  ({at_level} cells here  |  "
                               f"whole table: {computed:,}/"
                               f"{total_cells:,})", vmax)

                show(cap_l)
                ax_slider = fig2.add_subplot(gs[1, 0])
                ax_slider.set_facecolor(PANEL)
                slider = Slider(ax_slider, "", 0, cap_l, valinit=cap_l,
                                valstep=1, color=CYAN, initcolor="none")
                slider.valtext.set_color(AMBER)
                ax_slider.set_title("drag to scrub volume level l",
                                    color=GREY, fontsize=8, loc="left",
                                    pad=2)
                slider.on_changed(lambda v: (show(int(v)),
                                             fig2.canvas.draw_idle()))
                fig2._slider = slider          # keep a live reference
        fig2.suptitle("NEUROMANCER // operation report — cargo",
                      color=CYAN, fontsize=13, fontweight="bold")

    # ---------------- show, then save -----------------------------
    try:
        plt.show()
    except Exception:
        pass                                   # headless: save only
    fig.savefig(base + "_network.png", dpi=110, facecolor=BG)
    print(f"      Saved {base}_network.png")
    if fig2 is not None:
        fig2.savefig(base + "_cargo.png", dpi=110, facecolor=BG,
                     bbox_inches="tight")
        print(f"      Saved {base}_cargo.png")
    plt.close("all")
