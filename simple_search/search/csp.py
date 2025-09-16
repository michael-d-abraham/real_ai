

# 1) Define the CSP
variables = ["A", "B", "C", "D"]  # four regions on a map
colors = ["Red", "Green", "Blue"]  # allowed colors for every region

# Who touches whom (undirected edges)
neighbors = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D"],
    "D": ["B", "C"],
}

#domaindictionary in a simple way

domains = {}  # start with an empty dictionary

for v in variables:
    # Give each variable its own copy of the colors list
    domains[v] = colors[:]

# 2) Helper: check if assigning 'value' to 'var' breaks any constraint
def is_consistent(var, value, assignment):
    for n in neighbors[var]:
        if n in assignment and assignment[n] == value:
            return False  # neighbor has the same color → not allowed
    return True


# 3) Backtracking search
def backtrack(assignment):
    # If everything is assigned, we found a solution
    if len(assignment) == len(variables):
        return assignment

    # Pick the next unassigned variable (simple left-to-right choice)
    for var in variables:
        if var not in assignment:
            break

    # Try each color for this variable
    for value in domains[var]:
        if is_consistent(var, value, assignment):
            assignment[var] = value           # choose
            result = backtrack(assignment)    # explore
            if result is not None:
                return result                 # success bubbles up
            del assignment[var]               # undo (backtrack)

    # No color worked → dead end
    return None


# 4) Run it
solution = backtrack({})
print("Solution:", solution)
