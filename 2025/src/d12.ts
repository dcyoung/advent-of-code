import { Effect, pipe, Brand } from "effect"
import * as path from "node:path"
import { readFile, splitLines } from "./common.js"

class Shape {
    constructor(private lines: string[]) {

    }

    public get height(): number {
        return this.lines.length;
    }

    public get width(): number {
        return this.lines.at(0)?.length ?? 0;
    }

    public get area(): number {
        return this.height * this.width;
    }

    public get interiorArea(): number {
        return this.lines.reduce((acc, line) => {
            return acc + line.split("").filter(c => c === "#").length;
        }, 0);
    }
}

class Region {
    constructor(
        public height: number,
        public width: number,
    ) {

    }

    get area(): number {
        return this.height * this.width;
    }
}

class Problem {
    constructor(
        private region: Region,
        private shapeCounts: number[]
    ) {

    }
    public fits(shapes: Shape[]) {
        // if (this.shapeCounts.map(x => x.shape).some(shape => Math.max(shape.height, shape.width) > Math.max(this.region.height, this.region.width))) {
        //     return false;
        // }
        let totalArea = 0;
        let totalInteriorArea = 0;
        for (let i = 0; i < shapes.length; i++) {
            const shape = shapes[i]!;
            const count = this.shapeCounts[i]!;
            totalArea += shape.area * count;
            totalInteriorArea += shape.interiorArea * count;
        }

        if (totalArea < this.region.area) {
            return true;
        }
        if (totalInteriorArea > this.region.area) {
            return false;
        }
        return true;
    }
}

const pt1 = (s: string) => {
    const sections = s.split("\n\n").filter(s => s.trim() !== "");
    const regionStr = sections.pop()!;
    const shapes = sections.map(section => new Shape(
        section
            .split("\n")
            // skip first line (id)
            .slice(1))
    );

    const problems = regionStr.split("\n").map(line => {
        const [size, rest] = line.trim().split(":").map(s => s.trim());
        const [height, width] = size.split("x").map(Number);
        const shapeCounts = rest.split(" ").map(c => Number(c));
        const region = new Region(
            height,
            width,
        );
        return new Problem(region, shapeCounts);
    });

    return problems.filter(prob => prob.fits(shapes)).length;
}



const program = pipe(
    Effect.succeed(path.join(process.env.DATA_DIR!, "d12.txt")),
    Effect.andThen(readFile),
    Effect.map(b => b.toString()),
    Effect.map(pt1),
    Effect.tap(total => console.log(`Pt1: ${total}`))
)

Effect.runPromise(program);
