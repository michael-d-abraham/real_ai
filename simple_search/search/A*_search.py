import heapq

def astar(graph, start, goal, h):
    """graph: {state: [(neighbor, cost), ...]}
       h: function(state) -> nonnegative heuristic
    """
    frontier = [(h(start), 0, start)]   # (f, g, state)
    best_g   = {start: 0}
    parent   = {start: None}

    while frontier:
        f, g, s = heapq.heappop(frontier)
        if s == goal:
            # reconstruct path
            path = []
            cur = s
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path, g

        for child, step_cost in graph.get(s, []):
            new_g = g + step_cost
            if child not in best_g or new_g < best_g[child]:
                best_g[child] = new_g
                parent[child] = s
                new_f = new_g + h(child)
                heapq.heappush(frontier, (new_f, new_g, child))

    return None


GRAPH = {
    "S": [("A", 2), ("B", 1)],
    "A": [("G", 9)],
    "B": [("C", 1)],
    "C": [("G", 7)],
    "G": []
}

# An admissible heuristic (never overestimates remaining cost)
H = {"S": 8, "A": 8, "B": 7, "C": 6, "G": 0}
h = lambda s: H.get(s, 0)

print(astar(GRAPH, "S", "G", h))
# -> (['S', 'B', 'C', 'G'], 9)


