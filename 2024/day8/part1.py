from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])


def find_antinodes(positions: set[Position]) -> set[Position]:
    positions = list(positions)
    result: set[Position] = set()
    for i, antenna1 in enumerate(positions):
        for antenna2 in positions[i + 1 :]:
            difference = Position(
                antenna2.x - antenna1.x, antenna2.y - antenna1.y
            )
            result.add(
                Position(antenna1.x - difference.x, antenna1.y - difference.y)
            )
            result.add(
                Position(antenna2.x + difference.x, antenna2.y + difference.y)
            )
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
    antinodes: set[Position] = set()
    for char, positions in antenna.items():
        antinodes.update(find_antinodes(positions))
    filtered = {
        anode
        for anode in antinodes
        if 0 <= anode.x < len(data[0]) and 0 <= anode.y < len(data)
    }
    print(len(filtered))


if __name__ == "__main__":
    main()
