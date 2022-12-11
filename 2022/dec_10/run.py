from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Instruction:
    cycles: int
    value: int
    txt: str


def parse_instructions() -> List[Instruction]:
    instructions = []
    with open("input.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        if parts[0] == "noop":
            instructions.append(Instruction(1, 0, line.strip()))
        else:
            instructions.append(Instruction(2, int(parts[-1]), line.strip()))
    return instructions


def get_cycle_for_pix(x: int, y: int) -> int:
    w = 40
    return 1 + y * w + x


def get_pix_for_cycle(cycle: int) -> Tuple[int, int]:
    h = 6
    w = 40
    repeat = h * w
    cycle = (cycle - 1) % repeat
    return (cycle % w, cycle // w)


if __name__ == "__main__":
    instructions = parse_instructions()
    # print(instructions[:10])

    total = 0
    for target in [20, 60, 100, 140, 180, 220]:
        register = 1
        cycle = 1
        for instruction in instructions:
            # print(f"C: {cycle}\tR: {register}")
            # print(x.txt)
            if cycle + instruction.cycles > target:
                print(
                    f"Cycle: {cycle}, Target: {target}, Register: {register}, SS: {target * register}"
                )
                total += target * register
                break
            register += instruction.value
            cycle += instruction.cycles

    print(total)

    register = 1
    cycle = 1
    output = [["." for _ in range(40)] for _ in range(6)]
    for instruction in instructions:
        for _ in range(instruction.cycles):
            x, y = get_pix_for_cycle(cycle)
            output[y][x] = "#" if abs(x - register) <= 1 else "."
            cycle += 1
        register += instruction.value

    for line in output:
        print("".join(line))
