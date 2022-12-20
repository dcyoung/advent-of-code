from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Entry:
    value: int
    original_idx: int


def mix(original_entries: List[Entry], n_mixes: int = 1) -> List[Entry]:
    circular = [e for e in original_entries]
    for _ in range(n_mixes):
        for e in original_entries:
            start_idx = circular.index(e)
            circular.remove(e)
            end_idx = (start_idx + e.value) % len(circular)
            if end_idx == 0:
                end_idx = len(circular)
            circular.insert(end_idx, e)
    return circular


def coordinates(mixed: List[Entry]) -> List[int]:
    zero_idx = next(i for i, entry in enumerate(mixed) if entry.value == 0)
    return [
        mixed[(zero_idx + offset) % len(mixed)].value for offset in [1000, 2000, 3000]
    ]


if __name__ == "__main__":
    fpath = "input.txt"
    with open(fpath, "r") as f:
        data = [int(l.strip()) for l in f.readlines() if l.strip()]

    print("Part #1:")
    mixed = mix(
        original_entries=[Entry(value=v, original_idx=i) for i, v in enumerate(data)],
        n_mixes=1,
    )
    print(sum(coordinates(mixed=mixed)))

    print("Part #2")
    DECRYPTION_KEY = 811589153
    mixed = mix(
        original_entries=[
            Entry(value=v * DECRYPTION_KEY, original_idx=i) for i, v in enumerate(data)
        ],
        n_mixes=10,
    )
    print(sum(coordinates(mixed=mixed)))
