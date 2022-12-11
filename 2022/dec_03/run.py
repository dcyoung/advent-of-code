from dataclasses import dataclass
from typing import List, Set


def priority(s) -> int:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alphabet = alphabet + alphabet.upper()
    return alphabet.index(s) + 1


def overlap(sets: List[Set[str]]) -> str:
    common = sets[0]
    for set in sets[1:]:
        common = common.intersection(set)
    assert len(common) == 1, sets

    return list(common)[0]


@dataclass
class Sack:
    side_a: Set[str]
    side_b: Set[str]

    @property
    def combined(self) -> Set[str]:
        return self.side_a | self.side_b

    @classmethod
    def from_str(cls, s: str):
        side_a = set(s[: len(s) // 2])
        side_b = set(s[len(s) // 2 :])
        return cls(side_a=side_a, side_b=side_b)

    @property
    def common(self) -> str:
        return overlap([self.side_a, self.side_b])


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()

    sacks = [Sack.from_str(s.strip()) for s in lines]

    print(sum([priority(s.common) for s in sacks]))

    items = [
        overlap([s.combined for s in sacks[i : i + 3]]) for i in range(0, len(sacks), 3)
    ]
    print(sum([priority(s) for s in items]))
