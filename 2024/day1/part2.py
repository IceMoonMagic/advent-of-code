import bisect
from collections import Counter

left: Counter[int] = Counter()
right: Counter[int] = Counter()
with open("part1.input.txt") as file:
    for line in file:
        l, r = line.split("   ")
        left[int(l)] += 1
        right[int(r)] += 1

similarity = 0
for number, count in left.items():
    for _ in range(count):
        similarity += number * right[number]

print(similarity)
