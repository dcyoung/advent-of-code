import { Effect, pipe } from "effect"
import * as path from "node:path"
import { readFile, splitLines } from "./common.js"

class Node {
    r: number;
    c: number;
    constructor(r: number, c: number) {
        this.r = r;
        this.c = c;
    }

    key(): string {
        return `${this.r},${this.c}`;
    }
}

class Graph {
    public nodes;
    constructor(lines: string[]) {
        this.nodes = new Map<string, Node>();
        for (let r = 0; r < lines.length; r++) {
            for (let c = 0; c < lines[r].length; c++) {
                if (lines[r][c] === "@") {
                    const node = new Node(r, c);
                    this.nodes.set(node.key(), node);
                }
            }
        }
    }

    public solveEdges() {
        const edges = new Map<string, Node[]>();
        for (const n of this.nodes.values()) {
            edges.set(n.key(), this.getOccupiedNeighbors(n));
        }
        return edges;
    }

    private isOccupied(node: Node): boolean {
        return this.nodes.has(node.key());
    }

    private getOccupiedNeighbors(node: Node): Node[] {
        return [
            new Node(node.r - 1, node.c),
            new Node(node.r + 1, node.c),
            new Node(node.r - 1, node.c - 1),
            new Node(node.r + 1, node.c - 1),
            new Node(node.r - 1, node.c + 1),
            new Node(node.r + 1, node.c + 1),
            new Node(node.r, node.c - 1),
            new Node(node.r, node.c + 1),
        ].filter(v => this.isOccupied(v));
    }

    public nextFreeNode() {
        // iterate through this.nodes.values() until a node with fewer than 4 neighbors is found
        for (const n of this.nodes.values()) {
            const neighbors = this.getOccupiedNeighbors(n);
            if (neighbors.length < 4) {
                return n;
            }
        }
        return undefined;
    }
}

const solvePart1 = (graph: Graph): number => {
    // move through nodes...
    let total = 0;
    for (const [_, neighbors] of graph.solveEdges()) {
        if (neighbors.length < 4) {
            total++;
        }
    }
    return total;
}



const solvePart2 = (graph: Graph): number => {
    // move through nodes...
    let total = 0;
    let nextNode = graph.nextFreeNode();
    while (nextNode) {
        total++;
        graph.nodes.delete(nextNode.key());
        nextNode = graph.nextFreeNode();
    }
    return total;
}


const program = pipe(
    Effect.succeed(path.join(process.env.DATA_DIR!, "d4.txt")),
    Effect.andThen(readFile),
    Effect.map(splitLines),
    Effect.map(lines => new Graph(lines)),
    Effect.andThen(graph => Effect.all([
        pipe(
            Effect.succeed(graph),
            Effect.map(graph => solvePart1(graph)),
            Effect.tap(total => console.log(`Total accesible rolls (pt1): ${total}`))
        ),
        pipe(
            Effect.succeed(graph),
            Effect.map(graph => solvePart2(graph)),
            Effect.tap(total => console.log(`Total accesible rolls (pt2): ${total}`))
        ),
    ])),
)

Effect.runPromise(program);
