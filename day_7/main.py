from time import monotonic_ns
import logging
import sys
from collections import Counter
from scipy.optimize import minimize_scalar

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("crabs.log"),
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


def count_crabs(puzzle_file: str) -> Counter:
    with open(puzzle_file, "r") as f:
        puzzle_input = f.read().split(",")
        l_all = [int(i) for i in puzzle_input]
        c = Counter(l_all)
        logging.info("Counted the positions of all crabs")
        return c

@timer_func
def part_1() -> int:
    """
    :return:   Least amount of fuel crabs need to get to the most efficient point
    """
    logging.info("Calculating the best position for the crabs")
    c_dict = dict(count_crabs("puzzle_input.txt"))

    # function to calculate distance of all crabs to point x
    def dist(x): return sum([abs(i - x) * j for i, j in c_dict.items()])

    min_fuel = round(minimize_scalar(dist).fun)

    return min_fuel


@timer_func
def part_2() -> int:
    """
    :return:   Least amount of fuel crabs need to get to the most efficient point
    """

    logging.info("Calculating the best position for the crabs")
    c_dict = dict(count_crabs("puzzle_input.txt"))

    # function to calculate fuel consumption of all crabs to point x
    def dist(x: int): return sum([(abs(i - x)+1)*abs(i - x)/2 * j for i, j in c_dict.items()])

    x = round(minimize_scalar(dist).x)
    min_fuel = dist(x)

    return min_fuel


if __name__ == '__main__':
    print(f"Solution to part 1: {part_1()}")
    print(f"Solution to part 2: {part_2()}")
