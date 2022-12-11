from dataclasses import dataclass
import math
from typing import Callable, List, Tuple
from tqdm import tqdm


@dataclass
class Monkey:
    items: List[int]
    operation_str: str
    test_divisor: int
    target_if_true: int
    target_if_false: int
    inspection_count: int = 0

    def inspect(self, item: int, relief: bool = True, lcm: int = 0) -> Tuple[int, int]:
        self.inspection_count += 1
        worry = self.operation(old=item)
        if relief:
            worry = math.floor(worry / 3)

        if lcm:
            worry %= lcm

        return worry, (
            self.target_if_true
            if worry % self.test_divisor == 0
            else self.target_if_false
        )

    def operation(self, old: int) -> int:
        return eval(self.operation_str)


def parse_monkeys(fpath: str) -> List[Monkey]:
    with open(fpath, "r") as f:
        lines = f.readlines()
    lines_per_monkey = 7
    n_monkeys = (len(lines) + 1) // lines_per_monkey
    lines_by_monkey = [
        lines[lines_per_monkey * i : lines_per_monkey * (i + 1)]
        for i in range(n_monkeys)
    ]
    monkeys = []
    for lines in lines_by_monkey:
        monkeys.append(
            Monkey(
                items=[
                    int(s) for s in lines[1].strip().split(":")[-1].strip().split(",")
                ],
                operation_str=lines[2].strip().split(":")[-1].split("=")[-1].strip(),
                test_divisor=int(lines[3].strip().split()[-1].strip()),
                target_if_true=int(lines[4].strip().split()[-1].strip()),
                target_if_false=int(lines[5].strip().split()[-1].strip()),
            )
        )
    return monkeys


def play(rounds: int, relief: bool = True, use_lcm: bool = False) -> int:

    monkeys = parse_monkeys("input.txt")
    lcm = math.lcm(*[monkey.test_divisor for monkey in monkeys]) if use_lcm else 0

    for _ in tqdm(range(rounds)):
        for m in monkeys:
            while m.items:
                item, target = m.inspect(m.items.pop(0), relief=relief, lcm=lcm)
                monkeys[target].items.append(item)

    counts = sorted([m.inspection_count for m in monkeys])
    monkey_business = counts[-1] * counts[-2]
    return monkey_business


if __name__ == "__main__":
    monkey_business = play(20, relief=True, use_lcm=False)
    print(f"Pt 1: {monkey_business}")

    monkey_business = play(
        10000,
        relief=False,
        use_lcm=True,
    )
    print(f"Pt 2: {monkey_business}")
