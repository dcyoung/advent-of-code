from dataclasses import dataclass
from functools import cache
from typing import List, Set, Tuple


@dataclass(frozen=True)
class Point2D:
    x: int
    y: int


@dataclass(frozen=True)
class Blizzard:
    position: Point2D
    direction: str


@cache
def step_blizzard(blizzard: Blizzard, w: int, h: int) -> Blizzard:
    x = blizzard.position.x + {">": 1, "<": -1}.get(blizzard.direction, 0)
    y = blizzard.position.y + {"v": 1, "^": -1}.get(blizzard.direction, 0)
    return Blizzard(position=Point2D(x=x % w, y=y % h), direction=blizzard.direction)


@cache
def step(blizzards: Tuple, w: int, h: int) -> List[Blizzard]:
    return [step_blizzard(b, w=w, h=h) for b in blizzards]


def parse_input(fpath: str) -> Tuple[Point2D, Point2D, Tuple[int, int], List[Blizzard]]:
    with open(fpath, "r") as f:
        lines = [l.strip() for l in f.readlines()]

    h = len(lines) - 2
    w = len(lines[0]) - 2

    blizzards = []
    for y, line in enumerate(lines[:-1]):
        for x, v in enumerate(line):
            if v in {"<", "v", "^", ">"}:
                blizzards.append(
                    Blizzard(position=Point2D(x=x - 1, y=y - 1), direction=v)
                )
    start = Point2D(x=lines[0].index(".") - 1, y=-1)
    goal = Point2D(x=lines[-1].index(".") - 1, y=h)
    return start, goal, (w, h), blizzards


@cache
def all_next(p: Point2D) -> Set[Point2D]:
    return {
        p,
        Point2D(x=p.x, y=p.y - 1),
        Point2D(x=p.x, y=p.y + 1),
        Point2D(x=p.x - 1, y=p.y),
        Point2D(x=p.x + 1, y=p.y),
    }


def display(blizzards: List[Blizzard], position: Point2D, h: int, w: int):
    rows = (
        [(w + 2) * ["#"]]
        + [["#"] + w * ["."] + ["#"] for _ in range(h)]
        + [(w + 2) * ["#"]]
    )
    for b in blizzards:
        rows[b.position.y + 1][b.position.x + 1] = b.direction
    print("-----------------------")
    for r in rows:
        print("".join(r))


def bfs(
    start: Point2D, goals: List[Point2D], w: int, h: int, blizzards: List[Blizzard]
) -> int:
    targets = [g for g in goals]
    n_turns = 0
    q = {start}
    while q:
        # display(blizzards=blizzards, position=None, h=h, w=w)
        n_turns += 1
        next_blizzards = step(blizzards=tuple(blizzards), w=w, h=h)
        blocked = set([b.position for b in next_blizzards])

        if targets[0] in q:
            q = {targets.pop(0)}
            if not targets:
                return n_turns - 1
        to_check, q = q, set()
        for p in to_check:
            for n in all_next(p):
                if n in blocked or n in q:
                    continue
                if n == targets[0]:
                    q.add(n)
                elif 0 <= n.x < w and 0 <= n.y < h:
                    q.add(n)
                elif not q and n in goals:
                    q.add(n)
        blizzards = next_blizzards
    assert False, "Never get here"


if __name__ == "__main__":
    fpath = "input.txt"
    start, goal, (w, h), blizzards = parse_input(fpath)

    print("Part #1", bfs(start=start, goals=[goal], w=w, h=h, blizzards=blizzards))
    start, goal, (w, h), blizzards = parse_input(fpath)
    print(
        "Part #2",
        bfs(start=start, goals=[goal, start, goal], w=w, h=h, blizzards=blizzards),
    )
