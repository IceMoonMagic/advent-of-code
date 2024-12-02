safe = 0
with open("part1.input.txt") as file:
    for report in file.readlines():
        levels = [int(level) for level in report.split(" ")]
        prev = levels[0]
        ascending = levels[0] < levels[1]
        for level in levels[1:]:
            difference = level - prev
            if not (
                1 <= abs(difference) <= 3 and ((difference > 0) == ascending)
            ):
                break
            prev = level
        else:
            safe += 1

print(safe)
