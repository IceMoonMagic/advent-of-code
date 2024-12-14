def blink(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1
    match stone:
        case 0:
            return blink(1, blinks - 1)
        case stone if len(str_stone := str(stone)) % 2 == 0:
            return blink(
                int(str_stone[: len(str_stone) // 2]), blinks - 1
            ) + blink(int(str_stone[len(str_stone) // 2 :]), blinks - 1)
        case _:
            return blink(stone * 2024, blinks - 1)


def main():
    with open("input.txt") as file:
        data = [int(i) for i in file.read().split(" ")]
    total = 0
    for stone in data:
        print("starting", stone)
        total += blink(stone, 75)
    print(total)


if __name__ == "__main__":
    main()
