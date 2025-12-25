import { Effect, pipe, Option } from "effect"
import * as path from "node:path"
import { readFile, splitLines, findIdxLargest } from "./common.js"

const maxSum = (bank: number[], n: number): Effect.Effect<number, Error> => {
    let values = [] as number[];
    while (n > 0) {
        const searchBank = bank.slice(0, bank.length - n + 1);
        const idx = findIdxLargest(searchBank);
        if (Option.isNone(idx)) {
            return Effect.fail(new Error("Out of bounds error."));
        }
        values.push(searchBank[idx.value]);
        bank = bank.slice(idx.value + 1);
        n--;
    }
    return Effect.succeed(Number(values.join("")));
}


const program = pipe(
    Effect.succeed(path.join(process.env.DATA_DIR!, "d3.txt")),
    Effect.andThen(readFile),
    Effect.map(splitLines),
    Effect.map(lines => lines.map(line => line.trim().split('').map(Number))),
    Effect.andThen(banks => Effect.all([
        pipe(
            Effect.succeed(banks.map(b => maxSum(b, 2))),
            Effect.andThen(Effect.all),
            Effect.map(jolts => jolts.reduce((acc, v) => acc + v, 0)),
            Effect.tap(total => console.log(`Total sum of 2 max joltage across banks: ${total}`))
        ),
        pipe(
            Effect.succeed(banks.map(b => maxSum(b, 12))),
            Effect.andThen(Effect.all),
            Effect.map(jolts => jolts.reduce((acc, v) => acc + v, 0)),
            Effect.tap(total => console.log(`Total sum of 12 max joltage across banks: ${total}`))
        ),
    ])),
)

Effect.runPromise(program);
