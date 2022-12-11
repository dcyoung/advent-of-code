from dataclasses import dataclass
from typing import List


@dataclass
class Elf:
    id: int
    calories: List[int]

    @property
    def total(self):
        return sum(self.calories)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        blob_by_elf = f.read().split("\n\n")

    elves = [
        Elf(id=i, calories=[int(s) for s in txt.split()])
        for i, txt in enumerate(blob_by_elf)
    ]

    elves.sort(key=lambda e: e.total)
    max_elf = elves[-1]
    print(max_elf)
    print(max_elf.total)

    top_3 = elves[-3:]
    print(len(top_3))
    print(top_3)
    print(sum([e.total for e in top_3]))
