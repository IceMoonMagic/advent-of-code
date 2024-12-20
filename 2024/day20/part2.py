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


Shortcut = tuple[Position, Position, int]
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
    result = []
    ends = reachable_positions(pos, CHEAT_LENGTH - 1, track)
    for end, distance in ends.items():
        saves = shortcut_shorts((pos, end, distance), track)
        if saves > 0:
            result.append((pos, end, saves))
    return result


def min_dict(dict1: dict[Position, int], dict2: dict[Position, int]) -> dict:
    keys = set(dict1.keys()).union(dict2.keys())
    result: dict[Position, int] = {}
    for key in keys:
        if key in dict1 and key not in dict2:
            result[key] = dict1[key]
        elif key not in dict1:
            result[key] = dict2[key]
        elif dict1[key] > dict2[key]:
            result[key] = dict2[key]
        else:
            result[key] = dict1[key]
    return result


def increase_dict(dictionary: dict[Position, int]):
    for pos, distance in dictionary.items():
        dictionary[pos] = distance + 1


@cache
def reachable_positions(
    start_pos: Position, start_spaces: int, track: Track
) -> dict[Position, int]:
    @cache
    def _reachable_positions(pos, spaces) -> dict[Position, int]:
        if not pos.is_valid_position(track):
            return {}
        if pos.at(track) != -1:
            return {pos: 1}
        elif spaces == 0:
            return {}

        result = dict()
        for move in [pos.north(), pos.south(), pos.east(), pos.west()]:
            if move.is_valid_position(track):
                result = min_dict(
                    result, _reachable_positions(move, spaces - 1)
                )

        increase_dict(result)
        return result

    reachable = min_dict(
        min_dict(
            min_dict(
                _reachable_positions(start_pos.north(), start_spaces),
                _reachable_positions(start_pos.south(), start_spaces),
            ),
            _reachable_positions(start_pos.east(), start_spaces),
        ),
        _reachable_positions(start_pos.west(), start_spaces),
    )
    # for key in {
    #     start_pos,
    #     start_pos.north(),
    #     start_pos.south(),
    #     start_pos.east(),
    #     start_pos.west(),
    # }:
    #     if key in reachable:
    #         del reachable[key]
    return reachable


def shortcut_shorts(shortcut: Shortcut, track: Track) -> int:
    result = shortcut[1].at(track) - shortcut[0].at(track) - shortcut[2]
    return result


def print_n_saves(shortcuts: list[Shortcut], track):
    ranked = defaultdict(list)
    for shortcut in shortcuts:
        ranked[shortcut[2]].append(shortcut)

    for saves, shortcuts_ in sorted(ranked.items()):
        print(f"{len(shortcuts_)} shortcut(s) save(s) {saves}")


def main():
    with open("input.txt") as file:
        data = file.read().splitlines()
    track, path = trace_track(data)
    shortcuts = []
    for tile in path:
        shortcuts += find_shortcuts(tile, track)

    # print(shortcuts)

    print_n_saves(shortcuts, track)

    # tally = 0
    # for shortcut in shortcuts:
    #     if shortcut_shorts(shortcut, track) >= 100:
    #         tally += 1
    # print(tally)


if __name__ == "__main__":
    main()
