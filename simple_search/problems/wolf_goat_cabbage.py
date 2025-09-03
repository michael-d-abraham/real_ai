from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

@dataclass(frozen=True)
class WolfGoatCabbageState:
    farmer: bool  # True = left bank, False = right bank
    wolf: bool
    goat: bool
    cabbage: bool

    def is_valid(self) -> bool:
        if self.goat == self.wolf and self.farmer != self.goat:
            return False
        if self.goat == self.cabbage and self.farmer != self.goat:
            return False
        return True

    def as_tuple(self) -> Tuple[bool, bool, bool, bool]:
        return (self.farmer, self.wolf, self.goat, self.cabbage)


CROSS_ALONE = "cross_alone"
TAKE_WOLF = "take_wolf"
TAKE_GOAT = "take_goat"
TAKE_CABBAGE = "take_cabbage"


class WolfGoatCabbageProblem:
    def __init__(self, start: WolfGoatCabbageState | None = None, goal: WolfGoatCabbageState | None = None):
        self.start = start or WolfGoatCabbageState(True, True, True, True)
        self.goal = goal or WolfGoatCabbageState(False, False, False, False)

    def Actions(self, s: WolfGoatCabbageState) -> List[str]:
        actions: List[str] = [CROSS_ALONE]
        if s.farmer == s.wolf:
            actions.append(TAKE_WOLF)
        if s.farmer == s.goat:
            actions.append(TAKE_GOAT)
        if s.farmer == s.cabbage:
            actions.append(TAKE_CABBAGE)
        return actions

    def Transition(self, s: WolfGoatCabbageState, a: str) -> WolfGoatCabbageState:
        f, w, g, c = s.as_tuple()
        new_f = not f
        new_w, new_g, new_c = w, g, c
        if a == CROSS_ALONE:
            pass
        elif a == TAKE_WOLF:
            new_w = not w
        elif a == TAKE_GOAT:
            new_g = not g
        elif a == TAKE_CABBAGE:
            new_c = not c
        else:
            raise ValueError(f"Unknown action: {a}")
        new_state = WolfGoatCabbageState(new_f, new_w, new_g, new_c)
        return new_state

    def GoalTest(self, s: WolfGoatCabbageState) -> bool:
        return s == self.goal

    def Cost(self, s1: WolfGoatCabbageState, a: str, s2: WolfGoatCabbageState) -> float:
        return 1.0

    def fmt_state(self, s: WolfGoatCabbageState) -> str:
        # Format as (L/R, L/R, L/R, L/R) for farmer,wolf,goat,cabbage
        def lr(b: bool) -> str:
            return 'L' if b else 'R'

        f, w, g, c = s.as_tuple()
        return f"({lr(f)},{lr(w)},{lr(g)},{lr(c)})"
