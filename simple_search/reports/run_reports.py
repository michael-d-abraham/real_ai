from __future__ import annotations
import argparse
from simple_search.problems.eight_puzzle import EightPuzzleState, EightPuzzleProblem, UP, DOWN, LEFT, RIGHT
from simple_search.search.astar import astar, ucs
from simple_search.heuristics import get_heuristic

ACTION_LABELS = {UP: "Move Up", DOWN: "Move Down", LEFT: "Move Left", RIGHT: "Move Right"}

def parse_8p_start(s: str) -> EightPuzzleState:
    s = s.strip()
    if len(s) != 9 or any(ch not in "012345678" for ch in s):
        raise argparse.ArgumentTypeError("start must be a 9-digit string containing digits 0-8 exactly once")
    tiles = tuple(int(ch) for ch in s)
    state = EightPuzzleState(tiles)
    if not state.is_valid():
        raise argparse.ArgumentTypeError("start must be a permutation of digits 0-8")
    return state

def print_report(prob, heuristic: str) -> None:
    def successors(s):
        for a in prob.Actions(s):
            s2 = prob.Transition(s, a)
            yield (s2, a, 1)
    
    if heuristic == "ucs":
        result = ucs(prob.start, prob.GoalTest, successors)
        alg_label = "UCS (h=0)"
    else:
        h_func = get_heuristic(heuristic)
        result = astar(prob.start, prob.GoalTest, successors, h_func, f"A* ({heuristic})")
        alg_label = f"A* ({heuristic})"

    print(f"Domain: EightPuzzle | Algorithm: {alg_label}")
    print(f"Solution cost: {result.cost} | Depth: {result.solution_depth}")
    print(f"Nodes generated: {result.nodes_generated} | Nodes expanded: {result.nodes_expanded} | Max frontier: {result.max_frontier_size}")
    print(f"Runtime: {result.runtime_ms:.2f}ms")
    print("Path:")

    def _one_line_ep(s: EightPuzzleState) -> str:
        tiles = s.as_tuple()
        rows = [" ".join(str(tiles[r * 3 + c]) for c in range(3)) for r in range(3)]
        return " | ".join(rows)

    if result.path is None:
        print("  No solution found!")
        return

    for i, (state, action) in enumerate(result.path[1:], start=1):
        label = ACTION_LABELS.get(action, str(action))
        prev_state = result.path[i - 1][0]
        left = _one_line_ep(prev_state)
        right = _one_line_ep(state)
        print(f"  {i}) {label:15} {left} -> {right}")
    print()

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="run_reports", description="Run A* reports on 8-puzzle")
    parser.add_argument("--start", type=parse_8p_start, default=None, help="8-puzzle start state as 9-digit string")
    
    sub = parser.add_subparsers(dest="heuristic", required=True, help="heuristic to use")
    sub.add_parser("ucs", help="Run UCS (h=0)")
    sub.add_parser("h1", help="Run A* with Manhattan Distance")
    sub.add_parser("h2", help="Run A* with Linear Conflict + Manhattan")

    args = parser.parse_args(argv)

    example_starts = [
        EightPuzzleState((1, 2, 3, 4, 5, 6, 7, 8, 0)),  # goal
        EightPuzzleState((1, 2, 3, 4, 5, 6, 7, 0, 8)),  # one move away
        EightPuzzleState((1, 2, 3, 4, 5, 6, 0, 7, 8)),  # two moves away
        EightPuzzleState((1, 2, 3, 4, 0, 5, 6, 7, 8)),  # three moves away
    ]

    if args.start is not None:
        s = args.start
        if not s.is_valid():
            print(f"Invalid start state: {s.as_tuple()}")
            return
        prob = EightPuzzleProblem(start=s)
        print_report(prob, args.heuristic)
    else:
        for s in example_starts:
            if not s.is_valid():
                print(f"Skipping invalid start state: {s.as_tuple()}")
                continue
            prob = EightPuzzleProblem(start=s)
            print_report(prob, args.heuristic)

if __name__ == "__main__":
    main()
