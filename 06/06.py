import fileinput
import math

op_tbl = {"+": sum, "*": math.prod}

lines = [line.split() for line in fileinput.input()]
nums = [map(int, line) for line in lines[:-1]]
nums_T = zip(*nums)
ops = lines[-1]

p1 = sum(op_tbl[op](prob) for prob, op in zip(nums_T, ops))
print(f"p1 answer: {p1}")

# p2
lines = [line for line in fileinput.input()][:-1]
lines_T = ["".join(l) for l in zip(*lines)]
p2 = 0
iter = iter(lines_T)
i = 0
for line_T in iter:
    prob = []
    while line_T.strip() != "":
        prob.append(int(line_T))
        line_T = next(iter, None)
        if line_T is None:
            break
    p2 += op_tbl[ops[i]](prob)
    i += 1

print(f"p2 answer: {p2}")
