class DependencyNode:
    def __init__(self, value: int):
        self.value = value
        self.dependencies = {}
        self.dependants = {}

    def __hash__(self):
        return hash(self.value)


found: dict[int, DependencyNode] = {}


def add_dependency(x: int, y: int):
    x_node = found.get(x, DependencyNode(x))
    y_node = found.get(y, DependencyNode(y))
    x_node.dependants[y] = y_node
    y_node.dependencies[x] = x_node
    found[x] = x_node
    found[y] = y_node


def is_in_order(values: list[int] | tuple[int, ...]) -> bool:
    encountered = []
    for value in values:
        v = found.get(value, DependencyNode(value))
        encountered.append(value)
        if any([d in encountered for d in v.dependants]):
            return False
    return True


def fix_update(update: list[int]):
    result = []
    for value in update:
        v = found.get(value, DependencyNode(value))
        failed_dependants = [d for d in v.dependants if d in result]
        first_index = len(result)
        for d in failed_dependants:
            first_index = min(first_index, result.index(d))
        result.insert(first_index, value)
    return result


def main():
    with open("part1.input.txt") as file:
        data = file.readlines()
    divider = data.index("\n")
    rules = data[:divider]
    updates = data[divider + 1 :]

    for rule in rules:
        add_dependency(*[int(value) for value in rule.split("|")])

    tally = 0
    for update in updates:
        update = [int(u) for u in update.split(",")]
        if not is_in_order(update):
            fixed = fix_update(update)
            tally += fixed[len(fixed) // 2]
    print(tally)


if __name__ == "__main__":
    main()
