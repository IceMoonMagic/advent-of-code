from collections import defaultdict
from collections.abc import Sequence
from functools import cache


CHEAT_LENGTH = 20


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


Shortcut = tuple[Position, Position]
Track = tuple[tuple[int, ...], ...]


def trace_track(
    data: list[str],
) -> tuple[Track, list[Position]]:
    track: list[list[int]] = []
    start, end = Position(0, 0), Position(0, 0)
    for y, line in enumerate(data):
        track.append([])
        for x, char in enumerate(line):
            if char == "#":
                track[-1].append(-1)
            else:
                track[-1].append(0)
            if char == "S":
                start = Position(x, y)
            elif char == "E":
                end = Position(x, y)

    def _find_next(curr_pos: Position) -> Position:
        for _pos in [
            curr_pos.north(),
            curr_pos.south(),
            curr_pos.east(),
            curr_pos.west(),
        ]:
            if _pos.at(track) == 0 and _pos != start:
                return _pos

    pos = start
    time = 0
    path: list[Position] = [start]
    while pos != end:
        time += 1
        pos = _find_next(pos)
        track[pos.y][pos.x] = time
        path.append(pos)
    path.append(end)
    return tuple(tuple(line) for line in track), path


def find_shortcuts(pos: Position, track: Track) -> list[Shortcut]:
    return [
        (pos, end) for end in reachable_positions(pos, CHEAT_LENGTH - 1, track)
    ]


@cache
def _reachable_positions(
    pos: Position, spaces: int, track: Track
) -> set[Position]:
    result = set()
    if not pos.is_valid_position(track):
        return result
    if pos.at(track) != -1:
        result.add(pos)
    if spaces == 0:
        return result
    for move in [pos.north(), pos.south(), pos.east(), pos.west()]:
        if move.is_valid_position(track):
            result.update(_reachable_positions(move, spaces - 1, track))

    return result


def reachable_positions(
    start_pos: Position, start_spaces: int, track: Track
) -> set[Position]:

    reachable = (
        _reachable_positions(start_pos.north(), start_spaces, track)
        .union(_reachable_positions(start_pos.south(), start_spaces, track))
        .union(_reachable_positions(start_pos.east(), start_spaces, track))
        .union(_reachable_positions(start_pos.west(), start_spaces, track))
    )
    return reachable


@cache
def shortcut_saves(shortcut: Shortcut, track: Track) -> int:
    distance = abs(shortcut[1].y - shortcut[0].y) + abs(
        shortcut[1].x - shortcut[0].x
    )

    result = shortcut[1].at(track) - shortcut[0].at(track) - distance
    return result


def print_n_saves(shortcuts: list[Shortcut], track, min_: int = 1):
    ranked = defaultdict(list)
    for shortcut in shortcuts:
        ranked[shortcut_saves(shortcut, track)].append(shortcut)

    for saves, shortcuts_ in sorted(ranked.items()):
        if saves >= min_:
            print(f"{len(shortcuts_)} shortcut(s) save(s) {saves}")


def print_shortcuts(shortcuts: list[Shortcut]):
    for shortcut in shortcuts:
        print(f"{shortcut[0]} -> {shortcut[1]} | {shortcut[2]}")


def main():
    with open("input.txt") as file:
        data = file.read().splitlines()
    track, path = trace_track(data)
    shortcuts = []
    print()
    for i, tile in enumerate(path):
        print("\033[1A", end="")
        print(f"{i:,} / {len(path):,}")
        shortcuts += find_shortcuts(tile, track)

    # print(shortcuts)

    # print_n_saves(shortcuts, track)
    # print_shortcuts(shortcuts)

    print()
    tally = 0
    for i, shortcut in enumerate(shortcuts):
        print("\033[1A", end="")
        print(f"{i:,} / {len(shortcuts):,} | {tally:,}")
        if shortcut_saves(shortcut, track) >= 100:
            tally += 1
    print(tally)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
