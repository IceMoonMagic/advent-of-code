import enum
import sys
from collections.abc import Sequence


INFINITY = float("inf")
UNPASSABLE = float("-inf")
MAZE = list[list[int | float | None]]


class Position:

    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def __repr__(self):
        return f"({self.x = :>3}, {self.y = :>3})"

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
        return self.__class__(self.x + 1, self.y)

    def west(self) -> "Position":
        return self.__class__(self.x - 1, self.y)

    def at(self, data: Sequence[Sequence]):
        return data[self.y][self.x]


class Facing(enum.Enum):
    NORTH = Position.north
    SOUTH = Position.south
    EAST = Position.east
    WEST = Position.west

    @classmethod
    def rotate(cls, facing: "Facing") -> tuple["Facing", "Facing"]:
        if facing in {cls.NORTH, cls.SOUTH}:
            return cls.WEST, cls.EAST
        return cls.NORTH, cls.SOUTH


def dijkstra(maze: MAZE, pos: Position, facing: Facing, cost: int):
    if cost > pos.at(maze):
        return

    maze[pos.y][pos.x] = cost
    rotates = Facing.rotate(facing)
    dijkstra(maze, facing(pos), facing, cost + 1)
    dijkstra(maze, rotates[0](pos), rotates[0], cost + 1001)
    dijkstra(maze, rotates[1](pos), rotates[1], cost + 1001)


def find(target, maze: Sequence[Sequence]) -> Position:
    for y, line in enumerate(maze):
        for x, char in enumerate(line):
            if char == target:
                return Position(x, y)
    raise ValueError


def to_matrix(data: list[str]) -> MAZE:
    convert = {"#": UNPASSABLE, "S": INFINITY, "E": INFINITY, ".": INFINITY}
    result = []
    for line in data:
        result.append([])
        for char in line:
            result[-1].append(convert[char])
    return result


def print_matrix(matrix: MAZE):
    for line in matrix:
        for element in line:
            if element is None:
                element = "None"
            print(f"{element:>5}", end=", ")
        print()


def main():
    with open("input.test.txt") as file:
        data = file.read().splitlines()
    start = find("S", data)
    end = find("E", data)
    matrix = to_matrix(data)

    # print(sys.getrecursionlimit())
    sys.setrecursionlimit(len(matrix) * len(matrix[0]))
    # print(sys.getrecursionlimit())

    dijkstra(matrix, start, Facing.EAST, 0)
    print_matrix(matrix)
    print(end.at(matrix))


if __name__ == "__main__":
    main()
