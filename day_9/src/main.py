from time import monotonic_ns
import logging
import sys
import numpy as np
from numpy.typing import NDArray
from scipy.ndimage import minimum_filter
from skimage import measure

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("smoke_basin.log"),
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
        basin_list = []
        for i in puzzle_input:
            basin_list.append([int(j) for j in i])
        basin_list = np.array(basin_list)
        logging.info("Loaded the input")
        return basin_list


def check_for_max(data: NDArray, j: int, m: int) -> bool:
    """
    checks if a given local extreme is a maximum
    :param data: basin data
    :param j: row index
    :param m: column index
    :return: True, if point (j,m) is a local maximum
    """
    if j != 0 and m != 0 and j != len(data)-1 and m != len(data[0])-1:
        up = data[j - 1][m]
        down = data[j + 1][m]
        right = data[j][m + 1]
        left = data[j][m - 1]
        if data[j][m] >= up and data[j][m] >= down and data[j][m] >= left and data[j][m] >= right:
            return True
        else:
            return False
    # have to consider all edge cases
    elif j == 0 and m == 0:
        down = data[j + 1][m]
        right = data[j][m + 1]
        if data[j][m] >= down and data[j][m] >= right:
            return True
        else:
            return False
    elif j == 0 and m == len(data[0])-1:
        down = data[j + 1][m]
        left = data[j][m - 1]
        if data[j][m] >= down and data[j][m] >= left:
            return True
        else:
            return False
    elif j == len(data[0])-1 and m == 0:
        up = data[j - 1][m]
        right = data[j][m + 1]
        if data[j][m] >= up and data[j][m] >= right:
            return True
        else:
            return False
    elif j == len(data)-1 and m == len(data[0])-1:
        up = data[j - 1][m]
        left = data[j][m - 1]
        if data[j][m] >= up and data[j][m] >= left:
            return True
        else:
            return False
    elif j == len(data)-1 and m == len(data[0])-1:
        down = data[j + 1][m]
        right = data[j][m + 1]
        if data[j][m] >= down and data[j][m] >= right:
            return True
        else:
            return False
    elif j == 0:
        down = data[j + 1][m]
        right = data[j][m + 1]
        left = data[j][m - 1]
        if data[j][m] >= down and data[j][m] >= right and data[j][m] >= left:
            return True
        else:
            return False
    elif j == len(data)-1:
        up = data[j - 1][m]
        right = data[j][m + 1]
        left = data[j][m - 1]
        if data[j][m] >= up and data[j][m] >= right and data[j][m] >= left:
            return True
        else:
            return False
    elif m == 0:
        up = data[j - 1][m]
        right = data[j][m + 1]
        down = data[j - 1][m]
        if data[j][m] >= up and data[j][m] >= right and data[j][m] >= down:
            return True
        else:
            return False
    elif m == len(data[0])-1:
        up = data[j - 1][m]
        left = data[j][m - 1]
        down = data[j - 1][m]
        if data[j][m] >= up and data[j][m] >= left and data[j][m] >= down:
            return True
        else:
            return False


def find_minima(data: NDArray) -> NDArray:
    """
    Finds minima in a 2d array
    :param data: 2d array
    :return: 2d array, with True values signifying locations of minima
    """
    # apply minimum filter -> unchanged pixels are local extrema
    footprint = np.array([[0, 1, 0],
                          [1, 1, 1],
                          [0, 1, 0]])
    filtered_data = minimum_filter(data, footprint=footprint, mode='mirror')
    minima = (data == filtered_data)

    # check if unchanged pixels are maxima
    for row, j_index in zip(minima, range(len(minima))):
        for boolean_element, m_index in zip(row, range(len(row))):
            if boolean_element:
                if check_for_max(data, j_index, m_index):
                    minima[j_index][m_index] = False
    return minima


def calc_risk(minima: NDArray, data: NDArray) -> int:
    """
    :param minima: output of find_minima
    :param data: 2d array of basin
    :return: sum of the risk levels
    """
    risk_level = sum(sum(minima))
    only_minima_basin = data * minima
    for i in only_minima_basin:
        risk_level += sum(i)
    return risk_level


@timer_func
def part_1() -> int:
    """
    :return:   Sum of the risk levels of all low points
    """
    basin = read_input("puzzle_input.txt")

    logging.info("Calculating the local minima in basin")
    minima = find_minima(basin)
    logging.info("Calculating risk level")
    risk_level = calc_risk(minima, basin)
    logging.info(f"The risk level is {risk_level}")
    return risk_level


@timer_func
def part_2() -> int:
    """
    :return: sum of all the size of the 3 largest basins
    """
    basin = read_input("puzzle_input.txt")
    logging.info("Calculating the sum of all the size of the 3 largest basins")
    basin_boolean = []
    for i in basin:
        basin_boolean.append([0 if j == 9 else 1 for j in i])
    basin_boolean = np.array(basin_boolean)
    properties = measure.regionprops(measure.label(basin_boolean, background=0, connectivity=1))
    basin_sizes = []
    for prop in properties:
        basin_sizes.append(prop.area)
    basin_sizes.sort(reverse=True)
    answer = basin_sizes[0] * basin_sizes[1] * basin_sizes[2]

    return answer


if __name__ == '__main__':
    print(f"Solution to part 1: {part_1()}")
    print(f"Solution to part 2: {part_2()}")
