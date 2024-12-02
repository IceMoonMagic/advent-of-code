def test_record(record: list[int]) -> bool:
    prev = record[0]
    ascending = record[0] < record[1]
    for level in record[1:]:
        difference = level - prev
        if not (1 <= abs(difference) <= 3 and ((difference > 0) == ascending)):
            return False
        prev = level
    else:
        return True


def test_skip(record: list[int]) -> bool:
    if test_record(record):
        return True

    for i in range(len(record)):
        if test_record(record[:i] + record[i + 1 :]):
            return True
    else:
        return False


def main():
    safe = 0
    with open("part1.input.txt") as file:
        for report in file.readlines():
            levels = [int(level) for level in report.split(" ")]
            safe += 1 if test_skip(levels) else 0

    print(safe)


if __name__ == "__main__":
    main()
