from dataclasses import dataclass, field
from functools import cache
from typing import Dict, Iterable, List, Set, Tuple


@dataclass
class Valve:
    id: str
    flow_rate: int
    tunnels: List[str]


def parse_input(fpath: str) -> List[Valve]:
    with open(fpath, "r") as f:
        lines = f.readlines()

    valves = []
    for line in lines:
        parts = line.strip().split()
        valves.append(
            Valve(
                id=parts[1].strip(),
                flow_rate=int(parts[4].split("=")[-1].removesuffix(";").strip()),
                tunnels=[s.removesuffix(",").strip() for s in parts[9:]],
            )
        )
    return valves


if __name__ == "__main__":
    fpath = "test_input.txt"
    valves = parse_input(fpath=fpath)
    valves_by_id = {v.id: v for v in valves}

    STARTING_BUDGET = 30

    def pressure_release(valves: Iterable[str]) -> int:
        return sum([valves_by_id[v].flow_rate for v in valves])

    @cache
    def max_pressure(v: str, open_valves: frozenset[str], budget: int) -> int:
        # Base - no remaining budget to do anything
        if budget <= 0:
            return 0

        options = []
        # Option - spend 1 minute opening valve
        if v not in open_valves and valves_by_id[v].flow_rate > 0:
            options.append(max_pressure(v, open_valves | {v}, budget=budget - 1))

        # Option [n] - spend 1 minute traveling to another valve
        for next_v in valves_by_id[v].tunnels:
            options.append(max_pressure(next_v, open_valves, budget=budget - 1))

        # Start w/ what is released by currently open valves and add the best option
        return pressure_release(open_valves) + max(options)

    print("-------------------------\nPart #1\n------------------------")
    print(
        "Maximum Released Pressure: ",
        max_pressure(v="AA", open_valves=frozenset(), budget=STARTING_BUDGET),
    )

    @cache
    def max_pressure_multi(
        valve_pair: Tuple[str], open_valves: frozenset[str], budget: int
    ) -> int:
        # Base - no remaining budget to do anything
        if budget <= 0:
            return 0

        options = []

        # Option - both people open (requires 2 different closed valves)s
        v1, v2 = valve_pair[:2]
        if v1 != v2 and v1 not in open_valves and v2 not in open_valves:
            options.append(
                max_pressure_multi(
                    valve_pair=valve_pair,
                    open_valves=open_valves | set(valve_pair),
                    budget=budget - 1,
                )
            )

        # Option - both people travel
        v1, v2 = valve_pair[:2]
        for next_v1 in valves_by_id[v1].tunnels:
            for next_v2 in valves_by_id[v2].tunnels:
                options.append(
                    max_pressure_multi(
                        tuple(sorted([next_v1, next_v2])),
                        open_valves,
                        budget=budget - 1,
                    )
                )

        # Option - 1 person opens, 1 person travels
        for v1, v2 in [valve_pair, valve_pair[::-1]]:
            if v1 not in open_valves and valves_by_id[v1].flow_rate > 0:
                for next_v2 in set(valves_by_id[v2].tunnels) - {v1}:
                    options.append(
                        max_pressure_multi(
                            valve_pair=tuple(sorted((v1, next_v2))),
                            open_valves=open_valves | {v1},
                            budget=budget - 1,
                        )
                    )

        # Start w/ what is released by currently open valves and add the best option
        return pressure_release(open_valves) + max(options)

    print("-------------------------\nPart #2\n------------------------")
    print(
        "Maximum Released Pressure: ",
        max_pressure_multi(
            valve_pair=("AA", "AA"), open_valves=frozenset(), budget=STARTING_BUDGET - 4
        ),
    )
