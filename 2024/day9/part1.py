def main():
    with open("input.txt") as file:
        data = file.read()
    fs = []
    for i, e in enumerate(data):
        if e == "\n":
            break
        for _ in range(int(e)):
            if i % 2 == 0:
                fs.append(i // 2)
            else:
                fs.append(None)

    for i in range(-1, -len(fs), -1):
        if fs[i] is None:
            continue
        next_free = fs.index(None)
        if next_free > len(fs) + i:
            break
        fs[next_free], fs[i] = fs[i], fs[next_free]

    checksum = 0
    for i, e in enumerate(fs):
        if e is not None:
            checksum += i * e
    print(checksum)


if __name__ == "__main__":
    main()
