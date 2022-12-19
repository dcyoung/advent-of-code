#!/usr/bin/env python3

import math
from typing import Dict, List


class BluePrint:
    def __init__(self, robots: Dict[str, Dict[str, int]]) -> None:
        self.robots = robots
        self.maxes = {
            t: max(res.get(t, 0) for res in self.robots.values())
            for t in self.robots.keys()
        }

    def __str__(self) -> str:
        return f"Blueprint {self.id}: {self.robots}"

    def geodes(self, minutes: int) -> int:
        resources = {t: 0 for t in self.robots}
        robots = {t: int(t == "ore") for t in self.robots}

        q = []
        q.append((minutes, resources, robots, None))
        max_geodes = 0

        while len(q):
            time, resources, robots, last = q.pop()

            # we reached the end, consider the candidate for the max
            if time == 0:
                max_geodes = max(max_geodes, resources["geode"])
                continue

            # this path can never beat our current maximum geode count
            if (
                max_geodes - resources["geode"]
                >= (time * (2 * robots["geode"] + time - 1)) // 2
            ):
                continue

            time -= 1
            wait = False

            for typ, res in self.robots.items():

                # if we already generate enough resources for this type
                # we don't need to create another robot to generate more
                if (
                    typ != "geode"
                    and robots[typ] * time + resources[typ] > self.maxes[typ] * time
                ):
                    continue

                # don't create one of these if we could have created one last time
                if (last is None or last == typ) and all(
                    v <= resources[t] - robots[t] for t, v in res.items()
                ):
                    continue

                # we don't have enough resources to create a robot
                # if other robots did something, we could get enough resources, though
                if any(resources[t] < v for t, v in res.items()):
                    wait = wait or all(robots[t] > 0 for t in res.keys())
                    continue

                next_resources = {
                    t: v + robots[t] - res.get(t, 0) for t, v in resources.items()
                }
                next_robots = {t: v + int(t == typ) for t, v in robots.items()}

                q.append((time, next_resources, next_robots, typ))

            if wait:
                next_resources = {t: v + robots[t] for t, v in resources.items()}
                q.append((time, next_resources, robots, None))

        return max_geodes


def parse_input(fpath: str) -> List[BluePrint]:
    with open(fpath, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    def parse_bp(line: str) -> BluePrint:
        return BluePrint(
            robots={
                bot_recipe.strip()
                .split()[1]
                .lower(): {
                    s.strip().split()[-1].lower(): int(s.strip().split()[0])
                    for s in bot_recipe.strip()
                    .split("costs")[-1]
                    .removesuffix(".")
                    .split("and")
                }
                for bot_recipe in line.split(":")[-1].split(".")
                if bot_recipe.strip()
            }
        )

    return [parse_bp(line) for line in lines]


if __name__ == "__main__":
    blueprints = parse_input("input.txt")

    quality_level = sum((i + 1) * bp.geodes(24) for i, bp in enumerate(blueprints))
    print(f"Total quality level: {quality_level}")

    geodes = [bp.geodes(32) for bp in blueprints[:3]]
    print(f"First 3 quality levels multiplied: {math.prod(geodes)}")
