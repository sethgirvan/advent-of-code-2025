# I tried to be fancy and do part 1 using math instead of brute-forcing, but
# then for part 2 ended up brute-forcing anyway (not sure whether there is some
# way to avoid it for part 2).

import fileinput
import functools
import math

def count_digits(x: int) -> int:
    return int(math.log10(x)) + 1

def split_num(x: int) -> tuple[int, int]:
    digits = count_digits(x)
    if digits % 2:
        raise Exception("split_num: must be even number of digits")

    half_order = 10**(digits // 2)
    return (x // half_order, x % half_order)

def sum_invalid_same_width(start: int, end: int) -> int:
    """
    start and end must be the same number of digits
    """

    starth, startl = split_num(start)
    if starth < startl:
        starth += 1
    endh, endl = split_num(end)
    if endh > endl:
        endh -= 1

    half_digits = count_digits(starth)

    # Every single first half of an id between starth and endh (inclusive)
    # should now correspond with a repeated number.
    res = ((endh*(endh + 1) + starth*(1 - starth)) // 2) * (10**half_digits + 1)
    return res

def sum_invalid_ids(start: int, end: int) -> int:
    start_digits = int(math.log10(start)) + 1
    end_digits = int(math.log10(end)) + 1

    if start_digits % 2:
        start = 10**start_digits
        start_digits += 1
        if start > end:
            return 0

    if end_digits % 2:
        end = 10**(end_digits - 1) - 1
        if start > end:
            return 0

    total = 0
    while start_digits < end_digits:
        total += sum_invalid_same_width(start, 10**start_digits - 1)
        start_digits += 2
        start = 10**(start_digits - 1)

    total += sum_invalid_same_width(start, end)
    return total

ranges = [tuple(map(int, r.split("-"))) for r in next(fileinput.input()).rstrip().split(",")]

p1_answer = sum(sum_invalid_ids(*range) for range in ranges)
print(f"p1_answer: {p1_answer}")

@functools.cache
def evenly_spaced_ones(digits: int, group_size: int) -> int:
    num_ones = digits // group_size
    res = 1
    for _ in range(0, num_ones - 1):
        res *= 10**group_size
        res += 1
    return res

def p2_is_invalid(x: int) -> bool:
    # Would be slightly more efficient to only divide digits into groupings
    # where the number of groupings correspond to the prime factors only of the
    # number of digits.
    digits = count_digits(x)
    for i in range(1, digits // 2 + 1):
        if digits % i == 0:
            part = x % 10**i
            if x == part * evenly_spaced_ones(digits, i):
                return True
    return False

def p2_sum_invalid_ids(start: int, end: int) -> int:
    return sum(x for x in range(start, end + 1) if p2_is_invalid(x))

p2_answer = sum(p2_sum_invalid_ids(*range) for range in ranges)
print(f"p2_answer: {p2_answer}")
