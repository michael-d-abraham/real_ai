
from simple_search.problems.eight_puzzle import EightPuzzleState, EightPuzzleProblem

def h0_zero(state: EightPuzzleState) -> float:
    return 0.0

def h1_manhattan(state: EightPuzzleState, goal: tuple = (1,2,3,4,5,6,7,8,0)) -> float:

    total = 0
    for idx, tile in enumerate(state.tiles):
        if tile == 0:  # Skip blank tile
            continue
        goal_idx = goal.index(tile)
        r1, c1 = divmod(idx, 3)
        r2, c2 = divmod(goal_idx, 3)
        total += abs(r1 - r2) + abs(c1 - c2)
    return float(total)

def h2_linear_conflict(state: EightPuzzleState, goal: tuple = (1,2,3,4,5,6,7,8,0)) -> float:

    manhattan = h1_manhattan(state, goal)
    
    # Check for linear conflicts in rows
    linear_conflicts = 0
    for row in range(3):
        tiles_in_row = []
        for col in range(3):
            idx = row * 3 + col
            tile = state.tiles[idx]
            if tile != 0:
                goal_idx = goal.index(tile)
                goal_row, goal_col = divmod(goal_idx, 3)
                if goal_row == row:  # Tile belongs in this row
                    tiles_in_row.append((col, goal_col, tile))
        
        # Check for conflicts in this row
        for i in range(len(tiles_in_row)):
            for j in range(i + 1, len(tiles_in_row)):
                col1, goal_col1, tile1 = tiles_in_row[i]
                col2, goal_col2, tile2 = tiles_in_row[j]
                
                # Check if they conflict (one needs to go left, other right)
                if (col1 < col2 and goal_col1 > goal_col2) or (col1 > col2 and goal_col1 < goal_col2):
                    linear_conflicts += 2
    
    # Check for linear conflicts in columns
    for col in range(3):
        tiles_in_col = []
        for row in range(3):
            idx = row * 3 + col
            tile = state.tiles[idx]
            if tile != 0:
                goal_idx = goal.index(tile)
                goal_row, goal_col = divmod(goal_idx, 3)
                if goal_col == col:  # Tile belongs in this column
                    tiles_in_col.append((row, goal_row, tile))
        
        # Check for conflicts in this column
        for i in range(len(tiles_in_col)):
            for j in range(i + 1, len(tiles_in_col)):
                row1, goal_row1, tile1 = tiles_in_col[i]
                row2, goal_row2, tile2 = tiles_in_col[j]
                
                # Check if they conflict (one needs to go up, other down)
                if (row1 < row2 and goal_row1 > goal_row2) or (row1 > row2 and goal_row1 < goal_row2):
                    linear_conflicts += 2
    
    return manhattan + linear_conflicts


# Heuristic registry for easy access
HEURISTICS = {
    'h0': h0_zero,
    'h1': h1_manhattan, 
    'h2': h2_linear_conflict,
}

def get_heuristic(name: str):
    """Get heuristic function by name."""
    return HEURISTICS.get(name, h1_manhattan)
