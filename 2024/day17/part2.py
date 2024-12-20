import re


def get_combo_operand(operand: int, registers: dict[str, int]) -> int:
    match operand:
        case 1:
            return 1
        case 2:
            return 2
        case 3:
            return 3
        case 4:
            return registers["A"]
        case 5:
            return registers["B"]
        case 6:
            return registers["C"]
        case 7:
            return NotImplemented
        case _:
            return NotImplemented


def run(
    registers: dict[str, int], instructions: tuple[int, ...]
) -> tuple[int, ...]:
    pointer = 0
    out: list[int] = []

    while pointer < len(instructions):
        operand = instructions[pointer + 1]
        combo_operand = get_combo_operand(operand, registers)
        match instructions[pointer]:
            case 0:  # adv
                registers["A"] = registers["A"] // (2**combo_operand)
            case 1:  # bxl
                registers["B"] = registers["B"] ^ operand
            case 2:  # bst
                registers["B"] = combo_operand % 8
            case 3:  # jnz
                if registers["A"] != 0:
                    pointer = operand
                    continue
            case 4:  # bxc
                registers["B"] = registers["B"] ^ registers["C"]
            case 5:  # out
                out.append(combo_operand % 8)
            case 6:  # bdv
                registers["B"] = registers["A"] // (2**combo_operand)
            case 7:  # cdv
                registers["C"] = registers["A"] // (2**combo_operand)
        pointer += 2

    return tuple(out)


def run_a(
    a: int, registers: dict[str, int], instructions: tuple[int, ...]
) -> tuple[int, ...]:
    registers = registers.copy()
    registers["A"] = a
    result = run(registers, instructions)
    print(a, oct(a), result)
    return result


def main():
    with open("input.txt") as file:
        data = file.read()
    data_re = re.match(
        r"Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: ([\d,]+)",
        data,
    )
    registers: dict[str, int] = {
        "A": int(data_re.group(1)),
        "B": int(data_re.group(2)),
        "C": int(data_re.group(3)),
    }
    instructions = tuple(int(op) for op in data_re.group(4).split(","))

    def _main(power: int, new_a: int) -> None | int:
        if power < 0:
            return new_a
        for i in range(0, 8):
            test_a = new_a + i * 8**power
            results = run_a(test_a, registers, instructions)
            if results[power - 15 - 1 :] == instructions[power - 15 - 1 :]:
                result = _main(power - 1, test_a)
                if result is not None:
                    return result

    print(_main(15, 0o0000000000000000))


if __name__ == "__main__":
    main()
