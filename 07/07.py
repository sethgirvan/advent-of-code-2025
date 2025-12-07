from collections import Counter
import fileinput
import re

p1 = 0

with fileinput.input() as f:
    lines = iter(f)
    first_line = next(lines)
    start_idx = first_line.find("S")
    beams: Counter[int] = Counter({start_idx: 1})

    for line in lines:
        nextbeams: Counter[int] = Counter()
        splitters = re.finditer(r"\^", line)
        for splitter in splitters:
            idx = splitter.start()
            if idx in beams:
                p1 += 1
                timelines = beams[idx]
                del beams[idx]

                left = idx - 1
                if left >= 0:
                    nextbeams[left] += timelines
                right = idx + 1
                if right < len(line):
                    nextbeams[right] += timelines

        beams += nextbeams
        print(beams)

print(f"p1 answer: {p1}")

p2 = beams.total()
print(f"p2 answer: {p2}")
