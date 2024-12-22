import sys
from collections.abc import Sequence

INFINITY = float("inf")
UNPASSABLE = float("-inf")
MAZE = list[list[int | float]]

WIDTH = HEIGHT = 70 + 1
NUM_BYTES = 12


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


def byte_fall(poses: Sequence[Position]) -> MAZE:
    result: MAZE = []
    for y in range(HEIGHT):
        result.append([])
        for x in range(WIDTH):
            result[-1].append(
                INFINITY if Position(x, y) not in poses else UNPASSABLE
            )
    return result


def dijkstra(maze: MAZE, pos: Position, cost: int):

    if not pos.is_valid_position(maze) or cost > pos.at(maze):
        return

    maze[pos.y][pos.x] = cost
    dijkstra(maze, pos.north(), cost + 1)
    dijkstra(maze, pos.south(), cost + 1)
    dijkstra(maze, pos.east(), cost + 1)
    dijkstra(maze, pos.west(), cost + 1)


def main():
    with open("input.txt") as file:
        data = file.read().splitlines()
    byte_poses = [
        Position(int(line.split(",")[0]), (int(line.split(",")[1])))
        for line in data
    ]

    grid = byte_fall(byte_poses[:NUM_BYTES])
    # for line in grid:
    #     print(line)

    sys.setrecursionlimit(HEIGHT * WIDTH)
    dijkstra(grid, Position(0, 0), 0)
    for line in grid:
        for char in line:
            print(f"{char:>6,}", end=" ")
        print()
    print(Position(WIDTH - 1, HEIGHT - 1).at(grid))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
