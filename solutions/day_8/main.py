from time import monotonic_ns
import logging
import sys
from itertools import chain

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("seven_segment.log"),
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


def read_input(puzzle_file: str) -> list:
    with open(puzzle_file, "r") as f:
        puzzle_input = f.read().splitlines()
        puzzle_input = [i.split("|") for i in puzzle_input]
        logging.info("Loaded the input")
        return puzzle_input

def identify_number_codes(number_codes: list[str]) -> list[set]:
    """
    :param number_codes: list of unidentified number codes for the seven-segment display
    :return: identified output code
    """

    # convert string input to sets in preparation for operations
    number_codes = [set(i) for i in number_codes]
    number_segments = [set()] * 10

    # deduce 1,4,7,8 through length
    for i in number_codes:
        if len(i) == 2:
            number_segments[1] = i
        elif len(i) == 3:
            number_segments[7] = i
        elif len(i) == 4:
            number_segments[4] = i
        elif len(i) == 7:
            number_segments[8] = i

    # separate segments from number combinations
    top = number_segments[7] - number_segments[1]
    right = number_segments[1]
    top_left_middle = number_segments[4] - number_segments[1]
    bottom_left_bottom = number_segments[8] - number_segments[4] - top

    # identify leftover segments via deduction
    x_len6 = [i for i in number_codes if len(i) == 6]
    for i in x_len6:
        t = i.intersection(number_segments[1])
        z = i - number_segments[4]
        if len(t) == 1:
            bottom_right = t
            number_segments[6] = i
            top_right = right - bottom_right
        elif len(z) == 2:
            bottom = z - top
            number_segments[9] = i
            bottom_left = bottom_left_bottom - bottom
        else:
            middle = number_segments[8] - i
            number_segments[0] = i
            top_left = top_left_middle - middle

    # set the rest of numbers
    number_segments[2] = number_segments[2].union(top, top_right, middle, bottom_left, bottom)
    number_segments[3] = number_segments[3].union(top, top_right, middle, bottom_right, bottom)
    number_segments[5] = number_segments[5].union(top, top_left, middle, bottom_right, bottom)

    return number_segments


def identify_output(number_segments: list[set], output: list[str]) -> int:
    io_set = [0]*4
    output_sets = [set(i) for i in output]
    for l, m in zip(output_sets, range(4)):
        for i, j in zip(number_segments, range(10)):
            if l == i:
                io_set[m] = j
    output_identified = int("".join([str(i) for i in io_set]))
    return output_identified

@timer_func
def part_1() -> int:
    """
    :return:   Number of 1,4,7,8 digits in the output
    """
    logging.info("Calculating the number of 1,4,7,8 digits in the output")
    output = list(chain(*[i[1].split(" ") for i in read_input("puzzle_input.txt")]))  # load and flatten output
    output = [i for i in output if i]  # get rid of empty strings
    no_digits = sum([1 for i in output if len(i) in [2, 3, 4, 7]])  # sum digits that are 1,4,7,8
    logging.info(f"The number of 1,4,7,8 digits in the output is {no_digits}")
    return no_digits


@timer_func
def part_2() -> int:
    """
    :return: sum of all output values
    """
    logging.info("Calculating the sum of all output values")
    # load, flatten and get rid of empty strings in puzzle input
    puzzle_input = read_input("puzzle_input.txt")
    output_all = [j for j in list(chain(*[i[1].split(" ") for i in puzzle_input])) if j]
    number_codes_all = [j for j in list(chain(*[i[0].split(" ") for i in puzzle_input])) if j]

    identified_outputs = []
    for i, j in zip(range(0,len(number_codes_all),10),range(0,len(output_all),4)):
        identified_outputs.append(identify_output(identify_number_codes(number_codes_all[i:i+10]), output_all[j:j+4]))

    sum_outputs = sum(identified_outputs)
    logging.info(f"The sum of all output values is {sum_outputs}")
    return sum_outputs


if __name__ == '__main__':
    print(f"Solution to part 1: {part_1()}")
    print(f"Solution to part 2: {part_2()}")
