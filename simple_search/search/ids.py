from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

@dataclass
class _Node:
    state: Any
    action: Optional[str]
    parent: Optional["_Node"]
    depth: int


@dataclass
class IDSStats:
    nodes_generated: int = 0
    nodes_expanded: int = 0
    max_frontier_size: int = 0
    solution_depth: Optional[int] = None
    solution_cost: Optional[float] = None


def depth_limited_search(problem, limit: Optional[int] = 5, return_stats: bool = False):
    stats = IDSStats()
    start = problem.start
    stack: List[_Node] = [_Node(start, None, None, 0)]
    stats.nodes_generated = 1
    stats.max_frontier_size = max(stats.max_frontier_size, len(stack))

    while stack:
        node = stack.pop()
        depth = node.depth
        stats.nodes_expanded += 1
        if problem.GoalTest(node.state):
            path: List[Tuple[Any, Optional[str]]] = []
            cur: Optional[_Node] = node
            cost = 0.0
            while cur is not None:
                path.append((cur.state, cur.action))
                if cur.parent is not None:
                    try:
                        cost += problem.Cost(cur.parent.state, cur.action, cur.state)
                    except Exception:
                        cost += 1.0
                cur = cur.parent
            path.reverse()
            stats.solution_depth = len(path) - 1
            stats.solution_cost = cost
            if return_stats:
                return (path, stats)
            return path

        if depth >= (limit or 0):
            continue

        children: List[_Node] = []
        for action in problem.Actions(node.state):
            child_state = problem.Transition(node.state, action)
            stats.nodes_generated += 1
            if hasattr(child_state, "is_valid") and not child_state.is_valid():
                continue
            child = _Node(child_state, action, node, node.depth + 1)
            children.append(child)
        for child in reversed(children):
            stack.append(child)
        stats.max_frontier_size = max(stats.max_frontier_size, len(stack))

    if return_stats:
        return ([], stats)
    return []


def ids(problem, max_limit: Optional[int] = 50, return_stats: bool = False):
    accumulated = IDSStats()
    for depth in range(0, max_limit + 1):
        res = depth_limited_search(problem, limit=depth, return_stats=True)
        path, stats = res
        accumulated.nodes_generated += stats.nodes_generated
        accumulated.nodes_expanded += stats.nodes_expanded
        accumulated.max_frontier_size = max(accumulated.max_frontier_size, stats.max_frontier_size)
        if path:
            accumulated.solution_depth = stats.solution_depth
            accumulated.solution_cost = stats.solution_cost
            if return_stats:
                return (path, accumulated)
            return path
    if return_stats:
        return ([], accumulated)
    return []
