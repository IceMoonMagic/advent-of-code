import enum
from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])


class Facing(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


def preform_next_action(
    map_: list[str], pos: Position, facing: Facing
) -> tuple[Position | None, Facing]:
    match facing:
        case Facing.UP:
            next_pos = Position(pos.x, pos.y - 1)
            turn = Facing.RIGHT
        case Facing.DOWN:
            next_pos = Position(pos.x, pos.y + 1)
            turn = Facing.LEFT
        case Facing.LEFT:
            next_pos = Position(pos.x - 1, pos.y)
            turn = Facing.UP
        case Facing.RIGHT:
            next_pos = Position(pos.x + 1, pos.y)
            turn = Facing.DOWN
        case _:  # To make PyCharm happy
            next_pos = pos
            turn = facing

    if not 0 <= next_pos.x < len(map_[0]) or not 0 <= next_pos.y < len(map_):
        return None, facing
    elif map_[next_pos.y][next_pos.x] == "#":
        return pos, turn
    else:
        return next_pos, facing


def find_starting_pos(map_: list[str]) -> tuple[Position, Facing]:
    for y, line in enumerate(map_):
        if (x := line.find("^")) != -1:
            return Position(x, y), Facing.UP


def main():
    with open("part1.input.txt") as file:
        data = file.read().splitlines()
    pos, facing = find_starting_pos(data)
    visited: set[Position] = set()
    while pos is not None:
        visited.add(pos)
        pos, facing = preform_next_action(data, pos, facing)
    print(len(visited))


if __name__ == "__main__":
    main()
