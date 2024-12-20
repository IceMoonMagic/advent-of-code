from collections import defaultdict
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


Shortcut = tuple[Position, Position]
Track = list[list[int]]


def trace_track(
    data: list[str],
) -> tuple[Track, list[Position]]:
    track: Track = []
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
    return track, path


def find_shortcuts(pos: Position, track: Track) -> list[Shortcut]:
    result = []
    here = pos.at(track)
    for moved in [
        pos.north().north(),
        pos.south().south(),
        pos.east().east(),
        pos.west().west(),
    ]:
        if moved.is_valid_position(track) and moved.at(track) > here + 2:
            result.append((pos, moved))
    return result


def shortcut_shorts(shortcut: Shortcut, track: Track) -> int:
    return shortcut[1].at(track) - shortcut[0].at(track) - 2


def print_n_saves(shortcuts: list[Shortcut], track):
    ranked = defaultdict(list)
    for shortcut in shortcuts:
        ranked[shortcut_shorts(shortcut, track)].append(shortcut)

    for saves, shortcuts_ in sorted(ranked.items()):
        print(f"{len(shortcuts_)} shortcut(s) save(s) {saves}")


def main():
    with open("input.txt") as file:
        data = file.read().splitlines()
    track, path = trace_track(data)
    shortcuts = []
    for tile in path:
        shortcuts += find_shortcuts(tile, track)

    # print_n_saves(shortcuts, track)

    tally = 0
    for shortcut in shortcuts:
        if shortcut_shorts(shortcut, track) >= 100:
            tally += 1
    print(tally)


if __name__ == "__main__":
    main()
