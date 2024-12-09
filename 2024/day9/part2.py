def line_to_list(data: str) -> list[int | None]:
    fs = []
    for i, e in enumerate(data):
        if e == "\n":
            break
        for _ in range(int(e)):
            if i % 2 == 0:
                fs.append(i // 2)
            else:
                fs.append(None)
    return fs


def checksum(filesystem: list[int | None]) -> int:
    _checksum = 0
    for i, e in enumerate(filesystem):
        if e is not None:
            _checksum += i * e
    return _checksum


def rearrange(fs: list[int | None]):
    def find_left_bound(right: int) -> int:
        if right - 1 > -len(fs) and fs[right] == fs[right - 1]:
            return find_left_bound(right - 1)
        return right

    def find_right_bound(left: int) -> int:
        if left + 1 < len(fs) and fs[left] == fs[left + 1]:
            return find_right_bound(left + 1)
        return left

    def find_space(size_: int) -> int | None:
        for i, e in enumerate(fs):
            if e is None:
                right = find_right_bound(i)
                if right - i + 1 >= size_:
                    return i

    def swap(start1, start2, size_):
        for i in range(size_):
            fs[start1 + i], fs[start2 + i] = fs[start2 + i], fs[start1 + i]

    skip: int | None = None
    for j in range(-1, -len(fs), -1):
        if fs[j] is None or fs[j] == skip:
            continue
        file_left = find_left_bound(j)
        size = j - file_left + 1
        space_left = find_space(size)
        if space_left is None or file_left + len(fs) < space_left:
            skip = fs[j]
            continue
        swap(file_left, space_left, size)


def main():
    with open("input.txt") as file:
        data = file.read()
    fs = line_to_list(data)
    import sys

    # print(sys.getrecursionlimit())
    sys.setrecursionlimit(len(fs) + 3)
    # print(sys.getrecursionlimit())
    rearrange(fs)
    print(checksum(fs))


if __name__ == "__main__":
    main()
