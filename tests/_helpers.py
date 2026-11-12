# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# Shared console helpers for the local test scripts.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

GREEN, YELLOW, RED, RESET = '\033[92m', '\033[93m', '\033[91m', '\033[0m'

passed = 0
failed = 0


def check(condition: bool, msg: str) -> None:
    """
    Records and prints one test outcome.

    @param condition: True when the check passed.
    @param msg: A short description of the check.
    @returns: None
    """
    global passed, failed
    if condition:
        passed += 1
        print(f"  {GREEN}[PASS]{RESET} {msg}")
    else:
        failed += 1
        print(f"  {RED}[FAIL]{RESET} {msg}")


def warn(msg: str) -> None:
    """
    Prints a yellow advisory. Unlike check(), a warning never fails the
    run --- it flags something the full marking suite will look at more
    closely, so you can improve it before submitting.

    @param msg: The advisory message.
    @returns: None
    """
    print(f"  {YELLOW}[WARN]{RESET} {msg}")


def banner(task: str) -> None:
    """
    Prints the header and the non-exhaustive warning for a test run.

    @param task: The task name being tested.
    @returns: None
    """
    print("=" * 58)
    print(f"  Local tests — {task}")
    print("=" * 58)
    print(f"{YELLOW}  These local tests are NOT exhaustive. They check that")
    print("  you are on the right track — passing all of them does NOT")
    print(f"  mean full marks. The marking suite is far more rigorous.{RESET}")
    print()


def summary() -> None:
    """
    Prints the pass/fail count and exits non-zero on any failure.

    @returns: None
    """
    print()
    colour = GREEN if failed == 0 else RED
    print(f"{colour}  {passed} passed, {failed} failed{RESET}")
    if failed:
        raise SystemExit(1)
