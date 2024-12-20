from functools import cache


@cache
def find_solution(pattern: str, towels: tuple[str]) -> list[str] | None:
    if len(pattern) == 0:
        return []
    for towel in towels:
        if (
            pattern.startswith(towel)
            and (result := find_solution(pattern[len(towel) :], towels))
            is not None
        ):
            return [towel] + result
    return None


def main():
    with open("input.txt") as file:
        _towels, _designs = file.read().split("\n\n")
    towels = tuple(_towels.split(", "))
    designs = _designs.split("\n")[:-1]
    result = tuple(find_solution(design, towels) for design in designs)
    print(len(result) - result.count(None))


if __name__ == "__main__":
    main()
