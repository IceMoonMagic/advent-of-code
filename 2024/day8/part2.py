from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])


def find_antinodes(positions: set[Position], br: Position) -> set[Position]:
    positions = list(positions)
    result: set[Position] = set()
    for i, antenna1 in enumerate(positions):
        result.add(antenna1)
        for antenna2 in positions[i + 1 :]:
            difference = Position(
                antenna2.x - antenna1.x, antenna2.y - antenna1.y
            )
            pos = Position(
                antenna1.x - difference.x, antenna1.y - difference.y
            )
            while 0 <= pos.x < br.x and 0 <= pos.y < br.y:
                result.add(pos)
                pos = Position(pos.x - difference.x, pos.y - difference.y)

            pos = Position(
                antenna2.x + difference.x, antenna2.y + difference.y
            )
            while 0 <= pos.x < br.x and 0 <= pos.y < br.y:
                result.add(pos)
                pos = Position(pos.x + difference.x, pos.y + difference.y)
    return result


def main():
    with open("input.txt") as file:
        data = file.read().splitlines()

    antenna: dict[str, set[Position]] = {}
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char in ".#":
                continue
            if char not in antenna:
                antenna[char] = set()
            antenna[char].add(Position(x, y))
    br = Position(len(data[0]), len(data))
    antinodes: set[Position] = set()
    for char, positions in antenna.items():
        antinodes.update(find_antinodes(positions, br))
    print(len(antinodes))


if __name__ == "__main__":
    main()
