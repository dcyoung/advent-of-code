import { Effect, pipe } from "effect"
import * as path from "node:path"
import { readFile, splitLines, pairwise } from "./common.js"

class Point {
    constructor(public x: number, public y: number) { }

    key() {
        return `${this.x},${this.y}`;
    }

    distSquared(other: Point): number {
        const dx = this.x - other.x;
        const dy = this.y - other.y;
        return dx * dx + dy * dy;
    }

    area(other: Point): number {
        return (Math.abs(this.x - other.x) + 1) * (Math.abs(this.y - other.y) + 1)
    }
}

const rectangleInterior = (p1: Point, p2: Point) => {
    const minX = Math.min(p1.x, p2.x);
    const maxX = Math.max(p1.x, p2.x);
    const minY = Math.min(p1.y, p2.y);
    const maxY = Math.max(p1.y, p2.y);

    if (maxX - minX <= 1 || maxY - minY <= 1) {
        return { p1, p2 };
    }
    return { p1: new Point(minX + 1, minY + 1), p2: new Point(maxX - 1, maxY - 1) };
}

const lineIntersectsRectangle = (
    line: [Point, Point],
    rectangle: { p1: Point, p2: Point }
) => {
    const [l1, l2] = line;
    const { p1: c1, p2: c2 } = rectangle;

    const lineMinX = Math.min(l1.x, l2.x);
    const lineMaxX = Math.max(l1.x, l2.x);
    const lineMinY = Math.min(l1.y, l2.y);
    const lineMaxY = Math.max(l1.y, l2.y);
    const rectMinX = Math.min(c1.x, c2.x);
    const rectMaxX = Math.max(c1.x, c2.x);
    const rectMinY = Math.min(c1.y, c2.y);
    const rectMaxY = Math.max(c1.y, c2.y);

    return (
        lineMinX <= rectMaxX && lineMaxX >= rectMinX && lineMinY <= rectMaxY && lineMaxY >= rectMinY
    );
}

const parseInput = (lines: string[]) => {
    return lines
        .map(line => line.trim().split(",").map(Number) as [number, number])
        .map(([x, y]) => new Point(x, y));
}



const pt1 = (tiles: Point[]) => {
    const pairs = pairwise(tiles);
    let maxArea = -1;
    for (const [a, b] of pairs) {
        const area = a.area(b);
        if (area > maxArea) {
            maxArea = area;
        }
    }
    return maxArea;
}

const pt2 = (tiles: Point[]) => {
    const lineSegments = tiles.map(
        (p, i) => [p, tiles[(i + 1) % tiles.length]] as [Point, Point]
    );

    let maxArea = 0;
    for (const [a, b] of pairwise(tiles)) {
        const area = a.area(b);
        if (area <= maxArea) {
            continue;
        }
        const interior = rectangleInterior(a, b);
        if (!lineSegments.some((seg) => lineIntersectsRectangle(seg, interior))) {
            maxArea = area;
        }
    }
    return maxArea;
}

const program = pipe(
    Effect.succeed(path.join(process.env.DATA_DIR!, "d9.txt")),
    Effect.andThen(readFile),
    Effect.map(splitLines),
    Effect.map(parseInput),
    Effect.andThen(tiles => Effect.all([
        pipe(
            Effect.succeed(pt1(tiles)),
            Effect.tap(area => console.log(`Pt1: ${area}`))
        ),
        pipe(
            Effect.succeed(pt2(tiles)),
            Effect.tap(area => console.log(`Pt2: ${area}`))
        ),
    ])),
)

Effect.runPromise(program);
