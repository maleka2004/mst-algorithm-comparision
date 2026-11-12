# -------------------------------------------------
# Local tests for Task D — the freighter loader.
# Run with: python -m tests.task_d
#
# NOT EXHAUSTIVE: the marking suite checks many more hauls,
# including awkward ones these tests deliberately leave out.
#
# Green [PASS] / red [FAIL] check correctness: the right records, a
# valid load, and a returned list that matches the totals. Yellow [WARN]
# flags a refinement that is missing but does NOT make your loader wrong
# --- returning the lightest of equally good loads, and computing only
# the sub-problems you need. Those two are hints, never failures.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from tests._helpers import check, warn, banner, summary
from fold.databrick import Databrick
from cargo.load_freighter import load_freighter

banner("Task D (freighter loader)")


def check_consistent(selected, records, weight, volume, label):
    """
    A returned load must be self-consistent: the chosen databricks must
    actually sum to the reported records, weight and volume, with no
    brick counted twice. This is a correctness requirement.
    """
    indices = [b.index for b in selected]
    check(len(indices) == len(set(indices)),
          f"{label}: no databrick is loaded twice")
    check(sum(b.records for b in selected) == records,
          f"{label}: chosen bricks' records sum to the reported {records}")
    check(sum(b.weight for b in selected) == weight,
          f"{label}: chosen bricks' weight sums to the reported {weight}")
    check(sum(b.volume for b in selected) == volume,
          f"{label}: chosen bricks' volume sums to the reported {volume}")


# ---- return types -----------------------------------------------
bricks = [Databrick(1, 60, 4, 3), Databrick(2, 30, 2, 5)]
out = load_freighter(bricks, 10, 10)
check(isinstance(out, tuple) and len(out) == 5, "returns a 5-tuple")
if isinstance(out, tuple) and len(out) == 5:
    selected, records, weight, volume, memo = out
    check(isinstance(selected, list)
          and all(isinstance(b, Databrick) for b in selected),
          "first element is a list of Databricks")
    check(isinstance(records, int) and isinstance(weight, int)
          and isinstance(volume, int),
          "records, weight, volume are ints")
    check(isinstance(memo, dict) or memo is None, "memo is a dict (or None)")

# ---- correctness: simple single-limit haul ----------------------
bricks = [Databrick(1, 60, 10, 1),
          Databrick(2, 100, 20, 1),
          Databrick(3, 120, 30, 1)]
selected, records, weight, volume, memo = load_freighter(bricks, 50, None)
check(records == 220, f"single-limit: frees 220 records (got {records})")
check(weight <= 50, "single-limit: weight fits the capacity")
check_consistent(selected, records, weight, volume, "single-limit")

# ---- correctness: both limits binding ---------------------------
bricks = [Databrick(1, 50, 1, 8),
          Databrick(2, 60, 2, 2),
          Databrick(3, 70, 3, 2)]
selected, records, weight, volume, memo = load_freighter(bricks, 5, 4)
check(records == 130, f"both limits: frees 130 records (got {records})")
check(weight <= 5 and volume <= 4, "both limits: fits within both")
check(sorted(b.index for b in selected) == [2, 3],
      "both limits: loads d2 and d3 (d1 is too bulky by volume)")
check_consistent(selected, records, weight, volume, "both limits")

# ---- correctness: a haul that needs the volume limit ------------
# Without the volume limit, the value-dense heavy-volume brick would be
# taken; with it, a lighter-volume combination wins.
volcase = [Databrick(1, 90, 1, 9),
           Databrick(2, 50, 1, 3),
           Databrick(3, 55, 1, 3)]
selected, records, weight, volume, memo = load_freighter(volcase, 3, 6)
check(records == 105,
      f"volume-binding haul: frees 105 records (got {records}) --- a loader "
      f"that ignores volume would wrongly take d1 for 90")
check(volume <= 6, "volume-binding haul: volume fits")
check_consistent(selected, records, weight, volume, "volume-binding haul")

# ---- correctness: a haul greedy-by-value gets wrong -------------
# Taking the single highest-value brick (d1) is worse than taking the
# two lighter ones together, which a correct optimiser must find.
trap = [Databrick(1, 100, 10, 1),
        Databrick(2, 60, 6, 1),
        Databrick(3, 60, 5, 1)]
selected, records, weight, volume, memo = load_freighter(trap, 11, None)
check(records == 120, f"greedy-trap haul: frees 120 records (got {records})")
check(sorted(b.index for b in selected) == [2, 3],
      "greedy-trap haul: loads d2 and d3, not the single heavy d1")
