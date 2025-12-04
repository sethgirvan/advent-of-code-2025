import fileinput

banks = [line.rstrip() for line in fileinput.input()]

def max_joltage(bank: str) -> int:
    first_joltage = max(bank[:-1])
    first_idx = bank[:-1].find(first_joltage)
    second_joltage = max(bank[first_idx + 1:])

    return int(first_joltage + second_joltage)

p1 = sum(max_joltage(bank) for bank in banks)
print(f"p1 answer: {p1}")

def p2_joltage(bank: str) -> int:
    joltage = 0
    for i in reversed(range(12)):
        next_joltage = max(bank[:len(bank) - i])
        _, _, bank = bank.partition(next_joltage)
        joltage = 10*joltage + int(next_joltage)
    return joltage

p2 = sum(p2_joltage(bank) for bank in banks)
print(f"p2 answer: {p2}")
