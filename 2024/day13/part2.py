import re
from fractions import Fraction

COST_A = 3
COST_B = 1


def press_buttons(
    ax: Fraction,
    ay: Fraction,
    bx: Fraction,
    by: Fraction,
    px: Fraction,
    py: Fraction,
) -> int:
    px += 10_000_000_000_000
    py += 10_000_000_000_000

    slope_a = Fraction(ay, ax)
    slope_b = Fraction(by, bx)

    if (py < slope_a * px and py < slope_b * px) or (
        py > slope_a * px and py > slope_b * px
    ):
        return 0

    # https://www.desmos.com/calculator/e96mqkm2e6

    # ay / ax * x = (by * (x - px)) / bx + py
    intercept_x = (ax * (by * px - bx * py)) / (ax * by - ay * bx)

    # # by / bx * x = (ax * (x - px)) / ay + py
    # x2 = (bx * (ay * px - ax * py)) / (bx * ay - by * ax)

    cost = (intercept_x / ax) * COST_A + (px - intercept_x) / bx * COST_B

    return (
        cost.numerator if intercept_x.is_integer() and cost.is_integer() else 0
    )


def main():
    with open("input.txt") as file:
        data = file.read()
    matches = re.findall(
        r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)",
        data,
    )
    tally = 0
    for match in matches:
        cost = press_buttons(*(Fraction(group) for group in match))
        # print(cost)
        tally += cost
    print(tally)


if __name__ == "__main__":
    main()
