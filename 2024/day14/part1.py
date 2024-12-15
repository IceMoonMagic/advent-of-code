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

    def get_quadrant(self) -> int | None:
        if self.px < V_CENTER and self.py < H_CENTER:
            return 0
        if self.px < V_CENTER and self.py > H_CENTER:
            return 1
        if self.px > V_CENTER and self.py < H_CENTER:
            return 2
        if self.px > V_CENTER and self.py > H_CENTER:
            return 3
        return None


def calc_safety_factor(bots: list[Bot]) -> int:
    quads = [0, 0, 0, 0]
    for bot in bots:
        quad = bot.get_quadrant()
        if quad is not None:
            quads[quad] += 1
    return quads[0] * quads[1] * quads[2] * quads[3]


def main():
    with open("input.txt") as file:
        data = file.read().splitlines()
    bots = [Bot.from_file(line) for line in data]
    for bot in bots:
        for _ in range(100):
            bot.move()
    print(calc_safety_factor(bots))


if __name__ == "__main__":
    main()
