from dataclasses import dataclass, field
from typing import List, Tuple
import numpy as np
from tqdm import tqdm

CLOCK_ORDER = [
    "right",
    "down",
    "left",
    "up",
]

FACE_SIDE_TOP = 0
FACE_SIDE_BOTTOM = 1
FACE_SIDE_LEFT = 2
FACE_SIDE_RIGHT = 3


@dataclass(frozen=True)
class Point2D:
    x: int
    y: int


@dataclass(frozen=True)
class Move:
    turn: bool
    ccw: bool
    forward: int


@dataclass
class Game:
    grid: np.ndarray
    facing: str = field(default="right")
    position: Point2D = field(init=False)
    faces: List[np.ndarray] = field(init=False)

    def __post_init__(self):
        self.position = Point2D(
            x=next(i for i, v in enumerate(self.grid[0]) if v == 2), y=0
        )
        h = self.grid.shape[0] // 3
        w = self.grid.shape[1] // 4
        self.faces = [
            self.grid[0:h, 2 * w : 3 * w],
            self.grid[h : 2 * h, 0:w],
            self.grid[h : 2 * h, w : 2 * w],
            self.grid[h : 2 * h, 2 * w : 3 * w],
            self.grid[2 * h :, 2 * w : 3 * w],
            self.grid[2 * h :, 3 * w :],
        ]

    def face_idx(self, p: Point2D) -> int:
        h = self.grid.shape[0] // 3
        w = self.grid.shape[1] // 4

        if 0 <= p.y < h:
            return 0 if 2 * w <= p.x < 3 * w else -1
        if h <= p.y <= 2 * h:
            if p.x < w:
                return 1
            if p.x < 2 * w:
                return 2
            if p.y < 2 * h:
                return 3
        if p.y < 3 * h:
            if 2 * w <= p.x < 3 * w:
                return 4
            if 3 * w <= p.x < 4 * w:
                return 5
        return -1

    def horiz(self) -> bool:
        return self.facing in {"right", "left"}

    def tlc_brc(self, face_idx: int) -> Tuple[Point2D, Point2D]:
        h = self.grid.shape[0] // 3
        w = self.grid.shape[1] // 4
        tlc = {
            0: Point2D(x=2 * w, y=0),
            1: Point2D(x=0, y=h),
            2: Point2D(x=w, y=h),
            3: Point2D(x=2 * w, y=h),
            4: Point2D(x=2 * w, y=2 * h),
            5: Point2D(x=3 * w, y=2 * h),
        }[face_idx]

        return tlc, Point2D(x=tlc.x + w - 1, y=tlc.y + h - 1)

    def relative_face_point(self, p: Point2D, face_idx: int) -> Point2D:
        tlc, _ = self.tlc_brc(face_idx=face_idx)
        return Point2D(x=p.x - tlc.x, y=p.y - tlc.y)

    def face_transition(self) -> Tuple[Point2D, str]:
        next_p_raw = Point2D(
            x=self.position.x + {"right": 1, "left": -1}.get(self.facing, 0),
            y=self.position.y + {"down": 1, "up": -1}.get(self.facing, 0),
        )
        curr_face_idx = self.face_idx(self.position)
        assert curr_face_idx >= 0
        p_local = self.relative_face_point(p=self.position, face_idx=curr_face_idx)
        # case @face_0
        if curr_face_idx == 0:
            # left -> (down face_2)
            if self.facing == "left":
                tlc, _ = self.tlc_brc(face_idx=2)
                return Point2D(x=tlc.x + p_local.y, y=tlc.y), "down"
            # right -> (left face_5)
            if self.facing == "right":
                tlc, brc = self.tlc_brc(face_idx=5)
                return Point2D(x=brc.x, y=brc.y - p_local.y), "left"
            # up -> (down face_1)
            if self.facing == "up":
                assert next_p_raw.y < 0
                tlc, brc = self.tlc_brc(face_idx=1)
                return Point2D(x=brc.x - p_local.x, y=tlc.y), "down"
        # case @ face_1
        if curr_face_idx == 1:
            # up -> (down face_0)
            if self.facing == "up":
                tlc, brc = self.tlc_brc(face_idx=0)
                return Point2D(x=brc.x - p_local.x, y=tlc.y), "down"
            # down -> (up face_4)
            if self.facing == "down":
                tlc, brc = self.tlc_brc(face_idx=4)
                return Point2D(x=brc.x - p_local.x, y=brc.y), "up"
            # left ->  (up face_5)
            if self.facing == "left":
                assert next_p_raw.x < 0
                tlc, brc = self.tlc_brc(face_idx=5)
                return Point2D(x=brc.x - p_local.y, y=brc.y), "up"
        # case @ face_2
        if curr_face_idx == 2:
            assert not self.horiz()
            # up -> (right face_0)
            if self.facing == "up":
                tlc, brc = self.tlc_brc(face_idx=0)
                return Point2D(x=tlc.x, y=tlc.y + p_local.x), "right"
            # down -> (right face_4)
            if self.facing == "down":
                tlc, brc = self.tlc_brc(face_idx=4)
                return Point2D(x=tlc.x, y=brc.y - p_local.x), "right"
        # case @ face_3
        if curr_face_idx == 3:
            # right -> (down face_5)
            if self.facing == "right":
                tlc, brc = self.tlc_brc(face_idx=5)
                return Point2D(x=brc.x - p_local.y, y=tlc.y), "down"
        # case @ face_4
        if curr_face_idx == 4:
            # left -> (up face_2)
            if self.facing == "left":
                tlc, brc = self.tlc_brc(face_idx=2)
                return Point2D(x=brc.x - p_local.y, y=brc.y), "up"
            # down -> (up face_1)
            if self.facing == "down":
                tlc, brc = self.tlc_brc(face_idx=1)
                return Point2D(x=brc.x - p_local.x, y=brc.y), "up"
        # case @ face_5
        if curr_face_idx == 5:
            # down -> (right face_1)
            if self.facing == "down":
                tlc, brc = self.tlc_brc(face_idx=1)
                return Point2D(x=tlc.x, y=brc.y - p_local.x), "right"
            # up -> (left face_3)
            if self.facing == "up":
                tlc, brc = self.tlc_brc(face_idx=3)
                return Point2D(x=brc.x, y=brc.y - p_local.x), "left"
            # right -> (left face_0)
            if self.facing == "right":
                tlc, brc = self.tlc_brc(face_idx=0)
                return Point2D(x=brc.x, y=brc.y - p_local.y), "left"
        return (
            next_p_raw,
            self.facing,
        )

    def step_cube(self) -> Tuple[Point2D, str]:
        next_pos, next_facing = self.face_transition()
        v = self.grid[next_pos.y, next_pos.x]

        if v == 1:
            return self.position, self.facing
        assert v == 2
        return next_pos, next_facing

    def step(self) -> Tuple[Point2D, str]:
        vector = (
            self.grid[self.position.y]
            if self.horiz()
            else self.grid[:, self.position.x]
        )
        play_indxs = [i for i, v in enumerate(vector) if v > 0]

        if self.facing in {"up", "left"}:
            play_indxs.reverse()

        curr_idx = self.position.x if self.horiz() else self.position.y
        curr_idx_relative = curr_idx - play_indxs[0]

        next_idx_relative = (curr_idx_relative + 1) % len(play_indxs)
        next_idx = play_indxs[next_idx_relative]
        if vector[next_idx] == 2:
            return (
                Point2D(x=next_idx, y=self.position.y)
                if self.horiz()
                else Point2D(x=self.position.x, y=next_idx),
                self.facing,
            )
        return self.position, self.facing

    def next_dir(self, ccw: bool) -> str:
        idx = CLOCK_ORDER.index(self.facing) + (-1 if ccw else 1)
        return CLOCK_ORDER[idx % len(CLOCK_ORDER)]

    def move(self, move: Move, cube: bool = False) -> None:
        if move.turn:
            self.facing = self.next_dir(ccw=move.ccw)
            return

        before = self.position
        for _ in range(move.forward):
            self.position, self.facing = self.step_cube() if cube else self.step()
            if self.position == before:
                return
            before = self.position

    def answer(self) -> int:
        row = self.position.y + 1
        col = self.position.x + 1
        dir = CLOCK_ORDER.index(self.facing)
        return 1000 * row + 4 * col + dir


