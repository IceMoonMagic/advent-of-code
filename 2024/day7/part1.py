def check_line(line):
    total = int(line[: line.find(":")])
    operands = [int(o) for o in line[line.find(":") + 2 :].split()]

    def check(actual, ops):
        if len(ops) == 0:
            return total == actual

        for op in ["__add__", "__mul__"]:
            if check(getattr(actual, op)(ops[0]), ops[1:]):
                return True
        return False

    if check(operands[0], operands[1:]):
        return total
    return 0


def main():
    with open("input.txt") as file:
        data = file.read().splitlines()
    total = 0
    for line in data:
        total += check_line(line)
    print(total)


if __name__ == "__main__":
    main()
