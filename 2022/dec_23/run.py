from dataclasses import dataclass
from typing import Dict, Set, List, Tuple


@dataclass(frozen=True)
class Point2D:
    x: int
    y: int


def get_adjacent(p: Point2D) -> Dict[str, Point2D]:
    result = {}
    for k in {"N", "S", "W", "E", "NW", "NE", "SW", "SE"}:
        x = p.x
        y = p.y
        if "N" in k:
            y -= 1
        if "S" in k:
            y += 1
        if "W" in k:
            x -= 1
        if "E" in k:
            x += 1
        result[k] = Point2D(x, y)
    return result


def parse_input(fpath: str) -> Set[Point2D]:
    with open(fpath, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    elves = set()
    for y, row in enumerate(lines):
        for x, v in enumerate(row):
            if v == "#":
                elves.add(Point2D(x, y))
    return elves


def propose(elf: Point2D, elves: Set[Point2D], order: List[int]) -> Point2D:
    adjacent = get_adjacent(p=elf)
    # If no other Elves are in one of those eight positions, the Elf does not do anything during this round
    if not any((e in elves) for e in adjacent.values()):
        return elf
    priority_pairs = [
        # If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
        ({"N", "NE", "NW"}, adjacent["N"]),
        # If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
        ({"S", "SE", "SW"}, adjacent["S"]),
        # If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
        ({"W", "NW", "SW"}, adjacent["W"]),
        # If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
        ({"E", "NE", "SE"}, adjacent["E"]),
    ]
    for i in order:
        keys, result = priority_pairs[i]
        if not any(adjacent[k] in elves for k in keys):
            return result
    return elf


def bounds(points: List[Point2D]) -> Tuple[Point2D, Point2D]:
    return Point2D(x=min(e.x for e in points), y=min(e.y for e in points)), Point2D(
        x=max(e.x for e in points), y=max(e.y for e in points)
    )


def display(elves: Set[Point2D]):
    min_p, max_p = bounds(elves)
    w = max_p.x - min_p.x + 1
    h = max_p.y - min_p.y + 1
    print("------------------------")
    for y in range(min_p.y, min_p.y + h):
        s = ""
        for x in range(min_p.x, min_p.x + w):
            s += "#" if Point2D(x, y) in elves else "."
        print(s)


if __name__ == "__main__":

    fpath = "input.txt"
    elves = parse_input(fpath)

    priorities = [0, 1, 2, 3]
    round_idx = 0
    while True:
        # print(priorities)
        # display(elves)
        # propose positions
        proposals = {
            elf: propose(elf=elf, elves=elves, order=priorities) for elf in elves
        }

        counts = {}
        for p in proposals.values():
            counts[p] = counts.get(p, 0) + 1

        valid_proposals = set([p for p, count in counts.items() if count <= 1])

        new_elves = []
        n_moved = 0
        for e, proposal in proposals.items():
            if proposal in valid_proposals:
                new_elves.append(proposal)
                if e != proposal:
                    n_moved += 1
            else:
                new_elves.append(e)
        if n_moved == 0:
            print("Part #2: ", round_idx + 1)
            break
        elves = set(new_elves)

        # cycle priorities
        priorities.append(priorities.pop(0))

        if round_idx == 9:
            min_p, max_p = bounds(elves)
            w = max_p.x - min_p.x + 1
            h = max_p.y - min_p.y + 1
            print("Part #1: ", w * h - len(elves))

        round_idx += 1
