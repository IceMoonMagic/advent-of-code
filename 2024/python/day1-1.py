import bisect

left: list[int] = []
right: list[int] = []
with open("../day1-1.input.txt") as file:
    for line in file:
        l, r = line.split("   ")
        l, r = int(l), int(r)
        bisect.insort_left(left, l)
        bisect.insort_left(right, r)

distance = 0
for l, r in zip(left, right):
    distance += abs(l - r)

print(distance)
