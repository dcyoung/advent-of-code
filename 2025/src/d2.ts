import { Effect, pipe } from "effect"
import * as path from "node:path"
import { readFile } from "./common.js"

const isInvalid = (s: string, base: number) => {
    if (s.length < 2 || s.length % base !== 0) {
        return false;
    }

    const segmentLength = base;
    const targetSegment = s.slice(0, segmentLength);
    for (let i = segmentLength; i < s.length; i += segmentLength) {
        const segment = s.slice(i, i + segmentLength);
        if (segment !== targetSegment) {
            return false;
        }
    }
    return true;
}

const sumInvalidIdsP1 = (pair: [number, number]) => {
    let sum = 0
    for (let v = pair[0]; v <= pair[1]; v++) {
        const s = `${v}`;
        if (s.length < 2 || s.length % 2 !== 0) {
            continue;
        }
        if (s.slice(0, s.length / 2) === s.slice(s.length / 2)) {
            sum += v;
        }
    }
    return sum;
}


const sumInvalidIdsP2 = (pair: [number, number]) => {
    let sum = 0
    for (let v = pair[0]; v <= pair[1]; v++) {
        const s = `${v}`;
        let base = 1;
        while (base <= s.length / 2) {
            if (isInvalid(s, base)) {
                sum += v;
                break;
            }
            base++;
        }
    }
    return sum;
}

const program = pipe(
    Effect.succeed(path.join(process.env.DATA_DIR!, "d2.txt")),
    Effect.andThen(readFile),
    Effect.map((buffer) => buffer.toString().trim().split(",").map(pair => pair.trim().split("-").map(Number) as [number, number])),
    Effect.andThen(pairs => Effect.all([
        pipe(
            Effect.succeed(pairs.map(sumInvalidIdsP1)),
            Effect.map(sums => sums.reduce((acc, v) => acc + v, 0)),
            Effect.tap(total => console.log(`Total sum of invalid IDs: ${total}`))
        ),
        pipe(
            Effect.succeed(pairs.map(sumInvalidIdsP2)),
            Effect.map(sums => sums.reduce((acc, v) => acc + v, 0)),
            Effect.tap(total => console.log(`Total sum of invalid IDs (part 2): ${total}`))
        ),
    ])),
)

Effect.runPromise(program);