def parse_input(fpath: str) -> Tuple[np.ndarray, List[Move]]:
    with open(fpath, "r") as f:
        lines = [l.strip("\n") for l in f.readlines() if l.strip()]
    mapping = {" ": 0, "#": 1, ".": 2}
    rows = [[mapping[x] for x in line] for line in lines[:-1]]
    size = max([len(r) for r in rows])
    for row in rows:
        missing = size - len(row)
        if missing > 0:
            row += missing * [0]
    grid = np.array(rows, np.int32)

    instructions = []
    letters = list(lines[-1].strip())

    while letters:
        s = letters.pop(0)
        if s == "L":
            instructions.append(Move(turn=True, ccw=True, forward=0))
            continue
        if s == "R":
            instructions.append(Move(turn=True, ccw=False, forward=0))
            continue
        while letters and letters[0] not in {"L", "R"}:
            s += letters.pop(0)
        instructions.append(Move(turn=False, ccw=True, forward=int(s)))
    return grid, instructions


if __name__ == "__main__":
    fpath = "test_input.txt"

    grid, instructions = parse_input(fpath)

    game = Game(grid=grid)
    for move in tqdm(instructions):
        game.move(move=move)

    print(game.answer())

    game = Game(grid=grid)
    for move in tqdm(instructions):
        game.move(move=move, cube=True)

    print(game.answer())
