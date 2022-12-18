import numpy as np
from typing import Tuple, Generator, Set


if __name__ == "__main__":
    fpath = "input.txt"

    with open(fpath, "r") as f:
        lines = [l for l in f.readlines() if l.strip()]

    voxels = np.array(
        [[int(s) for s in l.strip().split(",")] for l in lines], dtype=np.int32
    )
    print(voxels.shape)

    # Calculate the distance to each point
    distances = np.linalg.norm(voxels[:, None, :] - voxels[None, :, :], axis=-1)

    print("------------- Part #1: -------------")
    # Find anywhere that represents two voxels touching
    touching = distances[distances == 1]
    # Surface area = total faces - faces in contact
    surface_area = 6 * voxels.shape[0] - np.sum(touching)
    print(surface_area)

    print("------------- Part #2: -------------")
    search_space = [
        (mn - 1, mx + 1)
        for mn, mx in zip(np.amin(voxels, axis=0), np.amax(voxels, axis=0))
    ]
    print(search_space)

    occupied = set([tuple(v) for v in voxels])
    visited = set()

    def get_adjacent_nodes(
        v: Tuple[int, int, int]
    ) -> Generator[Tuple[int, int, int], None, None]:
        for axis in range(3):
            # increment and decrement
            for value in [list(v)[axis] + 1, list(v)[axis] - 1]:
                # out of bounds check
                if not search_space[axis][0] <= value <= search_space[axis][1]:
                    continue

                next_v = [*v]
                next_v[axis] = value
                if next_v != v:
                    yield tuple(next_v)

    def flood_fill_bfs(v: Tuple[int, int, int]) -> int:
        surface_area = 0
        if v in visited:
            return surface_area
        visited.add(v)

        to_search = list(get_adjacent_nodes(v))
        while to_search:
            v = to_search.pop(0)
            if v in visited:
                continue
            # assert v not in visited
            visited.add(v)

            for next_v in get_adjacent_nodes(v):
                if next_v in occupied:
                    surface_area += 1
                    continue
                if next_v in visited:
                    continue
                to_search.append(next_v)
        return surface_area

    print(flood_fill_bfs(v=tuple(a[0] for a in search_space)))
