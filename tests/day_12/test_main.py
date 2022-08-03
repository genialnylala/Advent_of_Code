"""
Day 12 Tests
"""
from solutions.day_12.main import read_input, simple_paths_infinite_capital_nodes,\
    simple_paths_2_single_lowercase_nodes

caves_small = read_input("tests/day_12/simple_network.txt")
caves_medium = read_input("tests/day_12/medium_network.txt")
caves_large = read_input("tests/day_12/large_network.txt")


def test_simple_paths_infinite_capital_nodes():
    """
    Tests the simple_paths_infinite_capital_nodes function
    """
    paths = []
    for path in simple_paths_infinite_capital_nodes(caves_small, "start", "end"):
        paths.append(path)
    assert len(paths) == 10

    paths = []
    for path in simple_paths_infinite_capital_nodes(caves_medium, "start", "end"):
        paths.append(path)
    assert len(paths) == 19

    paths = []
    for path in simple_paths_infinite_capital_nodes(caves_large, "start", "end"):
        paths.append(path)
    assert len(paths) == 226


def test_simple_paths_2_single_lowercase_nodes():
    """
    Test the simple_paths_2_single_lowercase_nodes function
    """
    paths = []
    for path in simple_paths_2_single_lowercase_nodes(caves_small, "start", "end"):
        paths.append(path)
    assert len(paths) == 36

    paths = []
    for path in simple_paths_2_single_lowercase_nodes(caves_medium, "start", "end"):
        paths.append(path)
    assert len(paths) == 103

    paths = []
    for path in simple_paths_2_single_lowercase_nodes(caves_large, "start", "end"):
        paths.append(path)
    assert len(paths) == 3509
