from dataclasses import dataclass
from typing import List


@dataclass
class Stacks:
    stacks: List[List[str]]

    def move_9000(self, n: int, src: int, dst: int) -> None:
        for _ in range(n):
            self.stacks[dst].append(self.stacks[src].pop())

    def move_9001(self, n: int, src: int, dst: int) -> None:
        move = []
        for _ in range(n):
            move.insert(0, self.stacks[src].pop())
        self.stacks[dst] += move


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()

    stacks = [[] for _ in range(9)]
    for i, stack in enumerate(stacks):
        for line in lines[:8][::-1]:
            char = line[i * 4 + 1].strip()
            if char:
                stack.append(char)

    stax = Stacks(stacks=stacks)

    for line in lines[10:]:
        toks = line.strip().split()
        stax.move_9001(n=int(toks[1]), src=int(toks[3]) - 1, dst=int(toks[-1]) - 1)

    print(stax.stacks)
    print("".join([st[-1] for st in stax.stacks]))
