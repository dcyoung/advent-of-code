if __name__ == "__main__":
    with open("input.txt", "r") as f:
        text = f.read().strip()

    starts = []
    for i in range(14, len(text)):
        if len(set(text[i - 14 : i])) == 14:
            starts.append(i)

    print(starts[:5])
