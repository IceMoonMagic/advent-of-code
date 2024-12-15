from collections.abc import Sequence


class Position:

    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def __repr__(self):
        return f"({self.x = :>3}, {self.y = :>3}"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.x == other.x
            and self.y == other.y
        )

    def is_valid_position(self, data: Sequence[Sequence]) -> bool:
        return 0 <= self.y < len(data) and 0 <= self.x < len(data[self.y])

    def north(self) -> "Position":
        return self.__class__(self.x, self.y - 1)

    def south(self) -> "Position":
        return self.__class__(self.x, self.y + 1)

    def east(self) -> "Position":
        return self.__class__(self.x - 1, self.y)

    def west(self) -> "Position":
        return self.__class__(self.x + 1, self.y)

    def at(self, data: Sequence[Sequence]):
        return data[self.y][self.x]


def find_region(
    fields: list[str], pos: Position, crop: str, region: set[Position]
):
    if not pos.is_valid_position(fields) or pos.at(fields) != crop:
        return set()
    region.add(pos)
    for direction in [pos.north(), pos.south(), pos.east(), pos.west()]:
        if direction in region:
            continue
        find_region(fields, direction, crop, region)


def find_perimeter(region: set[Position]) -> int:
    result = 0
    for pos in region:
        for direction in [pos.north(), pos.south(), pos.east(), pos.west()]:
            result += direction not in region
    return result


def main():
    with open("input.txt") as file:
        data = file.read().splitlines()
    regions = []
    for y, line in enumerate(data):
        for x, _char in enumerate(line):
            pos = Position(x, y)
            if any((pos in region for region in regions)):
                continue
            regions.append(set())
            find_region(data, pos, data[y][x], regions[-1])

    print(sum((find_perimeter(region) * len(region) for region in regions)))


if __name__ == "__main__":
    main()
