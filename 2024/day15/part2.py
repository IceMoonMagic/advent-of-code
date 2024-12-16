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
        return self.__class__(self.x + 1, self.y)

    def west(self) -> "Position":
        return self.__class__(self.x - 1, self.y)

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
            movement = Position.west
        case ">":
            movement = Position.east
        case _:
            raise RuntimeError

    def push(
        curr_pos: Position, dry_run: bool, from_connected_box=False
    ) -> bool:
        if (curr_space := curr_pos.at(grid)) == "#":
            return False
        elif curr_space == ".":
            return True
        next_move = movement(curr_pos)
        if not push(next_move, dry_run):
            return False

        if not dry_run:
            set_char(grid, curr_pos, ".")
        if curr_space == "@":
            if not dry_run:
                set_char(grid, movement(curr_pos), "@")
            return True
        if curr_space in "[]":
            if movement in {Position.east, Position.west}:
                if not dry_run:
                    set_char(grid, movement(curr_pos), curr_space)
                return True
            else:
                if not (
                    from_connected_box
                    or (
                        curr_space == "["
                        and push(curr_pos.east(), dry_run, True)
                    )
                    or (
                        curr_space == "]"
                        and push(curr_pos.west(), dry_run, True)
                    )
                ):
                    return False
                if not dry_run:
                    set_char(grid, movement(curr_pos), curr_space)
                return True

    if push(bot, True):
        push(bot, False)
        return movement(bot)
    return bot


def locate_bot(grid: list[str]) -> Position:
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char == "@":
                return Position(x, y)


def widen_grid(grid: list[str]):
    replacement_chars = {"#": "##", "O": "[]", ".": "..", "@": "@."}
    for y, line in enumerate(grid.copy()):
        for x, char in enumerate(line):
            set_char(grid, Position(x * 2, y), replacement_chars[char])


def print_grid(grid: list[str]):
    for line in grid:
        print(line)
    print()


def gps_sum(grid: list[str]) -> int:
    result = 0
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char != "[":
                continue
            result += y * 100 + x
    return result


def main():
    with open("input.txt") as file:
        _grid, _moves = file.read().split("\n\n")
    grid = _grid.split("\n")
    widen_grid(grid)
    # print_grid(grid)
    moves = list(_moves.replace("\n", ""))
    pos = locate_bot(grid)
    for move in moves:
        pos = perform_move(grid, pos, move)
    # print_grid(grid)
    print(gps_sum(grid))


if __name__ == "__main__":
    main()
