from __future__ import annotations
from typing import Tuple
import argparse

from simple_search.problems.wolf_goat_cabbage import (
    WolfGoatCabbageState,
    WolfGoatCabbageProblem,
    CROSS_ALONE,
    TAKE_GOAT,
    TAKE_WOLF,
    TAKE_CABBAGE,
)
from simple_search.problems.water_jugs import (
    WaterJugsState,
    WaterJugsProblem,
)
from simple_search.problems.eight_puzzle import (
    EightPuzzleState,
    EightPuzzleProblem,
    UP,
    DOWN,
    LEFT,
    RIGHT,
)
from simple_search.search.bfs import bfs
from simple_search.search.ids import ids

ACTION_LABELS = {
    CROSS_ALONE: "Return alone",
    TAKE_GOAT: "Move Goat",
    TAKE_WOLF: "Move Wolf",
    TAKE_CABBAGE: "Move Cabbage",
    UP: "Move Up",
    DOWN: "Move Down",
    LEFT: "Move Left",
    RIGHT: "Move Right",
}


def parse_start(s: str) -> WolfGoatCabbageState:
    s = s.strip().upper()
    if len(s) != 4 or any(ch not in ("L", "R") for ch in s):
        raise argparse.ArgumentTypeError("start must be 4 characters long using only L or R, e.g. LLLL")
    vals = tuple(ch == "L" for ch in s)
    return WolfGoatCabbageState(*vals)


def parse_8p_start(s: str) -> EightPuzzleState:
    s = s.strip()
    if len(s) != 9 or any(ch not in "012345678" for ch in s):
        raise argparse.ArgumentTypeError(
            "start must be a 9-digit string containing digits 0-8 exactly once, e.g. '123456780'"
        )
    tiles = tuple(int(ch) for ch in s)
    state = EightPuzzleState(tiles)
    if not state.is_valid():
        raise argparse.ArgumentTypeError("start must be a permutation of digits 0-8")
    return state


