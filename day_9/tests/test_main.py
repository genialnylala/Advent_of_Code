from day_9.src.main import find_minima, calc_risk
import numpy as np

x = np.array([[2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
              [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
              [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
              [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
              [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]])
minima = np.array([[False, True, False, False, False, False, False, False, False, True],
                   [False, False, False, False, False, False, False, False, False, False],
                   [False, False, True, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, True, False, False, False]])


def test_find_minima():
    assert np.array_equal(find_minima(x), minima)


def test_calc_risk():
    assert calc_risk(minima, x) == 15
