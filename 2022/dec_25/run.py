POW_5 = [5**i for i in range(40)]


def int_to_snafu(x: int) -> str:
    vals = len(POW_5) * [0]

    for i, p in enumerate(POW_5):
        rem = x % p
        if rem == 0:
            continue

        prev_i = i - 1
        prev_p = POW_5[prev_i]
        count_prev = rem // prev_p
        if count_prev <= 2:
            vals[prev_i] += count_prev
        elif count_prev == 3:
            vals[prev_i] += -2
            vals[i] += 1
        elif count_prev == 4:
            vals[prev_i] += -1
            vals[i] += 1
        else:
            raise ValueError()
        if vals[prev_i] == 3:
            vals[prev_i] = -2
            vals[i] += 1
        if vals[prev_i] == 4:
            vals[prev_i] = -1
            vals[i] + 1
        x -= rem
    while vals and vals[-1] == 0:
        vals.pop()
    return "".join([parse_snafu(x) for x in vals[::-1]])


def parse_snafu(x: int) -> str:
    return {
        0: str(0),
        1: str(1),
        2: str(2),
        -1: "-",
        -2: "=",
    }[x]


def parse_digit(s: str) -> int:
    if s == "=":
        return -2
    if s == "-":
        return -1
    return int(s)


def snafu_to_int(s: str) -> int:
    digits = [parse_digit(x) for x in s]
    return sum([(5**i) * d for i, d in enumerate(digits[::-1])])


if __name__ == "__main__":
    fpath = "test_input.txt"
    with open(fpath, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # for s in lines:
    #     print(s, snafu_to_int(s), int_to_snafu(x=snafu_to_int(s)))
    total = sum([snafu_to_int(s) for s in lines])
    print("Part #1: ", total, int_to_snafu(x=total))