def print_report(prob, algo: str) -> None:
    """Run the selected algorithm on the given problem and print a report.

    The problem object must implement the standard problem API used by the search
    code (Actions, Transition, GoalTest, Cost) and optionally a `fmt_state` method.
    """
    if algo == "bfs":
        path, stats = bfs(prob, return_stats=True)
        alg_label = "BFS"
    else:
        path, stats = ids(prob, return_stats=True)
        alg_label = "IDS"

    domain = getattr(prob, "__class__", type(prob)).__name__
    print(f"Domain: {domain} | Algorithm: {alg_label}")
    print(f"Solution cost: {stats.solution_cost} | Depth: {stats.solution_depth}")
    print(f"Nodes generated: {stats.nodes_generated} | Nodes expanded: {stats.nodes_expanded} | Max frontier: {stats.max_frontier_size}")
    print("Path:")

    fmt = getattr(prob, "fmt_state", None)

    def _compact_multiline(s: str) -> str:
        # Convert a multi-line block into a single compact line using ' | ' as row separator
        rows = [line.strip() for line in s.splitlines() if line.strip()]
        return " | ".join(rows)

    for i, (state, action) in enumerate(path[1:], start=1):
        label = ACTION_LABELS.get(action, str(action)) if isinstance(action, str) else str(action)
        prev_state = path[i - 1][0]

        # Prefer compact one-line output for EightPuzzleState
        if isinstance(prev_state, EightPuzzleState) and isinstance(state, EightPuzzleState):
            def _one_line_ep(s: EightPuzzleState) -> str:
                tiles = s.as_tuple()
                rows = [" ".join(str(tiles[r * 3 + c]) for c in range(3)) for r in range(3)]
                return " | ".join(rows)

            left = _one_line_ep(prev_state)
            right = _one_line_ep(state)
        elif fmt is not None:
            left = fmt(prev_state)
            right = fmt(state)
            if isinstance(left, str) and "\n" in left:
                left = _compact_multiline(left)
            if isinstance(right, str) and "\n" in right:
                right = _compact_multiline(right)
        else:
            # fallback generic formatting using as_tuple if available
            try:
                left = "(" + ",".join("L" if v else "R" for v in prev_state.as_tuple()) + ")"
                right = "(" + ",".join("L" if v else "R" for v in state.as_tuple()) + ")"
            except Exception:
                left = str(prev_state)
                right = str(state)
        print(f"  {i}) {label:15} {left} -> {right}")
    print()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="run_reports", description="Run reports with BFS or IDS")
    parser.add_argument("--domain", choices=("wgc", "wj", "8p"), default="wgc", help="Domain to run: 'wgc', 'wj', or '8p'")
    # make --start a global option available to WGC
    parser.add_argument("--start", type=parse_start, default=None, help="WGC start state as 4 chars L/R (farmer,wolf,goat,cabbage).")
    # 8-puzzle start option (9-digit string)
    parser.add_argument("--start-8p", type=parse_8p_start, default=None, help="8-puzzle start state as 9-digit string row-major, e.g. '123456780'.")
    # WJ options
    parser.add_argument("--capacities", type=str, default=None, help="Comma-separated capacities for WJ, e.g. 3,5")
    parser.add_argument("--target", type=int, default=None, help="Target volume for WJ")

    sub = parser.add_subparsers(dest="algo", required=True, help="algorithm to run")

    p_bfs = sub.add_parser("bfs", help="Run BFS on selected domain")

    p_ids = sub.add_parser("ids", help="Run IDS on selected domain")

    args = parser.parse_args(argv)

    if args.domain == "wgc":
        # build problem(s) for Wolf-Goat-Cabbage
        example_starts = [
            WolfGoatCabbageState(True, True, True, True),
            WolfGoatCabbageState(False, False, False, True),
            WolfGoatCabbageState(False, True, False, True),
        ]

        if args.start is not None:
            s = args.start
            if not s.is_valid():
                print(f"Invalid start state: {s.as_tuple()}")
                return
            prob = WolfGoatCabbageProblem(start=s)
            print_report(prob, args.algo)
        else:
            for s in example_starts:
                if not s.is_valid():
                    print(f"Skipping invalid start state: {s.as_tuple()}")
                    continue
                prob = WolfGoatCabbageProblem(start=s)
                print_report(prob, args.algo)
    elif args.domain == "8p":
        # eight-puzzle domain
        # choose shallow example starts (0-2 moves from goal) so BFS/IDS finish quickly
        example_starts = [
            EightPuzzleState((1, 2, 3, 4, 5, 6, 7, 8, 0)),  # goal
            EightPuzzleState((1, 2, 3, 4, 5, 6, 7, 0, 8)),  # one move away
            EightPuzzleState((1, 2, 3, 4, 5, 6, 0, 7, 8)),  # two moves away
        ]

        if args.start_8p is not None:
            s = args.start_8p
            if not s.is_valid():
                print(f"Invalid start state: {s.as_tuple()}")
                return
            prob = EightPuzzleProblem(start=s)
            print_report(prob, args.algo)
        else:
            for s in example_starts:
                if not s.is_valid():
                    print(f"Skipping invalid start state: {s.as_tuple()}")
                    continue
                prob = EightPuzzleProblem(start=s)
                print_report(prob, args.algo)
    else:
        # water jugs domain
        # If user didn't provide capacities/target, run three default instances from docs
        if not args.capacities or args.target is None:
            defaults = [
                ((3, 5), 4),        # two-jug classic
                ((8, 5, 3), 4),      # three-jug example
                ((2, 4), 2),        # solvable example (changed from unsolvable)
            ]
            for caps, tgt in defaults:
                print(f"Running WaterJugsProblem capacities={caps} target={tgt}")
                prob = WaterJugsProblem(caps, tgt)
                print_report(prob, args.algo)
            return
        try:
            caps = tuple(int(x.strip()) for x in args.capacities.split(",") if x.strip())
        except ValueError:
            print("Invalid --capacities value; must be comma-separated integers, e.g. 3,5")
            return
        prob = WaterJugsProblem(caps, args.target)
        print_report(prob, args.algo)


if __name__ == "__main__":
    main()
