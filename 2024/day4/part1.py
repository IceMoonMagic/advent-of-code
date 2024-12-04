def check_spot(lines, i, j):
    count = 0
    for i_mod in range(-1, 2):
        for j_mod in range(-1, 2):
            if check_dir(lines, i, j, i_mod, j_mod):
                count += 1
    return count


def check_dir(lines, i, j, i_mod, j_mod):
    try:
        if (
            i + i_mod * 3 < 0
            or j + j_mod * 3 < 0
            or i + i_mod * 3 >= len(lines)
            or j + j_mod * 3 >= len(lines[i])
        ):
            return False
        return (
            lines[i][j] == "X"
            and lines[i + i_mod][j + j_mod] == "M"
            and lines[i + i_mod * 2][j + j_mod * 2] == "A"
            and lines[i + i_mod * 3][j + j_mod * 3] == "S"
        )
    except IndexError:
        return False


def main():
    with open("part1.input.txt") as file:
        lines = file.readlines()
    count = 0
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "X":
                c = check_spot(lines, i, j)
                print(i + 1, j + 1, c)
                count += c
    print(count)


if __name__ == "__main__":
    main()
