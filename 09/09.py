# Not very good, I manually looked at the graph for several iterations until
# finding the right rectangle.

import fileinput
import matplotlib.pyplot as plt

def area(tile1: tuple[int, int], tile2: tuple[int, int]):
    return (abs(tile2[0] - tile1[0]) + 1) * (abs(tile2[1] - tile1[1]) + 1)

red_tiles = [tuple(map(int, line.split(","))) for line in fileinput.input()]
pairs = [(t1, t2) for i, t1 in enumerate(red_tiles) for t2 in red_tiles[i + 1:]]
pairs.sort(key=lambda x: area(*x), reverse=True)
p1 = area(*pairs[0])
print(f"p1 answer: {p1}")

outline_segs = list(zip(red_tiles, red_tiles[1:]))
outline_segs.append((red_tiles[-1], red_tiles[0]))

fig, ax = plt.subplots()
ax.invert_yaxis()
ax.plot(*zip(*red_tiles, red_tiles[0])),
plt.show(block=False)

def intersect(seg1: tuple[tuple[int, int], tuple[int, int]],
              seg2: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    """
    Always returns false for collinear.
    """

    # seg1 is AB, seg2 is CD
    A, B = sorted(seg1)
    C, D = sorted(seg2)

    dim1 = A[0] == B[0]
    dim2 = not dim1

    if (A[0] == B[0]) == (C[0] == D[0]):
        # Parallel
        return A[dim2] == C[dim2] and ((A[dim1] < C[dim1] and B[dim1] >= C[dim1]) or C[dim1] <= B[dim1] and D[dim1] > B[dim1])

    return A[dim1] < C[dim1] and C[dim1] < B[dim1] and C[dim2] < A[dim2] and A[dim2] < D[dim2]

def intersect2(seg1: tuple[tuple[int, int], tuple[int, int]],
              seg2: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    """
    Always returns false for collinear.
    """

    # seg1 is AB, seg2 is CD
    A, B = sorted(seg1)
    C, D = sorted(seg2)

    if (A[0] == B[0]) == (C[0] == D[0]):
        # Parallel
        return False

    dim1 = A[0] == B[0]
    dim2 = not dim1

    return A[dim1] <= C[dim1] and C[dim1] <= B[dim1] and C[dim2] <= A[dim2] and A[dim2] <= D[dim2]

def point_in_seg(point: tuple[int, int], seg: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    A, B = sorted(seg)
    dim = A[0] == B[0]
    return A[not dim] == point[not dim] and A[dim] <= point[dim] and point[dim] <= A[dim]

def on_outline(point: tuple[int, int]) -> bool:
    return any(point_in_seg(point, seg) for seg in outline_segs)

def within_outline(point: tuple[int, int]) -> bool:
    if on_outline(point):
        return True

    return any(intersect2(((0, point[1]), point), seg) for seg in outline_segs)

def intersects_outline(seg: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    return any(intersect(seg, outline_seg) for outline_seg in outline_segs)

for pair in pairs:
    A, C = pair
    B = (A[0], C[1])
    D = (C[0], A[1])

    if not any(intersects_outline(seg) for seg in [(A, B), (B, C), (C, D), (D, A)]):
        ax.plot(*zip(*pair), "ro")
        ax.plot(*zip(B, D), "go")
        fig.canvas.draw()
        fig.canvas.flush_events()
        p2 = area(*pair)
        print(f"p2 answer: {p2}")
        input("Press any key to continue...")
