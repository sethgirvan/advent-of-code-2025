import fileinput
import functools

split = (line.split(":") for line in fileinput.input())
connections = {device: {output for output in outputs.split()} for device, outputs in split}

def paths_to_out(dev: str) -> int:
    if dev == "out":
        return 1

    return sum(paths_to_out(child) for child in connections[dev])

p1 = paths_to_out("you")
print(f"p1 answer: {p1}")

@functools.cache
def p2_paths_to_out(dev: str, dac: bool, fft: bool) -> int:
    if dev == "out":
        return int(dac and fft)

    if dev == "dac":
        dac = True
    if dev == "fft":
        fft = True

    return sum(p2_paths_to_out(child, dac, fft) for child in connections[dev])

p2 = p2_paths_to_out("svr", False, False)
print(f"p2 answer: {p2}")
