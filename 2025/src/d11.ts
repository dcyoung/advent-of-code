import { Effect, pipe, Brand } from "effect"
import * as path from "node:path"
import { readFile, splitLines } from "./common.js"

type TMask = Brand.Branded<number, "TMask">;
const asMask = Brand.nominal<TMask>();
type TNode = Brand.Branded<string, "TNode">;
const asNode = Brand.nominal<TNode>();
type TGraph = Brand.Branded<Map<TNode, TNode[]>, "TGraph">;
const asGraph = Brand.nominal<TGraph>();


function parseGraph(lines: string[]) {
    const graph = new Map<TNode, TNode[]>();
    for (const line of lines) {
        const [src, dsts] = line.split(":").map(s => s.trim());
        graph.set(asNode(src), dsts.split(" ").map(d => asNode(d.trim())));
    }
    return asGraph(graph);
}

function pt1(graph: TGraph) {
    const memo = new Map<TNode, number>();
    const dfs = (node: TNode): number => {
        const m = memo.get(node);
        if (m !== undefined) {
            return m;
        }
        if (node === asNode("out")) {
            return 1;
        }
        const count = (graph.get(node) ?? []).map(dfs).reduce((a, b) => a + b, 0);
        memo.set(node, count);
        return count;
    }

    return dfs(asNode("you"));
}

function pt2(graph: TGraph) {
    const src = asNode("svr");
    const dst = asNode("out");
    const memo = new Map<string, number>();

    const dfs = (
        node: TNode,
        // bit 0 = dac visited, bit 1 = fft visited
        mask: TMask
    ): number => {
        const cacheKey = `${node}:${mask}`;
        const m = memo.get(cacheKey);
        if (m !== undefined) {
            return m;
        }
        if (node === dst) {
            return mask === asMask(0b11) ? 1 : 0;
        }
        let count = 0;
        for (const next of graph.get(node) ?? []) {
            let nextMask = mask;
            switch (next) {
                case asNode("dac"):
                    nextMask = asMask(nextMask | asMask(0b01));
                    break;
                case asNode("fft"):
                    nextMask = asMask(nextMask | asMask(0b10));
                    break;
                default:
                    break;
            }
            count += dfs(next, nextMask);
        }
        memo.set(cacheKey, count);
        return count;
    }

    return dfs(src, asMask(0b00));
}


const program = pipe(
    Effect.succeed(path.join(process.env.DATA_DIR!, "d11.txt")),
    Effect.andThen(readFile),
    Effect.map(splitLines),
    Effect.map(parseGraph),
    Effect.andThen(g => Effect.all([
        pipe(
            Effect.succeed(g),
            Effect.map(pt1),
            Effect.tap(total => console.log(`Pt1: ${total}`))
        ),
        pipe(
            Effect.succeed(g),
            Effect.map(pt2),
            Effect.tap(total => console.log(`Pt2: ${total}`))
        ),
    ])),
)

Effect.runPromise(program);
