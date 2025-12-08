# Code not very good. Would have been simpler and more efficient to just
# calculate the distance between every single possible pair, since there are
# only 1000 points that is only 499500 pairs.
#
# I basically implemented the "Linear-time randomized algorithm" described here
# https://en.wikipedia.org/wiki/Closest_pair_of_points_problem#Linear-time_randomized_algorithms
# In fact it is way slower that the brute-force approach of calculating the
# distance between every possible pair and sorting.

from collections import defaultdict
from scipy.cluster.hierarchy import DisjointSet
import fileinput
import math
import random

class Pair:
    """
    Makes sure order is ignored when comparing pairs of points.
    """

    p1: tuple[int, int, int]
    p2: tuple[int, int, int]

    def __init__(self, p1: tuple[int, int, int], p2: tuple[int, int, int]):
        if p1 < p2:
            self.p1 = p1
            self.p2 = p2
        elif p1 == p2:
            raise Exception("Points should be different")
        else:
            self.p1 = p2
            self.p2 = p1

    def distance(self):
        res = 0
        for p1i, p2i in zip(self.p1, self.p2):
            res += (p1i - p2i)**2
        return math.sqrt(res)

    def to_tuple(self):
        return (self.p1, self.p2)

    def __eq__(self, other) -> bool:
        if isinstance(other, Pair):
            return self.to_tuple() == other.to_tuple()
        else:
            return NotImplemented

    def __hash__(self) -> int:
        return hash(self.to_tuple())


points: list[tuple[int, int, int]] = [tuple(map(int, line.rstrip().split(","))) for line in fileinput.input()]
circuits = DisjointSet(points)
connected_pairs: set[Pair] = set()

rand_pairs = (random.sample(points, 2) for _ in range(len(points)))
# Multiply by four as hack to avoid issue described in comment below above
# 'if closest_pair is None'.
d = 4 * int(math.ceil(min(Pair(p1, p2).distance() for p1, p2 in rand_pairs)))

def gen_grid(d: int) -> defaultdict[tuple[int, int, int], set[tuple[int, int, int]]]:
    grid: defaultdict[tuple[int, int, int], set[tuple[int, int, int]]] = defaultdict(set)
    grid_pos_to_points: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = [(tuple(x // d for x in point), point) for point in points]
    for grid_pos, point in grid_pos_to_points:
        grid[grid_pos].add(point)
    return grid

grid = gen_grid(d)

connection_count = 0
while len(circuits.subsets()) > 1:
    print(f"\r{connection_count}", end="")
    closest_dist = math.inf
    closest_pair: Pair|None = None
    while True:
        for g_pos, g_points in grid.items():
            x, y, z = g_pos
            for g_point in g_points:
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
                        for k in range(z - 1, z + 2):
                            g_other = (i, j, k)
                            if g_other in grid:
                                for other_point in grid[g_other]:
                                    if other_point != g_point:
                                        pair = Pair(g_point, other_point)
                                        dist = pair.distance()
                                        if dist < closest_dist and pair not in connected_pairs:
                                            closest_dist = dist
                                            closest_pair = pair
        # This is not actually a guaranteed to be accurate method if d is not
        # large enough, since we could have found a closest_pair, but missed out
        # on the real closest pair because d was not large enough.
        if closest_pair is None:
            d *= 2
            print(f"\nIncreasing grid square size to {d}")
            grid = gen_grid(d)
        else:
            break

    connected_pairs.add(closest_pair)
    circuits.merge(*closest_pair.to_tuple())
    connection_count += 1
    if connection_count == 1000:
        p1 = math.prod(sorted(map(len, circuits.subsets()))[-3:])
        print(f"\np1 answer: {p1}")

p2 = closest_pair.p1[0] * closest_pair.p2[0]
print(f"\np2 answer: {p2}")
