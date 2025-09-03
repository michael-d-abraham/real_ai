from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

@dataclass(frozen=True)
class EightPuzzleState:
    tiles: Tuple[int, ...]  # length 9, 0 is blank

    def as_tuple(self) -> Tuple[int, ...]:
        return self.tiles

    def is_valid(self) -> bool:
        return tuple(sorted(self.tiles)) == tuple(range(9)) and len(self.tiles) == 9


# actions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# heuristics
ZERO = 'zero'
MISPLACED = 'misplaced'
MANHATTAN = 'manhattan'


class EightPuzzleProblem:
    def __init__(self, start: EightPuzzleState | None = None, goal: Tuple[int, ...] = (1,2,3,4,5,6,7,8,0), heuristic: str = MANHATTAN):
        self.goal = goal
        if start is None:
            self.start = EightPuzzleState(goal)
        else:
            self.start = start
        self.heuristic_flavor = heuristic

    def Actions(self, s: EightPuzzleState) -> List[str]:
        actions: List[str] = []
        i = s.tiles.index(0)
        row, col = divmod(i, 3)
        if row > 0:
            actions.append(UP)
        if row < 2:
            actions.append(DOWN)
        if col > 0:
            actions.append(LEFT)
        if col < 2:
            actions.append(RIGHT)
        return actions

    def Transition(self, s: EightPuzzleState, a: str) -> EightPuzzleState:
        tiles = list(s.tiles)
        i = tiles.index(0)
        if a == UP:
            j = i - 3
        elif a == DOWN:
            j = i + 3
        elif a == LEFT:
            j = i - 1
        elif a == RIGHT:
            j = i + 1
        else:
            raise ValueError(f"Unknown action: {a}")
        tiles[i], tiles[j] = tiles[j], tiles[i]
        return EightPuzzleState(tuple(tiles))

    def GoalTest(self, s: EightPuzzleState) -> bool:
        return s.tiles == self.goal

    def Cost(self, s1: EightPuzzleState, a: str, s2: EightPuzzleState) -> float:
        return 1.0

    def Heuristic(self, s: EightPuzzleState) -> float:
        if self.heuristic_flavor == ZERO:
            return 0.0
        if self.heuristic_flavor == MISPLACED:
            # count tiles not in place (exclude blank)
            return float(sum(1 for i, v in enumerate(s.tiles) if v != 0 and v != self.goal[i]))
        # default manhattan
        total = 0
        for idx, v in enumerate(s.tiles):
            if v == 0:
                continue
            goal_idx = self.goal.index(v)
            r1, c1 = divmod(idx, 3)
            r2, c2 = divmod(goal_idx, 3)
            total += abs(r1 - r2) + abs(c1 - c2)
        return float(total)

    def fmt_state(self, s: EightPuzzleState) -> str:
        rows = []
        for r in range(3):
            row = s.tiles[3*r:3*r+3]
            rows.append(' '.join(str(x) for x in row))
        return '\n'.join(rows)
