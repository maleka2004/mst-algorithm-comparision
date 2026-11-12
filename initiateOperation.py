# -------------------------------------------------
# EDIT THIS FILE FOR TASK C ONLY.
# Main script for the operation. For Task C you may edit this file
# to set up, run, and time your experiments; your Task A, B, and D
# code must still work with the original version, because that is
# how it is marked.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

import sys

if sys.version_info < (3, 13):
    print("[ERROR] Python 3.13 or higher is required.")
    print(f"        You are running Python {sys.version_info.major}."
          f"{sys.version_info.minor}.{sys.version_info.micro}")
    print("        Please upgrade your Python installation and try again.")
    sys.exit(1)

import io
import contextlib
import statistics
import matplotlib.pyplot as plt
from mst.prims import prims
from mst.kruskals import kruskals
import gc

def experiment(config_file):
    with contextlib.redirect_stdout(io.StringIO()):      # silence the banner
        config = setup(config_file)

    config["num_databricks"] = 197                       # |V| = 200, fixed
    V = config["num_databricks"] + 3
    max_edges = V * (V - 1) // 2
    densities = [0.01, 0.03, 0.06, 0.09, 0.2, 0.4, 0.6, 0.8, 0.91, 0.95, 1.0]
    solvers = {"prims": prims, "kruskals": kruskals}
    REPS = 15

    results = {(g, s): [] for g in ("matrix", "list") for s in solvers}
    actual_d = []

    for d in densities:
        config["num_edges"] = max(V - 1, round(d * max_edges))   # at least a tree
        actual_d.append(config["num_edges"] / max_edges)
        totals = set()

        for g in ("matrix", "list"):
            config["graph_type"] = g
            with contextlib.redirect_stdout(io.StringIO()):
                fold = build_fold(config)                # building is NOT timed
            graph = fold.get_graph()

            for s, solver in solvers.items():
                solver(graph)                            # warm-up run, discarded
                gc.collect()                             
                gc.disable()
                times = []
                for _ in range(REPS):
                    t = start()
                    tree, total = solver(graph)          # only the solver is timed
                    times.append(stop(t))
                gc.enable()
                totals.add(total)
                results[(g, s)].append(statistics.median(times))

        # sanity check: all four combinations must find the same MST total
        assert len(totals) == 1, f"MST totals disagree at d={d}: {totals}"
        print(f"d={actual_d[-1]:.3f} done")

    for (g, s), ys in results.items():
        plt.plot(actual_d, ys, marker="o", label=f"{s} on {g}")
    plt.xlabel("density d")
    plt.ylabel("median run-time (s)")
    plt.title(f"MST run-time vs density (|V| = {V}, median of {REPS} runs)")
    plt.legend()
    plt.savefig("task_c_plot.png", dpi=150)
    plt.yscale("log")                                    # second view, easier to compare
    plt.savefig("task_c_plot_log.png", dpi=150)
    print(results)

from utils.timer import start, stop
from utils.operation_utils import (
    setup,
    build_fold,
    run_mst_solver,
    run_loader,
    run_visualiser,
)


def main():
    """
    Entry point for the operation.

    Runs each stage in order:
        1. Load and validate the configuration
        2. Build The Fold
        3. Find the safe path (MST — Task B)
        4. Load the freighter (Task D)
        5. Draw the operation report (optional)

    The timer wraps the whole program — use utils/timer.py to time
    individual stages for your Task C experiments.
    """
    program_start = start()

    if len(sys.argv) != 2:
        print("Usage: python initiateOperation.py <config_file>.json")
        sys.exit(1)

    config = setup(sys.argv[1])
    fold = build_fold(config)
    mst_result = run_mst_solver(config, fold)
    load_result = run_loader(config, fold)
    run_visualiser(config, fold, mst_result, load_result)

    elapsed = stop(program_start)
    print("==========================================")
    print("   Operation complete. Vanish, Slyce.")
    print(f"   Total time: {elapsed:.4f}s")
    print("==========================================")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[2] == "experiment":
        experiment(sys.argv[1])
    else:
        main()
