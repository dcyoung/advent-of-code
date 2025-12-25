import { Option, Effect } from "effect"
import * as NodeFS from "node:fs"

export const readFile = (filename: string) =>
    Effect.async<Buffer, Error>((resume) => {
        NodeFS.readFile(filename, (error, data) => {
            if (error) {
                // Resume with a failed Effect if an error occurs
                resume(Effect.fail(error))
            } else {
                // Resume with a succeeded Effect if successful
                resume(Effect.succeed(data))
            }
        })
    })

export const splitLines = (fileContent: Buffer) => fileContent.toString().split("\n")



export const findIdxLargest = (arr: number[]): Option.Option<number> => {
    let bestIdx = -1;
    let bestValue = -1;
    arr.forEach((b, idx) => {
        if (b > bestValue) {
            bestValue = b;
            bestIdx = idx;
        }
    });
    return bestIdx >= 0 ? Option.some(bestIdx) : Option.none();
}


export const pairwise = <T>(arr: T[]) => {
    const n = arr.length
    const pairs = [];
    for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
            pairs.push([arr[i], arr[j]] as [T, T])
        }
    }
    return pairs;
}


export function arraysEqual<T>(a: T[], b: T[]) {
    if (a.length !== b.length) return false;

    for (let i = 0; i < a.length; i++) {
        if (a[i] !== b[i]) return false;
    }

    return true;
}