import collections
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


def find_sides(region: set[Position]) -> int:
    result = 0
    for pos in region:
        for direction in [pos.north(), pos.south(), pos.east(), pos.west()]:
            result += direction not in region
    return result


def get_pos_region(pos: Position, regions: list[set[Position]]) -> int:
    for i, region in enumerate(regions):
        if pos in region:
            return i
    raise ValueError


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

    sides: dict[int, int] = collections.Counter()
    for y in range(len(data) + 1):
        prev_top, prev_btm = None, None
        for x in range(len(data[0])):
            top = Position(x, y - 1)
            btm = Position(x, y)
            if (
                top.is_valid_position(data)
                and (top.at(data) != prev_top or top.at(data) == prev_btm)
                and (
                    not btm.is_valid_position(data)
                    or top.at(data) != btm.at(data)
                )
            ):
                sides[get_pos_region(top, regions)] += 1
            if (
                btm.is_valid_position(data)
                and (btm.at(data) != prev_btm or btm.at(data) == prev_top)
                and (
                    not top.is_valid_position(data)
                    or btm.at(data) != top.at(data)
                )
            ):
                sides[get_pos_region(btm, regions)] += 1
                if btm.at(data) == "C":
                    print(btm)
            if top.is_valid_position(data):
                prev_top = top.at(data)
            if btm.is_valid_position(data):
                prev_btm = btm.at(data)

    for x in range(len(data[0]) + 1):
        prev_left, prev_right = None, None
        for y in range(len(data)):
            left = Position(x - 1, y)
            right = Position(x, y)
            if (
                left.is_valid_position(data)
                and (left.at(data) != prev_left or left.at(data) == prev_right)
                and (
                    not right.is_valid_position(data)
                    or left.at(data) != right.at(data)
                )
            ):
                sides[get_pos_region(left, regions)] += 1
            if (
                right.is_valid_position(data)
                and (
                    right.at(data) != prev_right or right.at(data) == prev_left
                )
                and (
                    not left.is_valid_position(data)
                    or right.at(data) != left.at(data)
                )
            ):
                sides[get_pos_region(right, regions)] += 1
                if right.at(data) == "C":
                    print(right)
            if left.is_valid_position(data):
                prev_left = left.at(data)
            if right.is_valid_position(data):
                prev_right = right.at(data)

    print(sides)
    print(sum((sides[i] * len(region) for i, region in enumerate(regions))))


if __name__ == "__main__":
    main()
