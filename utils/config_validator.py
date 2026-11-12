# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# Validates the operation configuration file.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

# Every recognised key, with a short description used in error
# messages (JSON cannot hold comments, so this doubles as the
# in-code documentation of the configuration file; see also the
# table in the README).
KEY_DESCRIPTIONS = {
    "seed": "integer — seeds the random generator so runs repeat exactly",
    "num_databricks": "integer >= 1 — databrick nodes; the Entrance, "
                      "Power Unit and Roof are added on top",
    "num_edges": "integer — the exact number of connections; must be "
                 "between |V|-1 and |V|(|V|-1)/2 where |V| = "
                 "num_databricks + 3",
    "max_firewalls": "integer >= 1 — firewall counts are drawn uniformly "
                     "from 1..max_firewalls",
    "records_range": "[low, high] — records stored per databrick",
    "brick_weight_range": "[low, high] — databrick weight in kilograms",
    "brick_volume_range": "[low, high] — databrick volume in litres",
    "graph_type": "'list' or 'matrix' — which representation to use",
    "mst_solver": "'prims' or 'kruskals' — which MST algorithm to run",
    "run_loader": "true/false — whether to run the freighter loader",
    "loader": "'brute_force' or 'task_d' — the given baseline, or your Task D solution",
    "weight_capacity": "integer >= 0 — the freighter's weight limit (kg)",
    "volume_capacity": "integer >= 0, or null to switch the volume "
                       "limit off entirely",
    "visualise": "true/false — open and save the operation report",
    "visual_filename": "string — base name for the saved report images",
    "print_struct": "true/false — print the graph structure to the console",
}


def validate_config(config: dict) -> list[str]:
    """
    Checks a configuration dictionary for missing keys, unknown keys,
    and out-of-range values.

    @param config: The configuration dictionary loaded from JSON.
    @returns: A list of human-readable error strings; empty when the
              configuration is valid.
    """
    errors: list[str] = []

    for key in KEY_DESCRIPTIONS:
        if key not in config:
            errors.append(f"missing key '{key}' ({KEY_DESCRIPTIONS[key]})")
    for key in config:
        if key not in KEY_DESCRIPTIONS:
            errors.append(f"unknown key '{key}'")
    if errors:
        return errors

    def expect(cond: bool, key: str) -> None:
        if not cond:
            errors.append(f"'{key}' invalid: {KEY_DESCRIPTIONS[key]}")

    expect(isinstance(config["seed"], int), "seed")
    expect(isinstance(config["num_databricks"], int)
           and config["num_databricks"] >= 1, "num_databricks")
    total = config["num_databricks"] + 3
    expect(isinstance(config["num_edges"], int)
           and total - 1 <= config["num_edges"]
           <= total * (total - 1) // 2, "num_edges")
    expect(isinstance(config["max_firewalls"], int)
           and config["max_firewalls"] >= 1, "max_firewalls")
    for key in ("records_range", "brick_weight_range", "brick_volume_range"):
        val = config[key]
        expect(isinstance(val, list) and len(val) == 2
               and all(isinstance(x, int) for x in val)
               and 1 <= val[0] <= val[1], key)
    expect(config["graph_type"] in ("list", "matrix"), "graph_type")
    expect(config["mst_solver"] in ("prims", "kruskals"), "mst_solver")
    expect(isinstance(config["run_loader"], bool), "run_loader")
    expect(config["loader"] in ("brute_force", "task_d"), "loader")
    expect(isinstance(config["weight_capacity"], int)
           and config["weight_capacity"] >= 0, "weight_capacity")
    expect(config["volume_capacity"] is None
           or (isinstance(config["volume_capacity"], int)
               and config["volume_capacity"] >= 0), "volume_capacity")
    expect(isinstance(config["visualise"], bool), "visualise")
    expect(isinstance(config["visual_filename"], str)
           and config["visual_filename"] != "", "visual_filename")
    expect(isinstance(config["print_struct"], bool), "print_struct")

    return errors
