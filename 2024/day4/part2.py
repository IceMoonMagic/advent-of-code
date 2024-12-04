def check_spot(lines, i, j):
    if i - 1 < 0 or j - 1 < 0 or i + 1 >= len(lines) or j + 1 >= len(lines[i]):
        return False
    return (
        (lines[i - 1][j - 1] == "M" and lines[i + 1][j + 1] == "S")
        or (lines[i - 1][j - 1] == "S" and lines[i + 1][j + 1] == "M")
    ) and (
        (lines[i + 1][j - 1] == "M" and lines[i - 1][j + 1] == "S")
        or (lines[i + 1][j - 1] == "S" and lines[i - 1][j + 1] == "M")
    )


def main():
    with open("part1.input.txt") as file:
        lines = file.readlines()
    count = 0
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "A":
                c = check_spot(lines, i, j)
                print(i + 1, j + 1, c)
                count += c
    print(count)


if __name__ == "__main__":
    main()
