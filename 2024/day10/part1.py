from collections import namedtuple


Position = namedtuple("Position", ["x", "y"])


def is_valid_position(data: list[list[int]], pos: Position) -> bool:
    return 0 <= pos.y < len(data) and 0 <= pos.x < len(data[pos.y])


def find_trails(
    data: list[list[int]], pos: Position, prev: int = -1
) -> set[Position]:
    if not is_valid_position(data, pos) or prev + 1 != data[pos.y][pos.x]:
        return set()
    here = data[pos.y][pos.x]
    if here == 9:
        return {pos}
    return (
        find_trails(data, pos._replace(x=pos.x - 1), here)
        .union(find_trails(data, pos._replace(x=pos.x + 1), here))
        .union(find_trails(data, pos._replace(y=pos.y - 1), here))
        .union(find_trails(data, pos._replace(y=pos.y + 1), here))
    )


def main():
    with open("input.txt") as file:
        data = file.read().splitlines()
    topo = [[int(char) for char in line] for line in data]
    score = 0
    for y, line in enumerate(topo):
        for x in range(len(line)):
            trail_tails = find_trails(topo, Position(x, y))
            score += len(trail_tails)

    print(score)


if __name__ == "__main__":
    main()
