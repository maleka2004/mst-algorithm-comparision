# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# Stage helpers for the main operation script.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

import json
import sys

from utils.config_validator import validate_config
from fold.the_fold import TheFold
from mst.prims import prims
from mst.kruskals import kruskals
from cargo.brute_force_loader import brute_force_load
from cargo.load_freighter import load_freighter


def print_banner() -> None:
    """
    Prints the operation banner.

    @returns: None
    """
    print("==========================================")
    print("   NEUROMANCER // Hacking with Graphs")
    print("   COSC2123/3119 Algorithms and Analysis")
    print("==========================================\n")


def setup(config_path: str) -> dict:
    """
    Loads and validates the configuration file, exiting with a
    readable message when anything is wrong.

    @param config_path: Path to the JSON configuration file.
    @returns: The validated configuration dictionary.
    """
    print_banner()
    print(f"[1] Loading configuration from {config_path}...")
    try:
        with open(config_path) as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[ERROR] Could not read config: {exc}")
        sys.exit(1)
    errors = validate_config(config)
    if errors:
        print("[ERROR] Configuration problems:")
        for e in errors:
            print(f"        - {e}")
        sys.exit(1)
    print("      Configuration valid.\n")
    return config


def build_fold(config: dict) -> TheFold:
    """
    Builds The Fold from the configuration.

    @param config: The validated configuration dictionary.
    @returns: The constructed TheFold.
    """
    print("[2] Building The Fold...")
    fold = TheFold(config)
    g = fold.get_graph()
    v = g.num_vertices(); e = g.num_edges()
    max_e = v * (v - 1) // 2
    d = e / max_e if max_e else 0.0
    print(f"      Nodes       |V| = {v} "
          f"({len(fold.get_databricks())} databricks + 3 special)")
    print(f"      Connections |E| = {e}")
    print(f"      Density       d = |E|/(|V|(|V|-1)/2) = {d:.3f}")
    if config["print_struct"]:
        print("\n" + repr(g))
    print()
    return fold


def run_mst_solver(config: dict, fold: TheFold):
    """
    Runs the configured MST solver on the network.

    @param config: The validated configuration dictionary.
    @param fold: The Fold whose network is to be spanned.
    @returns: A tuple of (tree_edges, total_firewalls) as returned by
              the solver.
    """
    solver = prims if config["mst_solver"] == "prims" else kruskals
    name = "Prim's" if config["mst_solver"] == "prims" else "Kruskal's"
    print(f"[3] Finding the safe path with {name} algorithm...")
    try:
        tree, total = solver(fold.get_graph())
    except NotImplementedError:
        print(f"      [WARN] {name} is not implemented yet "
              f"(Task B). Skipping the safe-path step.\n")
        return None
    print(f"      Connections in tree : {len(tree)}")
    print(f"      Total firewalls     : {total}\n")
    return tree, total


def run_loader(config: dict, fold: TheFold):
    """
    Runs the configured freighter loader over the recovered
    databricks, unless run_loader is false.

    @param config: The validated configuration dictionary.
    @param fold: The Fold whose databricks form the haul.
    @returns: The loader's result tuple, or None when skipped.
    """
    if not config["run_loader"]:
        print("[4] Freighter loading skipped (run_loader = false).\n")
        return None
    loader = (brute_force_load if config["loader"] == "brute_force"
              else load_freighter)
    bricks = fold.get_databricks()
    print(f"[4] Loading the freighter with the "
          f"'{config['loader']}' loader...")
    if config["loader"] == "brute_force" and len(bricks) > 20:
        print("[WARN] brute force over this many databricks will take "
              "a very long time...")
    try:
        result = loader(bricks, config["weight_capacity"],
                        config["volume_capacity"])
    except NotImplementedError:
        print("[WARN] Your Task D loader is not implemented yet.")
        print("       Set \"loader\": \"brute_force\" in the config to use")
        print("       the given baseline, or implement")
        print("       cargo/load_freighter.py to run your own solution.\n")
        return None
    selected, value, weight, volume, _ = result
    print(f"      Databricks loaded : {len(selected)} of {len(bricks)}")
    print(f"      Records freed     : {value}")
    cap_l = config["volume_capacity"]
    print(f"      Weight            : {weight}/{config['weight_capacity']} kg")
    print(f"      Volume            : {volume}"
          + (f"/{cap_l} L" if cap_l is not None else " L (no volume limit)"))
    print()
    return result


def run_visualiser(config: dict, fold: TheFold, mst_result, load_result) -> None:
    """
    Opens and saves the operation report, unless visualise is false.

    @param config: The validated configuration dictionary.
    @param fold: The Fold to draw.
    @param mst_result: The (tree, total) pair from the MST stage.
    @param load_result: The loader's result tuple, or None.
    @returns: None
    """
    if not config["visualise"]:
        return
    print("[5] Drawing the operation report...")
    from utils.visualise import operation_report
    operation_report(config, fold, mst_result, load_result)
    print()
