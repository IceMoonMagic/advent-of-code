from functools import cache
from itertools import permutations

BUTTON_PAD = tuple[tuple[str, ...], ...]

NUM_PAD: BUTTON_PAD = (
    ("7", "8", "9"),
    ("4", "5", "6"),
    ("1", "2", "3"),
    ("", "0", "A"),
)
D_PAD: BUTTON_PAD = (
    ("", "^", "A"),
    ("<", "v", ">"),
)


@cache
def find_button_location(
    button: str, button_pad: BUTTON_PAD
) -> tuple[int, int]:
    for y, row in enumerate(button_pad):
        for x, char in enumerate(row):
            if char == button:
                return x, y
    raise ValueError


@cache
def follow_sequence(
    sequence: str, button_pad: BUTTON_PAD, start_at: tuple[int, int]
) -> tuple[list[str], str]:
    # over = [start_at]
    over = []
    result: str = ""
    # pos = find_button_location(start_at, button_pad)
    pos = start_at
    for move in sequence:
        match move:
            case "A":
                result += button_pad[pos[1]][pos[0]]
                continue
            case "<":
                pos = pos[0] - 1, pos[1]
            case ">":
                pos = pos[0] + 1, pos[1]
            case "^":
                pos = pos[0], pos[1] - 1
            case "v":
                pos = pos[0], pos[1] + 1
            case "_":
                pass
        over.append(button_pad[pos[1]][pos[0]])
    # print(over, result, sequence)
    return over, result


@cache
def avoid_gaps(
    sequence: str, button_pad: BUTTON_PAD, start_at: tuple[int, int]
) -> str:
    if "" not in follow_sequence(sequence, button_pad, start_at)[0]:
        return sequence
    first_dir = sequence[0]
    last_first_dir = sequence.rfind(first_dir)
    return sequence[last_first_dir + 1 :] + sequence[: last_first_dir + 1]
    # for perm in permutations(sequence):
    #     if "" not in follow_sequence("".join(perm), button_pad, start_at)[0]:
    #         return "".join(perm)
    # raise ValueError


def button_sequence(
    sequence: str, button_pad: BUTTON_PAD, start_at: str
) -> str:
    result = ""
    pos = find_button_location(start_at, button_pad)
    for button in sequence:
        sub_result = ""
        target = find_button_location(button, button_pad)
        diff: tuple[int, int] = target[0] - pos[0], target[1] - pos[1]
        if diff[0] > 0:
            sub_result += ">" * diff[0]
        elif diff[0] < 0:
            sub_result += "<" * -diff[0]
        if diff[1] > 0:
            sub_result += "v" * diff[1]
        elif diff[1] < 0:
            sub_result += "^" * -diff[1]
        result += avoid_gaps(sub_result, button_pad, pos)
        # result += sub_result
        result += "A"
        pos = target
    return result


def get_complexity(code: str, sequence: str) -> int:
    return int(code[:-1]) * len(sequence)


def main():
    with open("input.txt") as file:
        data = file.read().splitlines()
    # sequences = (button_sequence(code) for code in data)
    tally = 0
    for code in data:
        seq = button_sequence(code, NUM_PAD, "A")
        for _ in range(2):
            seq = button_sequence(seq, D_PAD, "A")
        tally += get_complexity(code, seq)
        print(code, len(seq), seq)
    pass
    print(tally)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, InterruptedError):
        print()
