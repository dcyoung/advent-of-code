import { Effect, pipe } from "effect"
import * as path from "node:path"
import { readFile, splitLines } from "./common.js"

class Point {
    constructor(public x: number, public y: number, public z: number) { }

    key() {
        return `${this.x},${this.y},${this.z}`;
    }

    distSquared(other: Point): number {
        const dx = this.x - other.x;
        const dy = this.y - other.y;
        const dz = this.z - other.z;
        return dx * dx + dy * dy + dz * dz;
    }
}


const parseInput = (lines: string[]) => {
    return lines
        .map(line => line
            .trim()
            .split(",")
            .map(Number) as [number, number, number]
        ).map(([x, y, z]) => new Point(x, y, z));
}

const pt1 = (coords: Point[]) => {
    const nCoords = coords.length
    const pairs = [];
    for (let i = 0; i < nCoords; i++) {
        for (let j = i + 1; j < nCoords; j++) {
            pairs.push([coords[i], coords[j]] as [Point, Point])
        }
    }

    const sortedPairs = pairs
        .map(([a, b]) => {
            return { pair: [a, b], dist: a.distSquared(b) };
        })
        .sort((x, y) => y.dist - x.dist) // asc
        .map(({ pair }) => pair);

    //Initially all circuits are a single coord
    const circuits = coords.map(coord => new Map([[coord.key(), coord]]));
    const cfind = (p: Point) => {
        for (let i = 0; i < circuits.length; i++) {
            if (circuits[i].has(p.key())) {
                return i;
            }
        }
        return null;
    }
    let n = 1000;
    while (n > 0) {
        n -= 1
        const [c1, c2] = sortedPairs.pop()!;
        const i1 = cfind(c1)!;
        const i2 = cfind(c2)!;
        if (i1 !== i2) {
            // Merge circuits
            circuits[i1] = new Map([...circuits[i1]!, ...circuits[i2]!])
            circuits.splice(i2, 1);
        }
    }

    // Multiply length of 3 longest circuits
    return circuits
        .sort((a, b) => b.size - a.size)
        .slice(0, 3)
        .reduce((acc, cur) => acc * cur.size, 1);
}


const pt2 = (coords: Point[]) => {
    const nCoords = coords.length
    const pairs = [];
    for (let i = 0; i < nCoords; i++) {
        for (let j = i + 1; j < nCoords; j++) {
            pairs.push([coords[i], coords[j]] as [Point, Point])
        }
    }

    const sortedPairs = pairs
        .map(([a, b]) => {
            return { pair: [a, b], dist: a.distSquared(b) };
        })
        .sort((x, y) => y.dist - x.dist) // asc
        .map(({ pair }) => pair);

    //Initially all circuits are a single coord
    const circuits = coords.map(coord => new Map([[coord.key(), coord]]));
    const cfind = (p: Point) => {
        for (let i = 0; i < circuits.length; i++) {
            if (circuits[i].has(p.key())) {
                return i;
            }
        }
        return null;
    }
    while (true) {
        const [c1, c2] = sortedPairs.pop()!;
        const i1 = cfind(c1)!;
        const i2 = cfind(c2)!;
        if (i1 !== i2) {
            // Merge circuits
            circuits[i1] = new Map([...circuits[i1]!, ...circuits[i2]!])
            circuits.splice(i2, 1);
        }
        if (circuits.length <= 1) {
            return c1.x * c2.x;
        }
    }
}


const program = pipe(
    Effect.succeed(path.join(process.env.DATA_DIR!, "d8.txt")),
    Effect.andThen(readFile),
    Effect.map(splitLines),
    Effect.map(parseInput),
    Effect.andThen(points => Effect.all([
        pipe(
            Effect.succeed(points),
            Effect.map(pt1),
            Effect.tap(result => console.log(`(Pt1): ${result}`))
        ),
        pipe(
            Effect.succeed(points),
            Effect.map(pt2),
            Effect.tap(result => console.log(`Pt2: ${result}`))
        ),
    ])),

)

Effect.runPromise(program);
