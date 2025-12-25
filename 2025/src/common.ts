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