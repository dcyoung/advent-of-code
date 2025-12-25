import { Effect, pipe, Option } from "effect"
import * as path from "node:path"
import { readFile, splitLines } from "./common.js"

type TSpan = [number, number];

const mergeSpans = (a: TSpan, b: TSpan): Option.Option<TSpan> => {
    const x = a[0] < b[0] ? a : b;
    const y = a[0] < b[0] ? b : a;

    if (x[1] < y[0]) {
        return Option.none();
    }
    return Option.some([x[0], Math.max(x[1], y[1])] as TSpan);
}

const reduceSpans = (spans: TSpan[]): TSpan[] => {
    const sorted = spans.sort((a, b) => a[0] - b[0]);
    const reduced: TSpan[] = [];
    let current = sorted[0];
    for (let i = 1; i < sorted.length; i++) {
        const next = sorted[i];
        const merged = mergeSpans(current, next);
        if (Option.isSome(merged)) {
            current = merged.value;
            continue;
        }
        else {
            reduced.push(current);
            current = next;
        }
    }
    reduced.push(current);
    return reduced;
}

const parseInput = (lines: string[]) => {
    const spans = lines.filter(lines => lines.includes("-")).map(line => line.split("-").map(Number) as [number, number])
    const candidates = lines.filter(line => line.trim().length > 0 && !line.includes("-")).map(Number)

    return { spans, candidates };
}

const pt1 = (input: { spans: [number, number][], candidates: number[] }) => {
    const spans = reduceSpans(input.spans);
    return input.candidates.filter(c => spans.find(s => c >= s[0] && c <= s[1]) !== undefined);
}

const pt2 = (spans: TSpan[]) => {
    const reduced = reduceSpans(spans);
    return reduced.map(s => s[1] - s[0] + 1).reduce((acc, v) => acc + v, 0);
}

const program = pipe(
    Effect.succeed(path.join(process.env.DATA_DIR!, "d5.txt")),
    Effect.andThen(readFile),
    Effect.map(splitLines),
    Effect.map(lines => parseInput(lines)),
    Effect.andThen(input => Effect.all([
        pipe(
            Effect.succeed(input),
            Effect.map(pt1),
            Effect.tap(fresh => console.log(`Total fresh ingredients (Pt1): ${fresh.length}`))
        ),
        pipe(
            Effect.succeed(input.spans),
            Effect.map(pt2),
            Effect.tap(total => console.log(`Pt2: ${total}`))
        ),
    ])),
)

Effect.runPromise(program);

