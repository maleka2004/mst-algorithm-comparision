# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# Simple wall-clock timer, useful for Task C experiments.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

import time


def start() -> float:
    """
    Starts a timer.

    @returns: An opaque start marker to pass to stop().
    """
    return time.perf_counter()


def stop(start_marker: float) -> float:
    """
    Stops a timer started with start().

    @param start_marker: The value returned by start().
    @returns: The elapsed wall-clock time in seconds.
    """
    return time.perf_counter() - start_marker
