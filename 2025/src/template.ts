import { Effect, pipe } from "effect"
import * as path from "node:path"
import { readFile, splitLines } from "./common.js"

const program = pipe(
    Effect.succeed(path.join(process.env.DATA_DIR!, "dX_example.txt")),
    Effect.andThen(readFile),
    Effect.map(splitLines),
    Effect.map(lines => lines.map(line => line.trim())),
    Effect.andThen(items => Effect.all([
        pipe(
            Effect.succeed(items.map(b => pt1(b, 2))),
            Effect.andThen(Effect.all),
            Effect.map(results => results.reduce((acc, v) => acc + v, 0)),
            Effect.tap(total => console.log(`Pt1: ${total}`))
        ),
        // pipe(
        //     Effect.succeed(items.map(b => pt2(b, 2))),
        //     Effect.andThen(Effect.all),
        //     Effect.map(results => results.reduce((acc, v) => acc + v, 0)),
        //     Effect.tap(total => console.log(`Pt2: ${total}`))
        // ),
    ])),
)

Effect.runPromise(program);
