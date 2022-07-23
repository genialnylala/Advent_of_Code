import numpy as np
from time import time


def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2 - t1):.4f}s')
        return result

    return wrap_func


@timer_func
def part_1() -> int:
    """
    :return: total number of increases
    """

    # PART 1
    with open("puzzle_input.txt", "r") as f:
        puzzle_input = [int(i) for i in f.read().splitlines()]

    # calculating the number of increases as difference between two vectors
    v_1 = np.array(puzzle_input)
    v_2 = v_1[1:]
    v_2 = np.append(v_2, 0)
    v_diff = v_2-v_1
    number_of_increase = [1 if i > 0 else 0 for i in v_diff]
    return sum(number_of_increase)

def part_2() -> int:
    """
    :return: total number of increases over the running sum
    """

    with open("puzzle_input.txt", "r") as f:
        puzzle_input = [int(i) for i in f.read().splitlines()]

    # a running sum can be calculated using convolution
    v_1 = np.array(puzzle_input)
    v_1_rs = np.convolve(v_1, np.ones(3), mode='valid')
    v_2_rs = v_1_rs[1:]
    v_2_rs = np.append(v_2_rs, 0)
    vrs_diff = v_2_rs - v_1_rs
    number_of_increase_rs = [1 if i > 0 else 0 for i in vrs_diff]

    return sum(number_of_increase_rs)


if __name__ == '__main__':
    print(f"PART 1: The total number of increases is: {part_1()}.")
    print(f"PART 2: The total number of running sum increases is: {part_2()}")
