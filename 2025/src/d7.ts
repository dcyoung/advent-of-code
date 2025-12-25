import { Effect, pipe } from "effect"
import * as path from "node:path"
import { readFile, splitLines } from "./common.js"

const solve = (lines: string[]) => {
    let beams = new Map<number, number>();
    const startIdx = lines.shift()?.indexOf("S")!;
    beams.set(startIdx, 1);

    let nSplits = 0;
    while (lines.length > 0) {
        const line = lines.shift()!.split("");
        for (const idx of [...beams.keys()]) {
            const count = beams.get(idx)!;
            if (line[idx] === "^") {
                nSplits += 1;
                beams.set(idx - 1, (beams.get(idx - 1) ?? 0) + count);
                beams.set(idx + 1, (beams.get(idx + 1) ?? 0) + count);
                beams.delete(idx);
            }
        }
    }


    return {
        nSplits,
        nBeams: [...beams.values()].reduce((acc, v) => acc + v, 0)
    };
}

const program = pipe(
    Effect.succeed(path.join(process.env.DATA_DIR!, "d7.txt")),
    Effect.andThen(readFile),
    Effect.map(splitLines),
    Effect.map(lines => lines.filter((_, idx) => idx % 2 === 0).map(line => line.trim())),
    Effect.map(solve),
    Effect.tap(r => console.log(`Pt1: ${r.nSplits}`)),
    Effect.tap(r => console.log(`Pt1: ${r.nBeams}`))
)

Effect.runPromise(program);
