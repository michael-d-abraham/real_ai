import heapq
from typing import Tuple, List, Optional, Callable, Any
import time

class AStarResult:
    def __init__(self):
        self.path: Optional[List[Tuple[Any, Any]]] = None
        self.cost: float = 0.0
        self.nodes_expanded: int = 0
        self.nodes_generated: int = 0
        self.max_frontier_size: int = 0
        self.solution_depth: int = 0
        self.runtime_ms: float = 0.0
        self.heuristic_name: str = ""

def astar(start, goal_test: Callable, successors: Callable, h: Callable, heuristic_name: str = "A*") -> AStarResult:

    start_time = time.time()
    result = AStarResult()
    result.heuristic_name = heuristic_name
    

    frontier = [(h(start), 0, 0, start)]
    heapq.heapify(frontier)
    
    # Closed set with best_g[state] to handle reopens
    best_g = {start: 0}  # best known g-cost for each state
    parent = {start: None}
    parent_action = {start: None}
    
    # Metrics tracking
    nodes_generated = 1  # start node
    counter = 1  # for tie-breaking in heap
    visited = set()  # closed set for graph search
    
    while frontier:
        # Track max frontier size
        result.max_frontier_size = max(result.max_frontier_size, len(frontier))
        
        # Pop state with minimum f(n) = g(n) + h(n)
        f, g, _, s = heapq.heappop(frontier)
        
        # Skip if we've already found a better path to this state
        if s in best_g and g > best_g[s]:
            continue
            
        # Skip if already visited (graph search)
        if s in visited:
            continue
            
        # Add to closed set
        visited.add(s)
        result.nodes_expanded += 1
        
        # Check if goal reached
        if goal_test(s):
            # Reconstruct path
            path = []
            cur = s
            while cur is not None:
                path.append((cur, parent_action[cur]))
                cur = parent[cur]
            path.reverse()
            
            result.path = path
            result.cost = g
            result.solution_depth = len(path) - 1  # depth = path length - 1
            result.nodes_generated = nodes_generated
            result.runtime_ms = (time.time() - start_time) * 1000
            return result
        
        # Generate successors
        for s2, action, step_cost in successors(s):
            nodes_generated += 1
            g2 = g + step_cost
            
            # Only consider if we found a better path to s2
            if s2 not in best_g or g2 < best_g[s2]:
                best_g[s2] = g2
                parent[s2] = s
                parent_action[s2] = action
                
                # Add to frontier with f(n) = g(n) + h(n)
                f2 = g2 + h(s2)
                heapq.heappush(frontier, (f2, g2, counter, s2))
                counter += 1
    
    # No solution found
    result.nodes_generated = nodes_generated
    result.runtime_ms = (time.time() - start_time) * 1000
    return result

def ucs(start, goal_test: Callable, successors: Callable) -> AStarResult:
    return astar(start, goal_test, successors, lambda s: 0, "UCS (h=0)")
