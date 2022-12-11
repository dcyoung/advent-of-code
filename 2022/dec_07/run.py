from pathlib import Path

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()
        # text = f.read().strip()

    results = {}
    cwd = None
    # Group lines from the same directory
    for line in lines:
        if line.startswith("$ cd"):
            dir_name = line.strip()[5:].strip()
            if dir_name == "/":
                cwd = Path(dir_name)
            elif dir_name == "..":
                cwd = cwd.parent
            else:
                cwd = cwd / dir_name
            continue
        if line.startswith("$ ls") or line.startswith("dir"):
            continue
        fsize = int(line.split()[0])
        x = cwd
        results[str(x.absolute())] = results.get(str(x.absolute()), 0) + fsize
        while x != x.parent:
            x = x.parent
            results[str(x.absolute())] = results.get(str(x.absolute()), 0) + fsize

    valid = {k: v for k, v in results.items() if v <= 100000}
    print(valid.keys())
    print(sum(valid.values()))

    FS_SIZE = 70000000
    REQUIRED = 30000000
    delta = REQUIRED - (FS_SIZE - results["/"])
    print(delta)
    valid = sorted(
        [(k, v) for k, v in results.items() if v >= delta], key=lambda x: x[1]
    )
    print(valid)
    print(valid[0])
