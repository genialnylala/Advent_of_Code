import numpy as np
from time import time


def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2 - t1):.10f}s')
        return result

    return wrap_func


@timer_func
def part_1() -> int:
    """
    :return:   product of coordinates
    """

    with open("puzzle_input.txt", "r") as f:
        puzzle_input = f.read().splitlines()

    pos = np.array([0, 0])

    for i in puzzle_input:
        if i[0] == "f":
            pos = pos + np.array([int(i[-1]), 0])
        elif i[0] == "d":
            pos = pos + np.array([0, int(i[-1])])
        elif i[0] == "u":
            pos = pos - np.array([0, int(i[-1])])
        else:
            print("unknown direction")

    return np.product(pos)


@timer_func
def part_2() -> int:
    """
    :return:   product of coordinates
    """

    with open("puzzle_input.txt", "r") as f:
        puzzle_input = f.read().splitlines()

    pos = np.array([0, 0])
    aim = 0

    for i in puzzle_input:
        if i[0] == "f":
            pos = pos + np.array([int(i[-1]), aim * int(i[-1])])
        elif i[0] == "d":
            aim += int(i[-1])
        elif i[0] == "u":
            aim -= int(i[-1])
        else:
            print("unknown direction")

    return np.product(pos)


if __name__ == '__main__':
    print(f"Solution to part 1: {part_1()}")
    print(f"Solution to part 2: {part_2()}")
