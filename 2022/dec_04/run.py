from dataclasses import dataclass
from itertools import combinations, permutations
from typing import List, Set


@dataclass
class Elf:
    tasks: Set[int]


@dataclass
class Group:
    elves: List[Elf]


def overlap(g: Group) -> bool:
    for elf_a, elf_b in combinations(g.elves, 2):
        if elf_a.tasks.intersection(elf_b.tasks):
            return True
    return False


def complete_overlap(g: Group) -> bool:
    for elf_a, elf_b in permutations(g.elves, 2):
        if not (elf_a.tasks - elf_b.tasks):
            return True
    return False


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()

    groups = [
        Group(
            elves=[
                Elf(tasks=set(range(int(s.split("-")[0]), int(s.split("-")[-1]) + 1)))
                for s in line.strip().split(",")
            ]
        )
        for line in lines
    ]

    print(len(groups))

    print(len([g for g in groups if overlap(g)]))
    # print(lines[0])
    # print(groups[0].elves)
