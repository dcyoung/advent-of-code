from dataclasses import dataclass
from typing import List
from tqdm import tqdm


@dataclass(frozen=True)
class Point2D:
    x: int
    y: int

    def manhattan_distance(self, other) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass(frozen=True)
class Sensor:
    position: Point2D
    beacon: Point2D

    @property
    def dist_to_beacon(self):
        return self.position.manhattan_distance(self.beacon)


@dataclass(frozen=True)
class Interval1D:
    a: int
    b: int

    @property
    def count(self) -> int:
        return self.b - self.a + 1

    def contains(self, x: int) -> bool:
        return self.a <= x <= self.b

    @classmethod
    def merge(cls, intervals: List) -> List:
        if len(intervals) <= 1:
            return intervals
        intervals.sort(key=lambda x: (x.a, x.b))
        result = [intervals[0]]
        for interval in intervals[1:]:
            if interval.a <= result[-1].b:
                result[-1] = cls(a=result[-1].a, b=max(result[-1].b, interval.b))
            else:
                result.append(interval)
        return result

    def excluding(self, other):
        intersection = self.intersection(other)
        if not intersection:
            return self

        if intersection == self:
            return None

        if intersection.b < self.b:
            return Interval1D(intersection.b + 1, self.b)
        return Interval1D(self.a, intersection.a - 1)

    def intersection(self, other):
        if self.a > other.b or self.b < other.a:
            return None
        return Interval1D(a=max(self.a, other.a), b=min(self.b, other.b))


@dataclass(frozen=True)
class Intervals1D:
    intervals: List[Interval1D]

    @property
    def count(self) -> int:
        return sum([i.count for i in self.intervals])

    def contains(self, x: int) -> bool:
        for i in self.intervals:
            if i.contains(x):
                return True
        return False

    def excluding(self, interval: Interval1D):
        intervals = [i.excluding(interval) for i in self.intervals]
        return Intervals1D(intervals=[x for x in intervals if x])

    def intersection(self, other: Interval1D):

        intervals = [i.intersection(other) for i in self.intervals]
        return Intervals1D(intervals=[x for x in intervals if x])


def row_coverage(row_y: int, sensors: List[Sensor]) -> Intervals1D:
    row_coverage_intervals = []
    for s in sensors:
        dist_to_row = abs(s.position.y - row_y)
        # this sensor is too far from the line... it can't tell us anything
        if dist_to_row > s.dist_to_beacon:
            continue
        to_spare = s.dist_to_beacon - dist_to_row
        row_coverage_intervals.append(
            Interval1D(a=s.position.x - to_spare, b=s.position.x + to_spare)
        )
    return Intervals1D(intervals=Interval1D.merge(row_coverage_intervals))


def parse_input(input_fpath: str) -> List[Sensor]:
    with open(input_fpath, "r") as f:
        lines = f.readlines()

    def parse_sensor(line: str) -> Sensor:
        parts = line.strip().split()
        return Sensor(
            position=Point2D(
                x=int(parts[2].removesuffix(",").split("=")[-1].strip()),
                y=int(parts[3].removesuffix(":").split("=")[-1].strip()),
            ),
            beacon=Point2D(
                x=int(parts[-2].removesuffix(",").split("=")[-1].strip()),
                y=int(parts[-1].removesuffix(":").split("=")[-1].strip()),
            ),
        )

    return [parse_sensor(l) for l in lines]


if __name__ == "__main__":
    # REAL INPUT
    input_fpath = "input.txt"
    target_y = 2000000
    min_p = Point2D(x=0, y=0)
    max_p = Point2D(x=4000000, y=4000000)

    # TEST INPUT
    # input_fpath = "test_input.txt"
    # target_y = 10
    # min_p = Point2D(x=0, y=0)
    # max_p = Point2D(x=20, y=20)

    sensors = parse_input(input_fpath=input_fpath)
    beacons = set([s.beacon for s in sensors])
    beacons_x_by_y = {}
    for b in beacons:
        if b.y not in beacons_x_by_y:
            beacons_x_by_y[b.y] = {b.x}
        else:
            beacons_x_by_y[b.y].add(b.x)

    print("--------------------------------\nPart #1\n--------------------------------")
    coverage = row_coverage(row_y=target_y, sensors=sensors)
    x_beacons = [x for x in beacons_x_by_y.get(target_y, []) if coverage.contains(x)]
    print(
        "Number of spots in row, which CANNOT be a beacon: ",
        coverage.count - len(x_beacons),
    )
    # s = ""
    # for x in range(-4, 27):
    #     s += "#" if coverage.contains(x) else "."
    # print(s)

    print("--------------------------------\nPart #2\n--------------------------------")
    search_space = Interval1D(min_p.x, max_p.x)
    for row_y in tqdm(range(min_p.y, max_p.y + 1)):
        coverage = row_coverage(row_y=row_y, sensors=sensors).intersection(search_space)
        x_beacons = [x for x in beacons_x_by_y.get(row_y, []) if coverage.contains(x)]

        if coverage.count != search_space.count:
            # row_y contains the distress beacon... find it
            valid = Intervals1D(intervals=[search_space])
            for interval in coverage.intervals:
                valid = valid.excluding(interval)
            print(valid)
            assert valid.count == 1
            row_x = valid.intervals[0].a
            tuning_freq = 4000000 * row_x + row_y
            print(row_x, row_y, tuning_freq)
            exit(1)

        # s = ""
        # for x in range(-4, 27):
        #     s += "#" if coverage.contains(x) else "."
        # print(s)
