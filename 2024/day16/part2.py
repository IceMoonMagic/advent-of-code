import enum
import sys
from collections.abc import Sequence
from queue import Queue

INFINITY = float("inf")
UNPASSABLE = float("-inf")
MAZE = list[list[int | float]]


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


def follow_paths(
    maze: MAZE,
    pos: Position,
    prev: tuple[tuple[int, Position] | None, tuple[int, Position] | None],
) -> set[Position | None]:
    here = pos.at(maze)
    if here == 0:
        return {pos}
    if (
        here == UNPASSABLE
        or (prev[0] is not None and prev[0][1] == pos)
        or (prev[1] is not None and prev[1][1] == pos)
        or (
            prev[0] is not None
            and prev[0][0] <= here
            and (prev[1] is None or prev[1][0] <= here)
        )
        or here == 75307  # ToDo: Actually Solve
    ):
        return {None}

    result = {pos}
    for direction in [pos.north(), pos.south(), pos.east(), pos.west()]:
        path = follow_paths(maze, direction, ((here, pos), prev[0]))
        if None not in path:
            result.update(path)
    return result if len(result) > 1 else {None}
    # return set(*follow_paths(maze, child) for child in children if child is not None).union({pos})


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
    with open("input.txt") as file:
        data = file.read().splitlines()
    start = find("S", data)
    end = find("E", data)
    matrix = to_matrix(data)

    # print(sys.getrecursionlimit())
    sys.setrecursionlimit(len(matrix) * len(matrix[0]))
    # print(sys.getrecursionlimit())

    dijkstra(matrix, start, Facing.EAST, 0)

    paths = follow_paths(matrix, end, (None, None))

    data = [list(line) for line in data]
    for pos in paths:
        data[pos.y][pos.x] = "O"

    for y, line in enumerate(matrix):
        for x, value in enumerate(line):
            if Position(x, y) in paths:
                print(f"{value:>6}", end=", ")
            else:
                print(" " * 6, end="  ")
        print()

    for line in data:
        for char in line:
            print(char, end=" ")
        print()
    print(len(paths))


if __name__ == "__main__":
    main()
