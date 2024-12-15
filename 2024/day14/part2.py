import dataclasses
import re

WIDTH = 101
HEIGHT = 103

V_CENTER = WIDTH // 2
H_CENTER = HEIGHT // 2


@dataclasses.dataclass
class Bot:
    px: int
    py: int
    vx: int
    vy: int

    @classmethod
    def from_file(cls, line: str) -> "Bot":
        matches = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line)
        return cls(*(int(e) for e in matches.groups()))

    def move(self):
        self.px = (self.px + self.vx) % WIDTH
        self.py = (self.py + self.vy) % HEIGHT


def show_frame(bots: list[Bot], frame_num: int):
    frame = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]
    poses: set[tuple[int, int]] = set()
    for bot in bots:
        if (bot.px, bot.py) in poses:
            break
        poses.add((bot.px, bot.py))
        frame[bot.py][bot.px] = "#"
    else:
        print("Frame:", frame_num)
        for line in frame:
            print("".join(line))
        input("press enter")


def main():
    with open("input.txt") as file:
        data = file.read().splitlines()
    bots = [Bot.from_file(line) for line in data]
    counter = 1
    while True:
        for bot in bots:
            bot.move()
        show_frame(bots, counter)
        counter += 1


if __name__ == "__main__":
    main()
