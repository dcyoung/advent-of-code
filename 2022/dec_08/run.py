from functools import reduce
import operator
import numpy as np

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()

    trees = np.asarray([[int(c) for c in l.strip()] for l in lines])
    print(trees.shape)
    print(trees[:5, :5])

    visible = set()

    for i in range(trees.shape[0]):
        for j, v in enumerate(trees[i]):
            if i == 0 or j == 0 or i == trees.shape[0] - 1 or j == trees.shape[1] - 1:
                visible.add((i, j))
                continue
            if (
                v > np.max(trees[:i, j])
                or v > np.max(trees[i, :j])
                or v > np.max(trees[i + 1 :, j])
                or v > np.max(trees[i, j + 1 :])
            ):
                visible.add((i, j))

    print(len(visible))

    scenic_scores = np.zeros_like(trees)
    for i in range(trees.shape[0]):
        for j, v in enumerate(trees[i]):
            # left, right, top, bottom
            scalars = [0, 0, 0, 0]
            for x in range(i - 1, -1, -1):
                scalars[0] += 1
                if trees[x, j] >= v:
                    break
            for x in range(i + 1, trees.shape[0]):
                scalars[1] += 1
                if trees[x, j] >= v:
                    break
            for x in range(j - 1, -1, -1):
                scalars[2] += 1
                if trees[i, x] >= v:
                    break
            for x in range(j + 1, trees.shape[1]):
                scalars[3] += 1
                if trees[i, x] >= v:
                    break
            scenic_scores[i, j] = reduce(operator.mul, scalars, 1)
    print(scenic_scores[:5, :5])

    print(np.amax(scenic_scores))
