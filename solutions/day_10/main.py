from time import monotonic_ns
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("Syntax_Scoring.log"),
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
        puz_in_separate_characters = []
        for i in puzzle_input:
            puz_in_separate_characters.append([j for j in i])
        logging.info("Loaded the input")
        return puz_in_separate_characters


@timer_func
def identify_corrupted_characters(nav_subsystem: list[list[str]]) -> (list[str], list[int]):
    """
    :param nav_subsystem: output of the navigation subsystem as a matrix
     with each character being a single string element
    :return: list of illegal characters and list of the indexes of corrupted rows
    """
    illegal_characters = []
    corrupted_row_indexes = []
    for row, row_index in zip(nav_subsystem, range(len(nav_subsystem))):
        mutable_row = []
        for char, no in zip(row, range(len(row))):
            mutable_row.append(char)
            if char in "([{<":
                pass
            elif char == ")":
                if mutable_row[-2] == "(":
                    del mutable_row[-2:]
                else:
                    illegal_characters.append(char)
                    corrupted_row_indexes.append(row_index)
                    break
            elif char == "]":
                if mutable_row[-2] == "[":
                    del mutable_row[-2:]
                else:
                    illegal_characters.append(char)
                    corrupted_row_indexes.append(row_index)
                    break
            elif char == "}":
                if mutable_row[-2] == "{":
                    del mutable_row[-2:]
                else:
                    illegal_characters.append(char)
                    corrupted_row_indexes.append(row_index)
                    break
            elif char == ">":
                if mutable_row[-2] == "<":
                    del mutable_row[-2:]
                else:
                    illegal_characters.append(char)
                    corrupted_row_indexes.append(row_index)
                    break

    return illegal_characters, corrupted_row_indexes


@timer_func
def calculate_autocomplete_scores(incomplete_rows: list[list[str]]) -> list[int]:
    """
    :param incomplete_rows: matrix with incomplete rows
    :return: returns a list of scores for each row that is autocompleted
    """

    # get rid of closed brackets
    open_brackets = []
    for row, row_index in zip(incomplete_rows, range(len(incomplete_rows))):
        mutable_row = []
        for char, no in zip(row, range(len(row))):
            mutable_row.append(char)
            if char in "([{<":
                pass
            elif char == ")":
                if mutable_row[-2] == "(":
                    del mutable_row[-2:]
            elif char == "]":
                if mutable_row[-2] == "[":
                    del mutable_row[-2:]
            elif char == "}":
                if mutable_row[-2] == "{":
                    del mutable_row[-2:]
            elif char == ">":
                if mutable_row[-2] == "<":
                    del mutable_row[-2:]
        open_brackets.append(mutable_row)

    autocomplete_brackets = []
    for row in open_brackets:
        row.reverse()
        autocomplete_brackets_row = []
        for bracket in row:
            if bracket == "(":
                autocomplete_brackets_row.append(")")
            elif bracket == "[":
                autocomplete_brackets_row.append("]")
            elif bracket == "{":
                autocomplete_brackets_row.append("}")
            elif bracket == "<":
                autocomplete_brackets_row.append(">")
        autocomplete_brackets.append(autocomplete_brackets_row)

    # Calculate score for each row
    total_scores = []
    for row in autocomplete_brackets:
        total_score = 0
        for bracket in row:
            total_score *= 5
            if bracket == ")":
                total_score += 1
            elif bracket == "]":
                total_score += 2
            elif bracket == "}":
                total_score += 3
            else:
                total_score += 4
        total_scores.append(total_score)

    return total_scores


@timer_func
def part_1() -> int:
    """
    :return:   total syntax error score
    """
    nav_subsystem = read_input("puzzle_input.txt")
    logging.info("Calculating the total syntax error score")

    corrupted_characters = identify_corrupted_characters(nav_subsystem)[0]

    # Calculate score
    score = 0
    for i in corrupted_characters:
        if i == ")":
            score += 3
        elif i == "]":
            score += 57
        elif i == "}":
            score += 1197
        elif i == ">":
            score += 25137

    logging.info(f"The total syntax error score is {score}")
    return score


@timer_func
def part_2() -> int:
    """
    :return: the middle autocomplete score
    """
    nav_subsystem = read_input("puzzle_input.txt")
    logging.info("Calculating the middle autocomplete score")

    # create list without corrupted rows
    corrupted_rows = identify_corrupted_characters(nav_subsystem)[1]
    incomplete_rows = []
    for i, j in zip(nav_subsystem, range(len(nav_subsystem))):
        if j not in corrupted_rows:
            incomplete_rows.append(i)

    total_scores = calculate_autocomplete_scores(incomplete_rows)

    # find the middle score
    total_scores.sort()
    middle_score = total_scores[int(len(total_scores)/2)]
    logging.info(f"The middle score is {middle_score}")

    return middle_score


if __name__ == '__main__':
    print(f"Solution to part 1: {part_1()}")
    print(f"Solution to part 2: {part_2()}")
