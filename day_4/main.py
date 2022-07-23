from time import time
import logging
import numpy as np

logging.basicConfig(filename='bingo.log', filemode='w', level=logging.DEBUG)


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
    :return:   Final score of the winning board
    """

    with open("puzzle_input.txt", "r") as f:
        puzzle_input = f.read().splitlines()

    # reading generated numbers
    numbers_drawn = list(map(int, puzzle_input[0].split(',')))

    # reading bingo cards
    bingo_cards_all = []
    for i in range(2, len(puzzle_input)+1, 6):
        bingo_card = []
        for row in puzzle_input[i:i+5]:
            row = list(filter(None, row.split(' ')))  # delete empty strings
            bingo_card.append(list(row))
        bingo_cards_all.append(np.asarray(bingo_card, int))

    bingo_card_success_index = []
    no_of_trials_index = []
    for no_bingo_card, bingo_card in enumerate(bingo_cards_all):
        successful_marks = 0
        for no_of_trials, number in enumerate(numbers_drawn):
            new_bingo_card = np.where(bingo_card == number, -1, bingo_card)

            # check if bingo_card changed
            if np.array_equal(new_bingo_card, bingo_card):
                pass
            else:
                successful_marks += 1
                bingo_card = new_bingo_card
                indices = np.asarray(new_bingo_card == -1).nonzero()

                # check if there are 5 or more marks
                if len(indices[0]) > 4:
                    una_1 = np.unique(indices[0], return_counts=True)
                    una_2 = np.unique(indices[1], return_counts=True)

                    # check if there are 5 marks in a row in the vertical or horizontal direction
                    if (
                                (not np.where(una_1[1] == 5)[0].tolist() == []) or
                                (not np.where(una_2[1] == 5)[0].tolist() == [])
                    ):

                        # record successful bingo
                        no_of_trials_index.append(no_of_trials)
                        bingo_card_success_index.append((successful_marks, number))
                        bingo_cards_all[no_bingo_card] = new_bingo_card
                        break

    winner_index = no_of_trials_index.index(min(no_of_trials_index))
    score = (np.sum(bingo_cards_all[winner_index])
             + bingo_card_success_index[winner_index][0]) \
             * bingo_card_success_index[winner_index][1]

    return score


if __name__ == '__main__':
    print(f"Solution to part 1: {part_1()}")
    # print(f"Solution to part 2: {part_2()}")
