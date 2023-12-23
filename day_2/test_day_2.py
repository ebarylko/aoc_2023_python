import toolz.functoolz as tfz
# import toolz.itertoolz as iter
# from functools import partial
# from operator import *
from day_2 import *

input = open("input.txt", "r").readlines()

line = open("input.txt", "r").readline()
example_input = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"]



def parse_input(input):
    """
    @param input: all the games with the corresponding sets of cubes
    @return: a collection of pairs of the form game id, cube sets
    """
    return tfz.thread_last(
        input,
        list,
        (map, methodcaller("split", r':')),
        list,
        (map, tfz.compose(list, split_id_and_cube_sets)),
        list,
        iter.first,
        id_and_max_number_of_all_cube_types,
        # iter.second,
        # (map, cube_set_to_map),
        # list,
        # (dict.merge_with, max)
    )
# def test_input():
#     assert [line.strip() for line in divided] == "i"

def test_add_cube_information():
    assert add_cube_information({}, '4 green') == {"green": 4}
def test_cube_set_to_map():
    assert cube_set_to_map(['4 green', '3 blue', '11 red']) == {"green": 4, "blue": 3, "red": 11}
def test_example():
    assert parse_input(example_input) == "1"
    assert parse_input(input) == "i"
    # assert split_id_and_cube_sets(example) == "i"


# def test_sum_valid_ids():
#     assert sum_valid_ids(example, example_limits) == 8