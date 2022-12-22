from dataclasses import dataclass
from typing import Dict, Any, List, Set
from sympy import sympify
from sympy.solvers import solve


@dataclass(frozen=True)
class Monkey:
    s: str

    @property
    def name(self) -> str:
        return self.s.strip().split(":")[0].strip()

    @property
    def dependencies(self) -> Set[str]:
        parts = self.s.strip().split(":")[-1].strip().split()
        if len(parts) == 1:
            return set()
        return set((parts[0], parts[-1]))

    def eqn(self, monkeys_by_name: Dict[str, Any]) -> str:
        parts = self.s.strip().split(":")[-1].strip().split()
        if len(parts) == 1:
            return parts[0]

        a = monkeys_by_name[parts[0]].eqn(monkeys_by_name=monkeys_by_name)
        b = monkeys_by_name[parts[-1]].eqn(monkeys_by_name=monkeys_by_name)

        return f"({a}) {parts[1]} ({b})"

    def compute(self, monkeys_by_name: Dict[str, Any]) -> int:
        parts = self.s.strip().split(":")[-1].strip().split()
        if len(parts) == 1:
            return int(parts[0])

        a = monkeys_by_name[parts[0]].compute(monkeys_by_name=monkeys_by_name)
        b = monkeys_by_name[parts[-1]].compute(monkeys_by_name=monkeys_by_name)

        if parts[1] == "=":
            print(a, b)
        return {"+": a + b, "-": a - b, "*": a * b, "/": a / b}[parts[1]]


def parse_input(fpath: str) -> List[Monkey]:
    with open(fpath, "r") as f:
        return [Monkey(s=l.strip()) for l in f.readlines() if l.strip()]


if __name__ == "__main__":
    monkeys = parse_input("input.txt")
    by_name = {m.name: m for m in monkeys}

    result = by_name["root"].compute(monkeys_by_name=by_name)
    print(result)

    by_name["root"] = Monkey(s=by_name["root"].s.replace("+", "="))
    by_name["humn"] = Monkey(s="humn: x")
    eqn = by_name["root"].eqn(monkeys_by_name=by_name)
    sympy_eq = sympify("Eq(" + eqn.replace("=", ",") + ")")
    print(solve(sympy_eq))
