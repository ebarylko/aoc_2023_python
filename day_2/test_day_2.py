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
(iter.take, 1),
        list,
        (map, methodcaller("split", r':')),
        list,
        (map, tfz.compose(list, split_id_and_cube_sets)),
        list
    )
# def test_input():
#     assert [line.strip() for line in divided] == "i"

def test_add_cube_information():
    assert add_cube_information({}, '4 green') == {"green": 4}
def test_cube_set_to_map():
    assert cube_set_to_map(['4 green', '3 blue', '11 red']) == {"green": 4, "blue": 3, "red": 11}
def test_example():
    assert parse_input("input.txt") == "i"
    # assert split_id_and_cube_sets(example) == "i"


# def test_sum_valid_ids():
#     assert sum_valid_ids(example, example_limits) == 8