check_consistent(selected, records, weight, volume, "greedy-trap haul")

# ---- correctness: everything fits, so take it all --------------
allfit = [Databrick(1, 30, 2, 1),
          Databrick(2, 40, 3, 2),
          Databrick(3, 20, 1, 1)]
selected, records, weight, volume, memo = load_freighter(allfit, 10, 10)
check(records == 90, f"all-fit haul: frees all 90 records (got {records})")
check(sorted(b.index for b in selected) == [1, 2, 3],
      "all-fit haul: loads every databrick")
check_consistent(selected, records, weight, volume, "all-fit haul")

# ---- correctness: only the volume limit binds ------------------
volbound = [Databrick(1, 70, 1, 7),
            Databrick(2, 40, 1, 3),
            Databrick(3, 50, 1, 4)]
selected, records, weight, volume, memo = load_freighter(volbound, 100, 7)
check(records == 90, f"volume-bound haul: frees 90 records (got {records})")
check(volume <= 7, "volume-bound haul: volume fits")
check_consistent(selected, records, weight, volume, "volume-bound haul")

# ---- correctness: a larger mixed haul, both limits -------------
mixed = [Databrick(1, 60, 5, 4),
         Databrick(2, 100, 10, 6),
         Databrick(3, 120, 12, 5),
         Databrick(4, 80, 7, 7),
         Databrick(5, 40, 3, 2)]
selected, records, weight, volume, memo = load_freighter(mixed, 20, 12)
check(records == 220, f"mixed haul: frees 220 records (got {records})")
check(weight <= 20 and volume <= 12, "mixed haul: fits within both limits")
check_consistent(selected, records, weight, volume, "mixed haul")

# ---- edge cases: nothing to load -------------------------------
# An empty haul, a haul where no databrick fits, and zero capacity
# must all return an empty, valid, zero-value load without error.
sel_e, rec_e, w_e, v_e, _ = load_freighter([], 10, 10)
check(rec_e == 0 and sel_e == [], "empty haul: loads nothing, frees 0")

toobig = [Databrick(1, 100, 50, 1), Databrick(2, 90, 40, 1)]
sel_b, rec_b, w_b, v_b, _ = load_freighter(toobig, 5, None)
check(rec_b == 0 and sel_b == [],
      "no databrick fits: loads nothing, frees 0")

sel_z, rec_z, w_z, v_z, _ = load_freighter(
    [Databrick(1, 50, 1, 1)], 0, None)
check(rec_z == 0 and sel_z == [],
      "zero capacity: loads nothing, frees 0")

# =================================================================
# Diagnostics (hints only). These NEVER fail the run --- they flag the
# two refinements the full marking suite looks at, so you can see what
# is missing and improve it before submitting.
# =================================================================

# ---- hint 1: lightest-load tie-break ----------------------------
# Two single-brick loads free the same records. The heavier brick (d1)
# comes first, so a reconstruction that does not actively prefer the
# lighter load returns d1 (5 kg); a tie-breaking loader returns d2 (2 kg).
# Getting the records right is correctness (checked above elsewhere);
# preferring the lighter load is the hint.
tie = [Databrick(1, 50, 5, 1), Databrick(2, 50, 2, 1)]
selected, records, weight, volume, memo = load_freighter(tie, 5, None)
if records == 50 and weight == 2:
    check(True, "tie-break: returns the lighter of two equal-value loads")
elif records == 50:
    warn("tie-break: when two loads free the same records, could you "
         "be returning a heavier one than you need to?")
# (if records != 50 the loader is simply wrong on this haul; the
#  correctness cases above already cover value correctness.)

# ---- hint 2: sub-problems computed ------------------------------
# On this haul most sub-problems are never actually needed. A loader
# that only computes the ones it reaches will fill far fewer cells than
# one that computes every possible sub-problem.
big = [Databrick(i + 1, 10 * (i + 1), 7, 7) for i in range(12)]
C = L = 60
selected, records, weight, volume, memo = load_freighter(big, C, L)
if not isinstance(memo, dict) or not memo:
    warn("sub-problems: no memo returned --- could you be recomputing "
         "sub-problems instead of storing them?")
else:
    full_table = (len(big) + 1) * (C + 1) * (L + 1)
    filled = len(memo)
    if filled >= 0.6 * full_table:
        warn(f"sub-problems: {filled} of {full_table} cells computed --- "
             f"could you be calculating sub-problems you do not need?")
    else:
        check(True, f"sub-problems: computes {filled} of {full_table} "
                    f"cells (only what it needs)")

summary()
