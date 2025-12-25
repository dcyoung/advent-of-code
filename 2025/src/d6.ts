import { Effect, pipe, Option } from "effect"
import * as path from "node:path"
import { readFile, splitLines } from "./common.js"

class Op {
    private values: number[];
    constructor(private readonly op: "*" | "+") {
        this.values = [];
    }

    public addValue(value: number) {
        this.values.push(value);
    }

    public compute(): number {
        switch (this.op) {
            case "*":
                return this.values.reduce((acc, v) => acc * v, 1);
            case "+":
                return this.values.reduce((acc, v) => acc + v, 0);
        }
    };
}

const parseOp = (opStr: string): Op => {
    switch (opStr) {
        case "*": return new Op("*");
        case "+": return new Op("+");
        default: throw new Error(`Unknown operation: ${opStr}`);
    }
}



const parseInputPt1 = (lines: string[]) => {
    lines = [...lines];
    const ops = lines.pop()!.trim().split(" ")
        .map(s => s.trim())
        .filter(s => s.length > 0)
        .map(parseOp);

    for (const line of lines) {
        line.trim().split(" ")
            .map(s => s.trim())
            .filter(s => s.length > 0)
            .map((val, idx) => {
                ops[idx].addValue(Number(val));
            })
    }
    return ops;
}

const parseInputPt2 = (lines: string[]) => {
    lines = [...lines];
    const grid: string[][] = lines.map(line => line.split(""));
    const opsRow = grid.pop()!;
    const opsIdxs = opsRow
        .map((c, idx) => c.trim().length > 0 ? Option.some(idx) : Option.none())
        .filter(o => Option.isSome(o))
        .map(o => o.value);

    const ops = [];
    while (opsIdxs.length > 0) {
        const startIdxInclusive = opsIdxs.shift()!;
        const nextStartIdx = opsIdxs.at(0);
        const endIdxExclusive = nextStartIdx !== undefined ?
            nextStartIdx - 1 : opsRow.length;
        const op = parseOp(opsRow[startIdxInclusive]);

        for (let colIdx = startIdxInclusive; colIdx < endIdxExclusive; colIdx++) {
            op.addValue(
                Number(grid.map(row => row[colIdx]).filter(c => !!c).join("").trim())
            )
        }
        ops.push(op);
    }
    return ops;
}


const program = pipe(
    Effect.succeed(path.join(process.env.DATA_DIR!, "d6.txt")),
    Effect.andThen(readFile),
    Effect.map(splitLines),
    Effect.andThen(lines => Effect.all([
        pipe(
            Effect.succeed(lines),
            Effect.map(parseInputPt1),
            Effect.map(ops => ops.map(op => op.compute())),
            Effect.map(results => results.reduce((acc, v) => acc + v, 0)),
            Effect.tap(total => console.log(`Pt1: ${total}`))
        ),
        pipe(
            Effect.succeed(lines),
            Effect.map(parseInputPt2),
            Effect.map(ops => ops.map(op => op.compute())),
            Effect.map(results => results.reduce((acc, v) => acc + v, 0)),
            Effect.tap(total => console.log(`Pt2: ${total}`))
        ),
    ])),
)

Effect.runPromise(program);
