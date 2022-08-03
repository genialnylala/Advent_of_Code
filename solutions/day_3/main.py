import numpy as np
from time import time
from itertools import chain


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
    :return:   product of gamma and epsilon rates
    """

    with open("puzzle_input.txt", "r") as f:
        puzzle_input = np.fromiter(chain(*f.read().splitlines()), int)

    length = len(puzzle_input)/12
    x = [sum(puzzle_input[i::12])/length for i in range(12)]

    gamma_rate = [1 if i < 0.5 else 0 for i in x]
    gamma_rate = int(''.join([str(i) for i in gamma_rate]), 2)  # converting from binary to decimal

    epsilon_rate = [1 if i > 0.5 else 0 for i in x]
    epsilon_rate = int(''.join([str(i) for i in epsilon_rate]), 2)  # converting from binary to decimal

    return epsilon_rate * gamma_rate

@timer_func
def part_2() -> int:
    """
    :return:   product of oxygen and CO2 rating
    """

    with open("puzzle_input.txt", "r") as f:
        puzzle_input_str = f.read().splitlines()

    filtered = puzzle_input_str

    # Oxygen
    for i in range(12):
        x_len = len(filtered)
        if x_len == 1:
            break
        filtered_int = np.fromiter(chain(*filtered), int)
        x = sum(filtered_int[i::12])/x_len
        if x >= 0.5:
            filtered = list(filter(lambda y: int(y[i]) == 1, filtered))
        else:
            filtered = list(filter(lambda y: int(y[i]) == 0, filtered))

    oxy = int(filtered[0], 2)

    # CO2
    filtered = puzzle_input_str
    for i in range(12):
        x_len = len(filtered)
        if x_len == 1:
            break
        filtered_int = np.fromiter(chain(*filtered), int)
        x = sum(filtered_int[i::12])/x_len
        if x >= 0.5:
            filtered = list(filter(lambda y: int(y[i]) == 0, filtered))
        else:
            filtered = list(filter(lambda y: int(y[i]) == 1, filtered))

    co2 = int(filtered[0], 2)

    return oxy * co2


if __name__ == '__main__':
    print(f"Solution to part 1: {part_1()}")
    print(f"Solution to part 2: {part_2()}")
