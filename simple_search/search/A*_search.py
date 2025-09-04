import heapq

def ucs(graph, start, goal):
    frontier = [(0, start)]            # (g, state)
    best_g   = {start: 0}              # best known cost to each state
    parent   = {start: None}           # for path reconstruction

    while frontier:
        g, s = heapq.heappop(frontier)
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
                heapq.heappush(frontier, (new_g, child))

    return None

GRAPH = {
    "S": [("A", 2), ("B", 1)],
    "A": [("G", 9)],
    "B": [("C", 1)],
    "C": [("G", 7)],
    "G": []
}

print(ucs(GRAPH, "S", "G"))
# -> (['S', 'B', 'C', 'G'], 9.0)

