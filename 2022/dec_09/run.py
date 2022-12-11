from dataclasses import dataclass
from typing import List, Tuple
import numpy as np


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def add(self, other):
        return Point(self.x + other.x, self.y + other.y)


def parse_moves(line: str) -> List:
    direction, count = line.strip().split()
    match direction:
        case "R":
            return int(count) * [Point(1, 0)]
        case "L":
            return int(count) * [Point(-1, 0)]
        case "U":
            return int(count) * [Point(0, 1)]
        case "D":
            return int(count) * [Point(0, -1)]
        case _:
            raise ValueError(f"Invalid input direction: {direction}")


def calculate_tail(head: Point, tail: Point) -> Point:
    dx = head.x - tail.x
    dy = head.y - tail.y

    if abs(dx) > 1 or abs(dy) > 1:
        change_x = 1 if dx >= 1 else -1 if dx <= -1 else 0
        change_y = 1 if dy >= 1 else -1 if dy <= -1 else 0
        return tail.add(Point(change_x, change_y))

    return tail


@dataclass
class Chain:
    nodes: List[Point]

    def apply(self, move: Point):
        self.nodes[0] = self.nodes[0].add(move)

        for i in range(len(self.nodes) - 1):
            self.nodes[i + 1] = calculate_tail(self.nodes[i], self.nodes[i + 1])

    def viz(self) -> None:

        min_x = min([p.x for p in self.nodes])
        max_x = max([p.x for p in self.nodes])
        min_y = min([p.y for p in self.nodes])
        max_y = max([p.y for p in self.nodes])

        chars = ["H"] + [str(i + 1) for i in range(9)]
        for y in range(min_y, max_y + 1):
            row = ""
            for x in range(min_x, max_x + 1):
                p = Point(x, y)
                if p in self.nodes:
                    row += chars[self.nodes.index(p)]
                else:
                    row += "."
            print(row)


if __name__ == "__main__":

    with open("input.txt", "r") as f:
        lines = f.readlines()

    moves = []
    for line in lines:
        moves += parse_moves(line)

    for n_knots in [2, 10]:
        chain = Chain(nodes=[Point(0, 0) for _ in range(n_knots)])

        visited = set()
        visited.add(chain.nodes[-1])

        for move in moves:
            chain.apply(move)
            visited.add(chain.nodes[-1])
            # print("-------------------------")
            # print(chain.nodes)
            # chain.viz()

        print(50 * "#")
        print(f"Visited: {len(visited)}")
