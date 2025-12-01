import fileinput

lines = (line.rstrip() for line in fileinput.input())
int_strs = (line.replace("R", "").replace("L", "-") for line in lines)
ints = [int(s) for s in int_strs]

dial_pos = 50
was_zero = False
p1_answer = 0
p2_answer = 0
for rot in ints:
    dial_pos += rot

    if dial_pos <= 0:
        p2_answer += abs((dial_pos - 1) // 100) - was_zero
    else:
        p2_answer += dial_pos // 100

    dial_pos %= 100
    if dial_pos == 0:
        p1_answer += 1

    was_zero = dial_pos == 0

print(f"p1 answer: {p1_answer}")
print(f"p2 answer: {p2_answer}")
