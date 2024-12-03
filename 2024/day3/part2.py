import re


def main():
    regex = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|(don't\(\)|do\(\))")
    with open("part1.input.txt") as file:
        data = file.read()
    matches = regex.findall(data)
    total = 0
    enabled = True
    for match_ in matches:
        match match_[2]:
            case "do()":
                enabled = True
                continue
            case "don't()":
                enabled = False
                continue
            case "":
                if enabled:
                    total += int(match_[0]) * int(match_[1])
    print(total)


if __name__ == "__main__":
    main()
