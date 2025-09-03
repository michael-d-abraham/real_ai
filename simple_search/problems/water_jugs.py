from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass(frozen=True)
class WaterJugsState:
    volumes: Tuple[int, ...]

    def as_tuple(self) -> Tuple[int, ...]:
        return self.volumes

    def is_valid(self, capacities: Tuple[int, ...] | None = None) -> bool:
        # If capacities provided, validate volumes against them; otherwise assume valid
        if capacities is None:
            return True
        return all(0 <= v <= c for v, c in zip(self.volumes, capacities))


FILL = "fill"
EMPTY = "empty"
POUR = "pour"  # action will be encoded as tuples when returned from Actions


class WaterJugsProblem:
    def __init__(self, capacities: Tuple[int, ...], target: int, start: Optional[WaterJugsState] = None):
        self.capacities = capacities
        self.target = target
        if start is None:
            start_vols = tuple(0 for _ in capacities)
            self.start = WaterJugsState(start_vols)
        else:
            self.start = start

    def Actions(self, s: WaterJugsState) -> List[Tuple]:
        actions: List[Tuple] = []
        n = len(self.capacities)
        # fills
        for i in range(n):
            if s.volumes[i] < self.capacities[i]:
                actions.append((FILL, i))
        # empties
        for i in range(n):
            if s.volumes[i] > 0:
                actions.append((EMPTY, i))
        # pours
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if s.volumes[i] > 0 and s.volumes[j] < self.capacities[j]:
                    actions.append((POUR, i, j))
        return actions

    def Transition(self, s: WaterJugsState, a: Tuple) -> WaterJugsState:
        vols = list(s.volumes)
        if a[0] == FILL:
            _, i = a
            vols[i] = self.capacities[i]
        elif a[0] == EMPTY:
            _, i = a
            vols[i] = 0
        elif a[0] == POUR:
            _, i, j = a
            transfer = min(vols[i], self.capacities[j] - vols[j])
            vols[i] -= transfer
            vols[j] += transfer
        else:
            raise ValueError(f"Unknown action: {a}")
        new_state = WaterJugsState(tuple(vols))
        return new_state

    def GoalTest(self, s: WaterJugsState) -> bool:
        return any(v == self.target for v in s.volumes)

    def Cost(self, s1: WaterJugsState, a: Tuple, s2: WaterJugsState) -> float:
        # default unit cost
        if a[0] == POUR:
            # cost = amount poured
            transfer = 0
            _, i, j = a
            transfer = min(s1.volumes[i], self.capacities[j] - s1.volumes[j])
            return float(transfer)
        return 1.0

    def fmt_state(self, s: WaterJugsState) -> str:
        caps = ",".join(str(c) for c in self.capacities)
        vols = ",".join(str(v) for v in s.volumes)
        return f"capacities=({caps}) volumes=({vols})"
