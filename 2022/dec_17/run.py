from copy import deepcopy
from dataclasses import dataclass
from functools import cache
from typing import List, Tuple
import numpy as np
from tqdm import tqdm


INPUT_FPATH = "input.txt"
CAVERN_WIDTH = 7
STARTING_GAP = 3
TRUNCATE_TOWER = 53

KERNELS = [
    np.array([[1, 1, 1, 1]], dtype=np.int32),
    np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.int32),
    np.array([[0, 0, 1], [0, 0, 1], [1, 1, 1]], dtype=np.int32),
    np.array([[1], [1], [1], [1]], dtype=np.int32),
    np.array([[1, 1], [1, 1]], dtype=np.int32),
]
N_KERNELS = len(KERNELS)
JETS = [1 if c == ">" else -1 for c in open(INPUT_FPATH, "r").read().strip()]
N_JETS = len(JETS)


def empty_row() -> List[int]:
    return CAVERN_WIDTH * [0]


def calc_row_occupation(block: np.ndarray, x: int, block_y: int = -1) -> List[int]:
    block_row_occupation = empty_row()
    block_row_occupation[x : x + block.shape[1]] = list(block[block_y, :].flatten())
    return block_row_occupation


def display(
    rows: List[List[int]], falling_block: np.ndarray = None, blc: Tuple[int, int] = None
) -> None:
    print("-------------------------")

    rows = deepcopy(rows)
    if falling_block is not None:
        x, y = blc
        for i, row_idx in enumerate(range(y, y - falling_block.shape[0], -1)):
            block_row_occupation = calc_row_occupation(
                falling_block, x=x, block_y=-(1 + i)
            )
            if row_idx < 0:
                continue
            rows[row_idx] = [
                2 if b else a for a, b in zip(rows[row_idx], block_row_occupation)
            ]

    for row in rows:
        print(
            "|"
            + "".join(
                [
                    "#" if occupied == 1 else "." if occupied == 0 else "@"
                    for occupied in row
                ]
            )
            + "|"
        )
    print("+" + "".join(len(rows[0]) * ["-"]) + "+")


def collision(rows: List[List[int]], block: np.ndarray, blc: Tuple[int, int]) -> bool:
    x, y = blc
    # Check for collision w/ walls
    if x < 0 or x > CAVERN_WIDTH - block.shape[1]:
        return True

    if y >= len(rows):
        return True

    # for each row, check for collision with occupied spaces
    for i, row_idx in enumerate(range(y, y - block.shape[0], -1)):
        block_row_occupation = calc_row_occupation(block, x=x, block_y=-(1 + i))

        if row_idx < 0:
            continue

        if any(a and b for a, b in zip(rows[row_idx], block_row_occupation)):
            return True
    return False


@dataclass(frozen=True)
class State:
    jet_idx: int
    block_idx: int
    rows: str


def str_to_rows(s: str) -> List[List[int]]:
    return [
        [int(x) for x in row_s.strip().split(",")] for row_s in s.strip().split("\n")
    ]


def rows_to_str(rows: List[List[int]]) -> str:
    return "\n".join([",".join([str(x) for x in r]) for r in rows])


@cache
def simulate_block(state: State) -> Tuple[int, State]:
    block = KERNELS[state.block_idx]
    rows = str_to_rows(state.rows)
    jet_idx = state.jet_idx
    height_added = 0
    # Coordinates of blc start at 2, -4
    x = 2
    y = 0

    while True:
        jet_x = JETS[jet_idx]
        jet_idx = (jet_idx + 1) % N_JETS

        # Check for horizontal collision - only move by jet if no collision
        next_blc_x = x + jet_x
        if not collision(rows, block=block, blc=(next_blc_x, y)):
            x = next_blc_x

        # Check for vertical collision - only move down if no collision
        next_blc_y = y + 1
        if collision(rows, block=block, blc=(x, next_blc_y)):
            break
        y = next_blc_y

    # block at rest... calculate occupation for all rows
    for i, row_idx in enumerate(range(y, y - block.shape[0], -1)):
        block_row_occupation = calc_row_occupation(block, x=x, block_y=-(1 + i))
        replacement_row = [a or b for a, b in zip(rows[row_idx], block_row_occupation)]
        rows[row_idx] = replacement_row

    # Expand cavern to account for occupied rows
    first_occupied_row = next((row_idx for row_idx, row in enumerate(rows) if any(row)))
    to_add = (STARTING_GAP + 1) - first_occupied_row
    assert to_add <= (STARTING_GAP + 1)
    rows = [empty_row() for _ in range(to_add)] + rows
    height_added += to_add

    # Maybe truncate if requested (potentially lossy)
    if 0 < TRUNCATE_TOWER < len(rows):
        rows = rows[:TRUNCATE_TOWER]

    return height_added, State(
        jet_idx=jet_idx,
        block_idx=(state.block_idx + 1) % N_KERNELS,
        rows=rows_to_str(rows),
    )


@cache
def simulate_blocks(state: State, num_blocks: int) -> Tuple[int, State]:
    height = 0
    for _ in range(num_blocks):
        num_added, new_state = simulate_block(state=state)
        height += num_added
        state = new_state

    return height, state


if __name__ == "__main__":
    starting_rows = [empty_row() for _ in range(4)]

    print("Part #1:")
    height, state = simulate_blocks(
        state=State(jet_idx=0, block_idx=0, rows=rows_to_str(starting_rows)),
        num_blocks=2022,
    )
    # display(str_to_rows(state.rows))
    print(height)

    print("Part #2:")
    # the idea is to cache the input state... such that a cycle is eventually
    # identified and the results for most steps are pulled from cache
    total = 1_000_000_000_000
    n_per_step = 100_000
    state = State(jet_idx=0, block_idx=0, rows=rows_to_str(starting_rows))
    height = 0
    for _ in tqdm(range(total // n_per_step)):
        delta_height, state = simulate_blocks(state=state, num_blocks=n_per_step)
        height += delta_height
    print(height)
