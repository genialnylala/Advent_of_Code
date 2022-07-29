from time import monotonic_ns
import logging
import sys
from collections import Counter

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("vents.log"),
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


def read_vents(puzzle_file: str) -> list[tuple[list, list]]:
    with open(puzzle_file, "r") as f:
        puzzle_input = f.read().splitlines()
        v_all = [i.split("->") for i in puzzle_input]
        v_all = [(list(map(int, i.split(","))), list(map(int, j.split(",")))) for i, j in v_all]
        logging.info("Loaded all vent vectors")
        return v_all


@timer_func
def part_1() -> int:
    """
    :return:   Number of points where horizontal and vertical vents overlap
    """
    logging.info("Calculating vent overlaps for vertical and horizontal vents")
    v_all = read_vents("puzzle_input.txt")

    # separate horizontal and vertical vent vectors from rest
    v_vh = [i for i in v_all if (i[0][0] == i[1][0] or i[0][1] == i[1][1])]

    # generate all vent points
    points = []
    for vi in v_vh:
        if vi[0][0] == vi[1][0]:
            if vi[0][1] < vi[1][1]:
                for i in range(vi[0][1], vi[1][1] + 1):
                    points.append((vi[0][0], i))
            else:
                for i in range(vi[1][1], vi[0][1] + 1):
                    points.append((vi[0][0], i))
        elif vi[0][1] == vi[1][1]:
            if vi[0][0] < vi[1][0]:
                for i in range(vi[0][0], vi[1][0] + 1):
                    points.append((i, vi[0][1]))
            else:
                for i in range(vi[1][0], vi[0][0] + 1):
                    points.append((i, vi[0][1]))

    # finding overlap
    overlap = Counter(points)
    overlap = [i for i in overlap.items() if i[1] > 1]
    no_overlap = len(overlap)
    logging.info(f"Total number of overlaps is: {no_overlap}")

    return no_overlap

@timer_func
def part_2() -> int:
    """
    :return:   Number of overlaps for all vents
    """
    logging.info("Calculating vent overlaps for all vents (incl. diagonal)")
    v_all = read_vents("puzzle_input.txt")

    # generate all vent points
    points = []
    for vi in v_all:
        if vi[0][0] == vi[1][0]:
            if vi[0][1] < vi[1][1]:
                for i in range(vi[0][1], vi[1][1] + 1):
                    points.append((vi[0][0], i))
            else:
                for i in range(vi[1][1], vi[0][1] + 1):
                    points.append((vi[0][0], i))
        elif vi[0][1] == vi[1][1]:
            if vi[0][0] < vi[1][0]:
                for i in range(vi[0][0], vi[1][0] + 1):
                    points.append((i, vi[0][1]))
            else:
                for i in range(vi[1][0], vi[0][0] + 1):
                    points.append((i, vi[0][1]))
        elif vi[0][0] < vi[1][0] and vi[0][1] < vi[1][1]:
            for i, j in zip(range(vi[0][0], vi[1][0] + 1), range(vi[0][1], vi[1][1] + 1)):
                points.append((i, j))
        elif vi[0][0] > vi[1][0] and vi[0][1] < vi[1][1]:
            for i, j in zip(range(vi[0][0], vi[1][0] - 1, -1), range(vi[0][1], vi[1][1] + 1)):
                points.append((i, j))
        elif vi[0][0] < vi[1][0] and vi[0][1] > vi[1][1]:
            for i, j in zip(range(vi[0][0], vi[1][0] + 1), range(vi[0][1], vi[1][1] - 1, -1)):
                points.append((i, j))
        elif vi[0][0] > vi[1][0] and vi[0][1] > vi[1][1]:
            for i, j in zip(range(vi[0][0], vi[1][0] - 1, -1), range(vi[0][1], vi[1][1] - 1, -1)):
                points.append((i, j))
        else:
            print(f"somethings up,{vi}")
    

    # finding overlap
    overlap = Counter(points)
    overlap = [i for i in overlap.items() if i[1] > 1]
    no_overlap = len(overlap)
    logging.info(f"Total number of overlaps is: {no_overlap}")

    return no_overlap


if __name__ == '__main__':
    print(f"Solution to part 1: {part_1()}")
    print(f"Solution to part 2: {part_2()}")
