from time import monotonic_ns
import logging
import sys
from dataclasses import dataclass
from collections import Counter
from copy import copy

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("lanternfish.log"),
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


def read_lanternfish(puzzle_file: str) -> list:
    with open(puzzle_file, "r") as f:
        puzzle_input = f.read().split(",")
        l_all = [int(i) for i in puzzle_input]
        logging.info("Loaded the ages of all lanternfish")
        return l_all

def count_lanternfish(puzzle_file: str) -> Counter:
    with open(puzzle_file, "r") as f:
        puzzle_input = f.read().split(",")
        l_all = [int(i) for i in puzzle_input]
        c = Counter(l_all)
        logging.info("Counted the ages of all lanternfish")
        return c

@dataclass
class Lanternfish:
    """
    A Lanternfish
    """
    age: int = 8

    def get_older(self):
        if self.age > 0:
            self.age -= 1
            return False
        else:
            self.age = 6
            return True

@dataclass
class LanternfishSwarm:
    '''
    Container for Lanternfish objects
    '''
    swarm: list[Lanternfish]

    def reproduce(self):
        self.swarm.append(Lanternfish())

    def pass_day(self):
        no_births = 0
        for fish in self.swarm:
            if fish.get_older():
                no_births += 1
        for i in range(no_births):
            self.reproduce()


@timer_func
def part_1() -> int:
    """
    :return:   Number of lanternfish after 80 days
    """
    logging.info("Calculating number of lanternfish after 80 days")
    l_all = read_lanternfish("puzzle_input.txt")

    # simulate a swarm of lanternfish via agent-based-modelling
    initial_lanternfish_swarm = []
    for i in l_all:
        initial_lanternfish_swarm.append(Lanternfish(i))

    all_fish = LanternfishSwarm(initial_lanternfish_swarm)

    for i in range(80):
        all_fish.pass_day()

    no_fish = len(all_fish.swarm)

    logging.info(f"Number of Lanternfish after 80 days is {no_fish}")

    return no_fish


@timer_func
def part_2() -> int:
    """
    :return:   Number of lanternfish after 256 days.
    No longer agent-based simulation, direct calculation of number of lanternfish
    """
    logging.info("Calculating number of lanternfish after 256 days")
    c_dict = dict(count_lanternfish("puzzle_input.txt"))

    # establishing a temporary dictionary
    next_dict = {}
    for i in range(9):
        try:
            next_dict[i] = c_dict[i]
        except KeyError:
            next_dict[i] = 0

    for i in range(256):
        for age in range(9):
            if age == 0:
                try:
                    next_dict[8] += c_dict[age]
                    next_dict[6] += c_dict[age]
                    next_dict[0] -= c_dict[age]
                except KeyError:
                    logging.error(f"no fish of age {age}")
            else:
                try:
                    next_dict[age] -= c_dict[age]
                    next_dict[age - 1] += c_dict[age]
                except KeyError:
                    logging.error(f"no fish of age {age}")
        c_dict = copy(next_dict)

    no_fish = sum(c_dict.values())

    logging.info(f"Number of Lanternfish after 256 days is {no_fish}")

    return no_fish


if __name__ == '__main__':
    print(f"Solution to part 1: {part_1()}")
    print(f"Solution to part 2: {part_2()}")
