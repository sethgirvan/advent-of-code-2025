# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "intervaltree",
# ]
# ///

from intervaltree import Interval, IntervalTree
import fileinput

fresh_ingreds = IntervalTree()

with fileinput.input() as f:
    lines = iter(f)
    for line in lines:
        if not line.rstrip():
            break

        start, end = map(int, line.split("-"))
        fresh_ingreds.add(Interval(start, end + 1))

    fresh_ingreds.merge_overlaps()
    avail_ingreds = [int(line) for line in lines]

p1 = sum(len(fresh_ingreds[ingred]) > 0 for ingred in avail_ingreds)
print(f"p1 answer: {p1}")

p2 = sum(intvl.length() for intvl in fresh_ingreds)
print(f"p2 answer: {p2}")
