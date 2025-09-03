# A* Search

# Super small working UCS

from queue import PriorityQueue
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional


GRAPH: Dict[str, List[Tuple[str, int]]] = {
    "S": [("A", 2), ("B", 1)],
    "A": [("G", 9)],
    "B": [("C", 1)],
    "C": [("G", 7)],
    "G": []  # goal: no children
}


start = "S"
goal = "G"

def reconstruct_path(parent: Dict[str, Optional[str]], end: str) -> List[str]:
    path: List[str] = []
    cur: Optional[str] = end
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    path.reverse()
    return path

frontier = PriorityQueue()
frontier.put((0, start))          # (g, state)

best_g: Dict[str, int] = {start: 0}
parent: Dict[str, Optional[str]] = {start: None}

found_cost: Optional[int] = None
found_path: List[str] = []

while not frontier.empty():
    g, s = frontier.get()         # smallest g first

    if s == goal:                 # goal test
        found_cost = g
        found_path = reconstruct_path(parent, s)
        break

    for child, step_cost in GRAPH.get(s, []):
        new_g = g + step_cost
        if child not in best_g or new_g < best_g[child]:
            best_g[child] = new_g
            parent[child] = s
            frontier.put((new_g, child))

if found_cost is None:
    print("No path.")
else:
    print("Cost:", found_cost)            # Expected: 9
    print("Path:", " -> ".join(found_path))  # Expected: S -> B -> C -> G


#understand and build a heuristics


# Super small working A*