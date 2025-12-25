import { Effect, pipe, Option, Brand } from "effect"
import * as path from "node:path"
import { readFile, splitLines, arraysEqual } from "./common.js"


type TJoltage = number[] & Brand.Brand<"joltage">;
type TMask = number & Brand.Brand<"button_mask">;
type TNumClicks = number & Brand.Brand<"num_clicks">
const asJoltage = Brand.nominal<TJoltage>();
const asMask = Brand.nominal<TMask>();
const asNumClicks = Brand.nominal<TNumClicks>();

type Machine = {
    targetBitMask: TMask;
    switchBitMasks: TMask[];
    joltage: TJoltage;
};


function indicesToBitmask(indices: number[]): TMask {
    let mask = 0;
    for (const i of indices) {
        mask |= (1 << i);
    }
    return asMask(mask);
}


function parseMachine(line: string): Machine {
    const targetLightIdxs = line
        .match(/^\[([.#]+)\]/)![0]
        .trim()
        .split("")
        .slice(1, -1)
        .map((c, i) => c === "#" ? Option.some(i) : Option.none())
        .filter(Option.isSome)
        .map(o => o.value);
    const switches = Array.from(line.matchAll(/\(([\d,]+)\)/g))
        .map(m => m[0]
            .trim()
            .slice(1, -1)
            .split(",")
            .map(Number)
        );
    const joltage = line.match(/\{([\d,]+)\}$/)![0].trim().slice(1, -1).split(",").map(Number);
    return {
        targetBitMask: indicesToBitmask(targetLightIdxs),
        switchBitMasks: switches.map(indicesToBitmask),
        joltage: asJoltage(joltage),
    };
}


function pt1(mask: TMask, targetMask: TMask, switchMasks: TMask[]): Option.Option<TNumClicks> {
    if (mask === targetMask) {
        return Option.some(asNumClicks(0));
    }

    switchMasks = [...switchMasks];
    if (switchMasks.length === 0) {
        return Option.none();
    }
    const nextMask = switchMasks.shift()!;
    const woPress = pt1(mask, targetMask, switchMasks);
    const wPress = pt1(asMask(mask ^ nextMask), targetMask, switchMasks);

    const min = Math.min(
        Option.isSome(woPress) ? woPress.value : Number.POSITIVE_INFINITY,
        Option.isSome(wPress) ? wPress.value + 1 : Number.POSITIVE_INFINITY
    );

    if (min === Number.POSITIVE_INFINITY) {
        return Option.none();
    }
    return Option.some(asNumClicks(min));
}

function applyMaskIncrement(joltages: TJoltage, mask: TMask): TJoltage {
    // Make a copy so original array is not mutated
    const result = [...joltages];

    for (let i = 0; i < result.length; i++) {
        if ((mask >> i) & 1) {
            result[i]++; // increment if the bit is set
        }
    }

    return asJoltage(result);
}


// helper to compute the pattern (mod 2)
function pattern(jolts: TJoltage): TJoltage {
    return jolts.map(n => n % 2) as TJoltage;
}

// helper to compute press effect of a set of buttons
function press(btns: TMask[], numCounters: number): TJoltage {
    const result = new Array(numCounters).fill(0);
    for (let i = 0; i < numCounters; i++) {
        for (const b of btns) {
            if ((b >> i) & 1) result[i]++;
        }
    }
    return result as TJoltage;
}

// sub_halve: element-wise (a-b)/2
function subHalve(jA: TJoltage, jB: TJoltage): TJoltage {
    return jA.map((a, i) => Math.floor((a - jB[i]) / 2)) as TJoltage;
}

// convert array to string key for Map
function key(jolts: TJoltage) {
    return jolts.join(",");
}

function* allCombos<T>(arr: T[]): Generator<T[]> {
    const n = arr.length;
    for (let mask = 0; mask < (1 << n); mask++) {
        const combo: T[] = [];
        for (let i = 0; i < n; i++) {
            if ((mask >> i) & 1) combo.push(arr[i]);
        }
        yield combo;
    }
}

function groupByPattern(buttons: TMask[], numCounters: number): Map<string, TMask[][]> {
    const map = new Map<string, TMask[][]>();

    for (const combo of allCombos(buttons)) {
        const p = pattern(press(combo, numCounters));
        const k = key(p);
        const arr = map.get(k) ?? [];
        arr.push(combo);
        map.set(k, arr);
    }

    return map;
}

function joltageCost(buttons: TMask[], target: TJoltage): number {
    const numCounters = target.length;
    const pressPatterns = groupByPattern(buttons, numCounters);
    const memo = new Map<string, number>();

    function cost(jolts: TJoltage): number {
        const k = key(jolts);
        if (memo.has(k)) return memo.get(k)!;

        if (jolts.every(j => j === 0)) return 0;
        if (jolts.some(j => j < 0) || !pressPatterns.has(key(pattern(jolts)))) {
            return target.reduce((a, b) => a + b, 0); // "infinite" cost
        }

        const combos = pressPatterns.get(key(pattern(jolts)))!;
        let minCost = Infinity;

        for (const btns of combos) {
            const next = subHalve(jolts, press(btns, numCounters));
            const c = btns.length + 2 * cost(next);
            if (c < minCost) minCost = c;
        }

        memo.set(k, minCost);
        return minCost;
    }

    return cost(target);
}

function pt2(m: Machine): Option.Option<TNumClicks> {
    const buttons = m.switchBitMasks;
    const target = m.joltage;
    const presses = joltageCost(buttons, target);
    return Option.some(asNumClicks(presses));
}


const program = pipe(
    Effect.succeed(path.join(process.env.DATA_DIR!, "d10.txt")),
    Effect.andThen(readFile),
    Effect.map(splitLines),
    Effect.map(lines => lines.map(parseMachine)),
    Effect.andThen(machines => Effect.all([
        pipe(
            Effect.succeed(machines.map(m => pt1(0, m.targetBitMask, m.switchBitMasks)).map(
                r => Option.isSome(r) ? Effect.succeed(r.value) : Effect.fail("No solution found")
            )),
            Effect.andThen(Effect.all),
            Effect.map(results => results.reduce((acc, v) => acc + v, 0)),
            Effect.tap(total => console.log(`Pt1: ${total}`))
        ),
        pipe(
            Effect.succeed(machines.map(m => pt2(m)).map(
                r => Option.isSome(r) ? Effect.succeed(r.value) : Effect.fail("No solution found")
            )),
            Effect.andThen(Effect.all),
            Effect.map(results => results.reduce((acc, v) => acc + v, 0)),
            Effect.tap(total => console.log(`Pt2: ${total}`))
        ),
    ])),
)

Effect.runPromise(program);
