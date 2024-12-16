import re


def press_buttons(ax: int, ay: int, bx: int, by: int, px: int, py: int) -> int:
    def _press_buttons(at_x, at_y, press_a=True) -> int:
        if at_x == px and at_y == py:
            return 0
        if at_x >= px or at_y >= py:
            return -5

        a = _press_buttons(at_x + ax, at_y + ay) + 3 if press_a else -1
        b = _press_buttons(at_x + bx, at_y + by, False) + 1

        if a < 0 and b < 0:
            return -5
        return a if 0 < a < b or b < 0 else b

    foo = max(0, _press_buttons(0, 0))
    return foo


def main():
    with open("input.txt") as file:
        data = file.read()
    matches = re.findall(
        r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)",
        data,
    )
    tally = 0
    for match in matches:
        cost = press_buttons(*(int(group) for group in match))
        # print(cost)
        tally += cost
    print(tally)


if __name__ == "__main__":
    main()
