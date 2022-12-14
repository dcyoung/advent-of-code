from dataclasses import dataclass, field
from typing import List, Set, Tuple

import numpy as np


@dataclass(frozen=True)
class Point2D:
    x: int
    y: int


@dataclass(frozen=True)
class Line2D:
    start: Point2D
    end: Point2D

    @property
    def coverage(self) -> List[Point2D]:
        assert self.start.x == self.end.x or self.start.y == self.end.y
        output = set()
        for x in range(
            min(self.start.x, self.end.x), max(self.start.x, self.end.x) + 1
        ):
            for y in range(
                min(self.start.y, self.end.y), max(self.start.y, self.end.y) + 1
            ):
                output.add(Point2D(x, y))
        return list(output)


def bounding_box(all_points: List[Point2D]) -> Tuple[Point2D, Point2D]:
    return Point2D(
        x=min([p.x for p in all_points]), y=min([p.y for p in all_points])
    ), Point2D(x=max([p.x for p in all_points]), y=max([p.y for p in all_points]))


@dataclass
class Path2D:
    lines: List[Line2D]

    @property
    def coverage(self) -> List[Point2D]:
        return [p for l in self.lines for p in l.coverage]

    @property
    def bounding_box(self) -> Tuple[Point2D, Point2D]:
        all_points = set()
        for l in self.lines:
            all_points.update([l.start, l.end])
        return bounding_box(list(all_points))


@dataclass
class Grid2D:
    rock_paths: List[Path2D]
    sand_entry: Point2D
    contains_floor: bool
    grid: np.ndarray = field(init=False)

    def bounding_box(self) -> Tuple[Point2D, Point2D]:
        possible_bounds = {self.sand_entry}
        for r in self.rock_paths:
            possible_bounds.update(list(r.bounding_box))
        return bounding_box(all_points=list(possible_bounds))

    def __post_init__(self):
        self.sand = set()
        min_point, max_point = self.bounding_box()
        new_y = max_point.y + 2
        if self.contains_floor:
            h = max_point.y - min_point.y + 1
            floor = Path2D(
                lines=[
                    Line2D(
                        start=Point2D(x=min_point.x - (h + 1), y=new_y),
                        end=Point2D(x=max_point.x + (h + 1), y=new_y),
                    )
                ]
            )
            self.rock_paths.append(floor)
            min_point, max_point = self.bounding_box()

        self.grid = np.zeros((max_point.y + 1, max_point.x + 1))
        for p in self.rock_points():
            self.grid[p.y, p.x] = 1

    def rock_points(self):
        return [p for r in self.rock_paths for p in r.coverage]

    def sand_fall(self, start: Point2D) -> Point2D:
        h, w = self.grid.shape[:2]
        for next_p in [
            # below
            Point2D(start.x, start.y + 1),
            # below diag/left
            Point2D(start.x - 1, start.y + 1),
            # below diag/right
            Point2D(start.x + 1, start.y + 1),
        ]:
            # trying to fall off
            if next_p.y >= h or next_p.x >= w or next_p.x < 0:
                assert not self.contains_floor
                return None
            if self.grid[next_p.y, next_p.x] == 0:
                return self.sand_fall(next_p)
        return start

    def add_sand(self) -> bool:
        rest_point = self.sand_fall(self.sand_entry)
        if rest_point:
            self.grid[rest_point.y, rest_point.x] = 2
            if rest_point == self.sand_entry:
                return False
            return True
        return False

    def display(self):
        min_point, max_point = self.bounding_box()
        x_tick_lines = [
            "".join(
                [
                    str(x)[l]
                    if x in {min_point.x, max_point.x, self.sand_entry.x}
                    else " "
                    for x in range(min_point.x, max_point.x + 1)
                ]
            )
            for l in range(3)
        ]

        n_spaces_for_y_ticks = 4
        for l in x_tick_lines:
            print(f"{(n_spaces_for_y_ticks + 1)*' '}{l}")

        for y in range(min_point.y, max_point.y + 1):
            s = str(y) + (n_spaces_for_y_ticks - len(str(y)) + 1) * " "
            for x in range(min_point.x, max_point.x + 1):
                p = Point2D(x, y)
                s += (
                    "+"
                    if p == self.sand_entry
                    else "."
                    if self.grid[y, x] == 0
                    else "#"
                    if self.grid[y, x] == 1
                    else "o"
                )
            print(s)


def parse_input(fpath: str) -> List[Path2D]:
    with open(fpath, "r") as f:
        lines = f.readlines()

    def parse_path(line) -> Path2D:
        parts = line.split("->")
        points = [
            Point2D(x=int(p.split(",")[0].strip()), y=int(p.split(",")[1].strip()))
            for p in parts
        ]
        return Path2D(
            lines=[Line2D(start, end) for start, end in zip(points[:-1], points[1:])]
        )

    return [parse_path(line) for line in lines if line.strip()]


if __name__ == "__main__":
    input_fpath = "test_input.txt"

    # pt #1
    print(
        "--------------------------------\n Part #1: \n--------------------------------"
    )
    rock_paths = parse_input(input_fpath)
    grid = Grid2D(
        rock_paths=rock_paths, sand_entry=Point2D(x=500, y=0), contains_floor=False
    )
    grid.display()

    i = 0
    while grid.add_sand():
        i += 1
    grid.display()
    print(f"Number of grains until first falls off: {i}")

    # pt #2
    print(
        "--------------------------------\n Part #2: \n--------------------------------"
    )
    grid = Grid2D(
        rock_paths=rock_paths, sand_entry=Point2D(x=500, y=0), contains_floor=True
    )

    i = 1
    while grid.add_sand():
        i += 1
    grid.display()
    print(f"Number of grains come to rest: {i}")
