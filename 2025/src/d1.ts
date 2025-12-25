import { Effect, pipe } from "effect"
import * as path from "node:path"
import { splitLines, readFile } from "./common.js"

const DIAL_START = 50;

const parseRotation = (line: string) => {
    const multiplier = line[0] === "L" ? -1 : 1;
    return parseInt(line.slice(1)) * multiplier;
}

const countZeroSum = (rotations: number[]) => {
    return rotations.reduce((acc, rot) => {
        const [dial, zeroSumCount] = acc;
        const newDial = (dial + rot) % 100;
        return [newDial, zeroSumCount + (newDial === 0 ? 1 : 0)] as [number, number];
    }, [DIAL_START, 0] as [number, number])[1];
}

const countZeroPass = (rotations: number[]) => {
    let count = 0;
    let dial = DIAL_START;
    for (const rot of rotations) {
        const multiplier = rot > 0 ? 1 : -1;
        let remainingRot = Math.abs(rot);
        while (remainingRot > 0) {
            dial += (1 * multiplier);
            if (dial === 100 || dial === -100) {
                dial = 0;
            }
            if (dial === 0) {
                count += 1;
            }
            remainingRot -= 1;
        }
    }
    return count;
}


const program = pipe(
    Effect.succeed(path.join(process.env.DATA_DIR!, "d1.txt")),
    Effect.andThen(readFile),
    Effect.map(splitLines),
    Effect.map(lines => lines.map(parseRotation)),
    Effect.andThen(rotations => Effect.all([
        Effect.succeed(rotations).pipe(
            Effect.map(countZeroSum),
            Effect.tap(count => console.log(`Number of times dial lands on zero: ${count}`)),
        ),
        Effect.succeed(rotations).pipe(
            Effect.map(countZeroPass),
            Effect.tap(count => console.log(`Number of times dial passes zero: ${count}`)),
        ),
    ], { concurrency: "unbounded" }))
)

Effect.runPromise(program);
