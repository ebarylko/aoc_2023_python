import toolz.functoolz as tfz
# import toolz.itertoolz as iter
# from functools import partial
# from operator import *
from day_2 import *

input = open("input.txt", "r").readlines()

line = open("input.txt", "r").readline()
example = line.split(r':')
divided = line.split(r':')[1].split(r';')

def parse_input(input_file):
    """
    @param input_file: the file containing the games
    @return: a collection of pairs of the form game id, cube sets
    """
    lines = open(input_file).readlines()
    return tfz.thread_last(
        lines,
        (map, methodcaller("split", r':')),
        list
        # (map, lambda line: line.split(r':'))
        # (map, methodcaller("split", r':')),
        # lambda lines: lines.split(r':'),
        # (map, split_id_and_cube_sets)
    )
# def test_input():
#     assert [line.strip() for line in divided] == "i"

def test_example():
    assert parse_input("input.txt") == "i"
    # assert split_id_and_cube_sets(example) == "i"

# def test_sum_valid_ids():
#     assert sum_valid_ids(example, example_limits) == 8