from collections.abc import Sequence


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
        return self.__class__(self.x - 1, self.y)

    def west(self) -> "Position":
        return self.__class__(self.x + 1, self.y)

    def at(self, data: Sequence[Sequence]):
        return data[self.y][self.x]


def set_char(grid: list[str], pos: Position, char: str):
    grid[pos.y] = (
        grid[pos.y][: pos.x] + char + grid[pos.y][pos.x + len(char) :]
    )


def perform_move(grid: list[str], bot: Position, move: str) -> Position:
    match move:
        case "^":
            movement = Position.north
        case "v":
            movement = Position.south
        case "<":
            movement = Position.east
        case ">":
            movement = Position.west
        case _:
            raise RuntimeError

    def find_space(curr_pos: Position) -> Position | None:
        if not curr_pos.is_valid_position(grid):
            return None
        match curr_pos.at(grid):
            case "#":
                return None
            case ".":
                return curr_pos
            case "O":
                return find_space(movement(curr_pos))

    move_to = find_space(movement(bot))
    if move_to is None:
        return bot

    moved_to = movement(bot)

    set_char(grid, bot, ".")
    set_char(grid, moved_to, "@")
    if moved_to != move_to:
        set_char(grid, move_to, "O")
    return moved_to


def locate_bot(grid: list[str]) -> Position:
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char == "@":
                return Position(x, y)


def print_grid(grid: list[str]):
    for line in grid:
        print(line)
    print()


def gps_sum(grid: list[str]) -> int:
    result = 0
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char != "O":
                continue
            result += y * 100 + x
    return result


def main():
    with open("input.txt") as file:
        _grid, _moves = file.read().split("\n\n")
    grid = _grid.split("\n")
    moves = list(_moves.replace("\n", ""))
    pos = locate_bot(grid)
    for move in moves:
        pos = perform_move(grid, pos, move)
    print_grid(grid)
    print(gps_sum(grid))


if __name__ == "__main__":
    main()
