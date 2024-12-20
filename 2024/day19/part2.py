from functools import cache


@cache
def find_solution(pattern: str, towels: tuple[str]) -> int | None:
    if len(pattern) == 0:
        return 1
    result = 0
    for towel in towels:
        if (
            pattern.startswith(towel)
            and (child_result := find_solution(pattern[len(towel) :], towels))
            is not None
        ):
            result += child_result
    if result == 0:
        return None
    return result


def main():
    with open("input.txt") as file:
        _towels, _designs = file.read().split("\n\n")
    towels = tuple(_towels.split(", "))
    designs = _designs.split("\n")[:-1]
    result = tuple(find_solution(design, towels) for design in designs)
    for i, r in enumerate(result):
        if r is not None:
            print(r, designs[i])
    print(sum(r for r in result if r is not None))


if __name__ == "__main__":
    main()
