def blink(prev: list[int]) -> list[int]:
    result = []
    for stone in prev:
        match stone:
            case 0:
                result.append(1)
            case stone if len(str_stone := str(stone)) % 2 == 0:
                result.append(int(str_stone[: len(str_stone) // 2]))
                result.append(int(str_stone[len(str_stone) // 2 :]))
            case _:
                result.append(stone * 2024)
    return result


def main():
    with open("input.txt") as file:
        data = [int(i) for i in file.read().split(" ")]
    for _ in range(25):
        data = blink(data)
    print(len(data))


if __name__ == "__main__":
    main()
