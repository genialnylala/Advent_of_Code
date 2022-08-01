from time import monotonic_ns
import logging
import sys
import networkx as nx
from collections import Counter
from collections.abc import Generator

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("net.log"),
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


def read_input(puzzle_file: str) -> nx.Graph:
    with open(puzzle_file, "r") as f:
        puzzle_input = f.read().splitlines()
    G = nx.Graph()
    for i in puzzle_input:
        x = i.split("-")
        G.add_edge(x[0], x[1])
    return G


def simple_paths_infinite_capital_nodes(G: nx.Graph, source: str, target: str) -> Generator[str]:
    """
    A modified depth-first search algorithm for paths, were nodes marked with capital letters
    are allowed to be repeated indefinitely.
    Inspired by https://networkx.org/documentation/stable/_modules/networkx/algorithms/simple_paths.html#all_simple_paths
    :param G: an undirected graph (no parallel edges)
    :param source: starting node
    :param target: ending node
    :return: a generator, generating the next path from source to target
    """

    targets = {target}
    visited = [source]
    stack = [iter(G[source])]  # create iterator for neighbours of source
    while stack:
        children = stack[-1]  # gets latest iterator
        child = next(children, None)
        if child is None:  # if no more neighbours
            stack.pop()  # delete latest iterator
            visited.pop()  # delete last visited node from path
        else:
            visited_lower = [node for node in visited if node.islower()]  # list of lower case nodes visited
            if child in visited_lower:  # if lower case node already visited in this path
                continue
            if child in targets:  # if arrived at ending node
                yield list(visited) + [child]  # generate path
            visited.append(child)  # append to visited nodes
            if targets - set(visited):
                stack.append(iter(G[child]))  # expand stack to investigate neighbours of child
            else:  # if end has been reached
                visited.pop()  # maybe other ways to child


def simple_paths_2_single_lowercase_nodes(G: nx.Graph, source: str, target: str) -> Generator[str]:
    """
    A modified depth-first search algorithm for paths, were nodes marked with capital letters
    are allowed to be repeated indefinitely, and one lowercase node can occur twice
    Inspired by https://networkx.org/documentation/stable/_modules/networkx/algorithms/simple_paths.html#all_simple_paths
    :param G: an undirected graph (no parallel edges)
    :param source: starting node
    :param target: ending node
    :return: a generator, generating the next path from source to target
    """
    targets = {target}
    visited = [source]
    stack = [iter(G[source])]  # create a list of neighbour iterators
    while stack:  # iterates over neighbours
        children = stack[-1]  # gets latest iterator
        child = next(children, None)
        if child is None:  # if no more neighbours
            stack.pop()  # delete neighbour iterator
            visited.pop()  # delete last visited node
        else:
            visited_lower = [node for node in visited if node.islower()]  # list of lower case nodes visited
            tot_low_visits = Counter(visited_lower)  # a counter of how often lowercase nodes visited
            if len(visited_lower) > 1:
                if tot_low_visits.most_common(1)[0][1] > 2 or \
                        tot_low_visits.most_common(2)[1][1] > 1:  # if one lowercase node visited >2 times
                    stack.pop()  # delete neighbour iterator
                    visited.pop()  # delete last visited node
                    continue
            if str(child) == "start":  # start node cannot repeat
                continue
            if child in targets:  # if arrived at destination
                yield list(visited) + [child]  # generate path
            visited.append(child)  # create new entry for if not visited
            if targets - set(visited):  # expand stack until find all targets
                stack.append(iter(G[child]))
            else:   # if end reached
                visited.pop()  # maybe other ways to child


@timer_func
def part_1() -> int:
    """
    :return:   Total number of paths
    """
    logging.info("Calculating the total number of simple paths where capital nodes can repeat")
    caves = read_input("puzzle_input.txt")

    # draw network
    # nx.draw_networkx(caves)
    # plt.savefig("caves")

    my_paths = []
    for path in simple_paths_infinite_capital_nodes(caves, "start", "end"):
        my_paths.append(path)
    no_paths = len(my_paths)

    logging.info(f"The total number of paths is {no_paths}")

    return no_paths


@timer_func
def part_2() -> int:
    """
    :return: Total number of paths
    """
    logging.info("Calculating the total number of simple paths where one lowercase node can occur twice")
    caves = read_input("puzzle_input.txt")

    my_paths = []
    for path in simple_paths_2_single_lowercase_nodes(caves, "start", "end"):
        my_paths.append(path)
    no_paths = len(my_paths)

    logging.info(f"The number of paths is {no_paths}")
    return no_paths


if __name__ == '__main__':
    print(f"Solution to part 1: {part_1()}")
    print(f"Solution to part 2: {part_2()}")
