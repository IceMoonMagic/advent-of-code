def check_line(line):
    total = int(line[: line.find(":")])
    operands = [int(o) for o in line[line.find(":") + 2 :].split()]

    def check(actual, ops):
        if len(ops) == 0:
            return total == actual

        for op in ["+", "*", "||"]:
            match op:
                case "+":
                    calc = actual + ops[0]
                case "*":
                    calc = actual * ops[0]
                case "||":
                    calc = int(f"{actual}{ops[0]}")
                case _:
                    raise RuntimeError

            if check(calc, ops[1:]):
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
