from time import monotonic_ns
import logging
import sys
import numpy as np
from numpy.typing import NDArray

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("Dumbo_Octopuses.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = monotonic_ns()
        result = func(*args, **kwargs)
        t2 = monotonic_ns()
        logging.info(f'Function {func.__name__!r} executed in {(t2 - t1):,d}ns')
        return result

    return wrap_func


def read_input(puzzle_file: str) -> NDArray:
    with open(puzzle_file, "r") as f:
        puzzle_input = f.read().splitlines()
        puz_in_separate_characters = []
        for i in puzzle_input:
            puz_in_separate_characters.append([int(j) for j in i])
        logging.info("Loaded the input")
        return np.array(puz_in_separate_characters)


@timer_func
def part_1() -> int:
    """
    :return:   total number of flashes after 100 steps
    """
    dumbo_octopuses = read_input("puzzle_input.txt")
    logging.info("Calculating the total number of flashes after 100 steps")
    number_of_flashes = 0

    # define subroutines
    def add_1():
        for row, row_index in zip(dumbo_octopuses, range(len(dumbo_octopuses))):
            for octopus, column_index in zip(row, range(len(row))):
                dumbo_octopuses[row_index][column_index] += 1

    def flash(number_of_flashes: int) -> (bool, int):
        flash_bool = False
        for row, row_index in zip(dumbo_octopuses, range(len(dumbo_octopuses))):
            for octopus, column_index in zip(row, range(len(row))):
                if octopus > 9:
                    # flash
                    dumbo_octopuses[row_index][column_index] = 0
                    number_of_flashes += 1
                    flash_bool = True

                    # flash spread and wall boundary conditions
                    if row_index not in (0, len(dumbo_octopuses) - 1) and column_index not in (0, len(row) - 1):
                        if dumbo_octopuses[row_index - 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index - 1][column_index] != 0:
                            dumbo_octopuses[row_index - 1][column_index] += 1
                        if dumbo_octopuses[row_index - 1][column_index + 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index + 1] += 1
                        if dumbo_octopuses[row_index][column_index - 1] != 0:
                            dumbo_octopuses[row_index][column_index - 1] += 1
                        if dumbo_octopuses[row_index][column_index + 1] != 0:
                            dumbo_octopuses[row_index][column_index + 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index + 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index] != 0:
                            dumbo_octopuses[row_index + 1][column_index] += 1
                        if dumbo_octopuses[row_index + 1][column_index + 1]:
                            dumbo_octopuses[row_index + 1][column_index + 1] += 1
                    elif row_index == 0 and column_index == 0:
                        if dumbo_octopuses[row_index][column_index + 1] != 0:
                            dumbo_octopuses[row_index][column_index + 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index] != 0:
                            dumbo_octopuses[row_index + 1][column_index] += 1
                        if dumbo_octopuses[row_index + 1][column_index + 1] != 0:
                            dumbo_octopuses[row_index + 1][column_index + 1] += 1
                    elif row_index == 0 and column_index == len(row) - 1:
                        if dumbo_octopuses[row_index][column_index - 1] != 0:
                            dumbo_octopuses[row_index][column_index - 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index + 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index] != 0:
                            dumbo_octopuses[row_index + 1][column_index] += 1
                    elif row_index == len(dumbo_octopuses) - 1 and column_index == 0:
                        if dumbo_octopuses[row_index - 1][column_index] != 0:
                            dumbo_octopuses[row_index - 1][column_index] += 1
                        if dumbo_octopuses[row_index - 1][column_index + 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index + 1] += 1
                        if dumbo_octopuses[row_index][column_index + 1] != 0:
                            dumbo_octopuses[row_index][column_index + 1] += 1
                    elif row_index == len(dumbo_octopuses)-1 and column_index == len(row)-1:
                        if dumbo_octopuses[row_index - 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index - 1][column_index] != 0:
                            dumbo_octopuses[row_index - 1][column_index] += 1
                        if dumbo_octopuses[row_index][column_index - 1] != 0:
                            dumbo_octopuses[row_index][column_index - 1] += 1
                    elif row_index == 0:
                        if dumbo_octopuses[row_index][column_index - 1] != 0:
                            dumbo_octopuses[row_index][column_index - 1] += 1
                        if dumbo_octopuses[row_index][column_index + 1] != 0:
                            dumbo_octopuses[row_index][column_index + 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index + 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index] != 0:
                            dumbo_octopuses[row_index + 1][column_index] += 1
                        if dumbo_octopuses[row_index + 1][column_index + 1] != 0:
                            dumbo_octopuses[row_index + 1][column_index + 1] += 1
                    elif row_index == len(dumbo_octopuses) - 1:
                        if dumbo_octopuses[row_index - 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index - 1][column_index] != 0:
                            dumbo_octopuses[row_index - 1][column_index] += 1
                        if dumbo_octopuses[row_index - 1][column_index + 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index + 1] += 1
                        if dumbo_octopuses[row_index][column_index - 1] != 0:
                            dumbo_octopuses[row_index][column_index - 1] += 1
                        if dumbo_octopuses[row_index][column_index + 1] != 0:
                            dumbo_octopuses[row_index][column_index + 1] += 1
                    elif column_index == len(row) - 1:
                        if dumbo_octopuses[row_index - 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index - 1][column_index] != 0:
                            dumbo_octopuses[row_index - 1][column_index] += 1
                        if dumbo_octopuses[row_index][column_index - 1] != 0:
                            dumbo_octopuses[row_index][column_index - 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index + 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index] != 0:
                            dumbo_octopuses[row_index + 1][column_index] += 1
                    else:
                        if dumbo_octopuses[row_index - 1][column_index] != 0:
                            dumbo_octopuses[row_index - 1][column_index] += 1
                        if dumbo_octopuses[row_index - 1][column_index + 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index + 1] += 1
                        if dumbo_octopuses[row_index][column_index + 1] != 0:
                            dumbo_octopuses[row_index][column_index + 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index] != 0:
                            dumbo_octopuses[row_index + 1][column_index] += 1
                        if dumbo_octopuses[row_index + 1][column_index + 1] != 0:
                            dumbo_octopuses[row_index + 1][column_index + 1] += 1
        return flash_bool, number_of_flashes

    no_steps = 100
    for i in range(no_steps):
        while_bool = True
        add_1()
        while while_bool:
            x = flash(number_of_flashes)
            number_of_flashes = x[1]
            while_bool = x[0]

    logging.info(f"The total number of flashes after 100 steps is {number_of_flashes}")
    return number_of_flashes


@timer_func
def part_2() -> int:
    """
    :return: The number of steps until full synchronization
    """
    dumbo_octopuses = read_input("puzzle_input.txt")
    logging.info("Calculating the number of steps until full synchronization")
    number_of_flashes = 0

    # define subroutines
    def add_1():
        for row, row_index in zip(dumbo_octopuses, range(len(dumbo_octopuses))):
            for octopus, column_index in zip(row, range(len(row))):
                dumbo_octopuses[row_index][column_index] += 1

    def flash(number_of_flashes: int) -> (bool, int):
        flash_bool = False
        for row, row_index in zip(dumbo_octopuses, range(len(dumbo_octopuses))):
            for octopus, column_index in zip(row, range(len(row))):
                if octopus > 9:
                    # flash
                    dumbo_octopuses[row_index][column_index] = 0
                    number_of_flashes += 1
                    flash_bool = True

                    # flash spread and wall boundary conditions
                    if row_index not in (0, len(dumbo_octopuses) - 1) and column_index not in (0, len(row) - 1):
                        if dumbo_octopuses[row_index - 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index - 1][column_index] != 0:
                            dumbo_octopuses[row_index - 1][column_index] += 1
                        if dumbo_octopuses[row_index - 1][column_index + 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index + 1] += 1
                        if dumbo_octopuses[row_index][column_index - 1] != 0:
                            dumbo_octopuses[row_index][column_index - 1] += 1
                        if dumbo_octopuses[row_index][column_index + 1] != 0:
                            dumbo_octopuses[row_index][column_index + 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index + 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index] != 0:
                            dumbo_octopuses[row_index + 1][column_index] += 1
                        if dumbo_octopuses[row_index + 1][column_index + 1]:
                            dumbo_octopuses[row_index + 1][column_index + 1] += 1
                    elif row_index == 0 and column_index == 0:
                        if dumbo_octopuses[row_index][column_index + 1] != 0:
                            dumbo_octopuses[row_index][column_index + 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index] != 0:
                            dumbo_octopuses[row_index + 1][column_index] += 1
                        if dumbo_octopuses[row_index + 1][column_index + 1] != 0:
                            dumbo_octopuses[row_index + 1][column_index + 1] += 1
                    elif row_index == 0 and column_index == len(row) - 1:
                        if dumbo_octopuses[row_index][column_index - 1] != 0:
                            dumbo_octopuses[row_index][column_index - 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index + 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index] != 0:
                            dumbo_octopuses[row_index + 1][column_index] += 1
                    elif row_index == len(dumbo_octopuses) - 1 and column_index == 0:
                        if dumbo_octopuses[row_index - 1][column_index] != 0:
                            dumbo_octopuses[row_index - 1][column_index] += 1
                        if dumbo_octopuses[row_index - 1][column_index + 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index + 1] += 1
                        if dumbo_octopuses[row_index][column_index + 1] != 0:
                            dumbo_octopuses[row_index][column_index + 1] += 1
                    elif row_index == len(dumbo_octopuses) - 1 and column_index == len(row) - 1:
                        if dumbo_octopuses[row_index - 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index - 1][column_index] != 0:
                            dumbo_octopuses[row_index - 1][column_index] += 1
                        if dumbo_octopuses[row_index][column_index - 1] != 0:
                            dumbo_octopuses[row_index][column_index - 1] += 1
                    elif row_index == 0:
                        if dumbo_octopuses[row_index][column_index - 1] != 0:
                            dumbo_octopuses[row_index][column_index - 1] += 1
                        if dumbo_octopuses[row_index][column_index + 1] != 0:
                            dumbo_octopuses[row_index][column_index + 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index + 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index] != 0:
                            dumbo_octopuses[row_index + 1][column_index] += 1
                        if dumbo_octopuses[row_index + 1][column_index + 1] != 0:
                            dumbo_octopuses[row_index + 1][column_index + 1] += 1
                    elif row_index == len(dumbo_octopuses) - 1:
                        if dumbo_octopuses[row_index - 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index - 1][column_index] != 0:
                            dumbo_octopuses[row_index - 1][column_index] += 1
                        if dumbo_octopuses[row_index - 1][column_index + 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index + 1] += 1
                        if dumbo_octopuses[row_index][column_index - 1] != 0:
                            dumbo_octopuses[row_index][column_index - 1] += 1
                        if dumbo_octopuses[row_index][column_index + 1] != 0:
                            dumbo_octopuses[row_index][column_index + 1] += 1
                    elif column_index == len(row) - 1:
                        if dumbo_octopuses[row_index - 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index - 1][column_index] != 0:
                            dumbo_octopuses[row_index - 1][column_index] += 1
                        if dumbo_octopuses[row_index][column_index - 1] != 0:
                            dumbo_octopuses[row_index][column_index - 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index - 1] != 0:
                            dumbo_octopuses[row_index + 1][column_index - 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index] != 0:
                            dumbo_octopuses[row_index + 1][column_index] += 1
                    else:
                        if dumbo_octopuses[row_index - 1][column_index] != 0:
                            dumbo_octopuses[row_index - 1][column_index] += 1
                        if dumbo_octopuses[row_index - 1][column_index + 1] != 0:
                            dumbo_octopuses[row_index - 1][column_index + 1] += 1
                        if dumbo_octopuses[row_index][column_index + 1] != 0:
                            dumbo_octopuses[row_index][column_index + 1] += 1
                        if dumbo_octopuses[row_index + 1][column_index] != 0:
                            dumbo_octopuses[row_index + 1][column_index] += 1
                        if dumbo_octopuses[row_index + 1][column_index + 1] != 0:
                            dumbo_octopuses[row_index + 1][column_index + 1] += 1
        return flash_bool, number_of_flashes

    no_steps = 0
    while True:
        no_steps += 1
        while_bool = True
        add_1()
        while while_bool:
            x = flash(number_of_flashes)
            number_of_flashes = x[1]
            while_bool = x[0]
        if np.array_equal(dumbo_octopuses, np.zeros((10, 10))):
            break

    logging.info(f"The number of steps until full synchronization is {no_steps}")
    return no_steps


if __name__ == '__main__':
    print(f"Solution to part 1: {part_1()}")
    print(f"Solution to part 2: {part_2()}")
