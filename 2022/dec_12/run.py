from dataclasses import dataclass
import sys
from typing import Set, Tuple
import numpy as np


@dataclass(frozen=True)
class Point2D:
    x: int
    y: int


def parse_grid(fpath: str) -> Tuple[np.ndarray, Point2D, Point2D]:
    with open(fpath, "r") as f:
        lines = f.readlines()

    mapping = {c: i for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")}
    start = None
    goal = None
    grid = np.zeros((len(lines), len(lines[0].strip())), dtype=np.int32)
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            if c == "S":
                start = Point2D(x, y)
            elif c == "E":
                goal = Point2D(x, y)
                grid[y, x] = mapping["z"] + 1
            else:
                grid[y, x] = mapping[c]
    assert goal and start
    return grid, start, goal


def search(grid, possible_starts: Set[Point2D], goal) -> int:
    h, w = grid.shape[:2]

    visited = set()
    to_search = {p for p in possible_starts}

    dist = 0
    while to_search:
        searching = to_search
        to_search = set()
        for p in searching:
            if p == goal:
                return dist
            visited.add(p)
            curr_height = grid[p.y, p.x]
            possible_moves = [
                Point2D(p.x + d, p.y) for d in [-1, 1] if 0 <= p.x + d < w
            ] + [Point2D(p.x, p.y + d) for d in [-1, 1] if 0 <= p.y + d < h]
            # check we haven't been here before
            possible_moves = [m for m in possible_moves if m not in visited]
            # check the move is valid
            possible_moves = [
                m for m in possible_moves if grid[m.y, m.x] <= curr_height + 1
            ]

            # mark possible next moves for search
            to_search.update(possible_moves)
        dist += 1

    return sys.maxsize


if __name__ == "__main__":
    # grid, start, goal = parse_grid("input.txt")
    grid, start, goal = parse_grid("test_input.txt")
    # pt 1
    dist = search(grid=grid, possible_starts={start}, goal=goal)
    print(dist)

    # pt 2
    possible_starts = set([Point2D(x, y) for y, x in np.argwhere(grid == np.min(grid))])
    # print(possible_starts)
    dist = search(grid=grid, possible_starts=possible_starts, goal=goal)
    print(dist)
