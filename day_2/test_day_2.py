import toolz.functoolz as tfz
# import toolz.itertoolz as iter
# from functools import partial
# from operator import *
import pytest
from day_2 import *

input = open("input.txt", "r").readlines()

line = open("input.txt", "r").readline()

example_input = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"]

example_limits = [12, 13, 14]

small_example = [
    "Game 16: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
]



def test_add_cube_information():
    assert add_cube_information({}, '4 green') == {"green": 4}
def test_cube_set_to_map():
    assert cube_set_to_map(['4 green', '3 blue', '11 red']) == {"green": 4, "blue": 3, "red": 11}
def test_example():
    assert parse_input(example_input) == "1"
    assert parse_input(input) == "i"
    # assert split_id_and_cube_sets(example) == "i"

def test_number_parser():
    assert number_parser.parse("4") == 4

def test_number_color_parser():
    assert number_color_parser.parse("4 green") == [4, "green"]

def test_set_parser():
    assert set_parser.parse("3 blue, 4 red") == {"blue": 3, "red": 4}

def test_game_parser():
    assert game_parser.parse("3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green") == {"green": 2, "blue": 6, "red": 4}

def test_id_parser():
    assert id_parser.parse("Game 1") == 1
def test_line_parser():
    assert line_parser.parse("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green") == [1, {"green": 2, "blue": 6, "red": 4}]

def test_input_parser():
    assert input_parser(example_input) == {1:  {"blue": 6, "red": 4, "green": 2},
                                                  2: {"blue": 4, "green": 3, "red": 1},
                                                  3: {"blue": 6, "green": 13, "red": 20},
                                                  4: {"green": 3, "blue": 15, "red": 14},
                                                  5: {"green": 3, "blue": 2, "red": 6}
                                                  }

@pytest.mark.parametrize("test_input", [ "red", "green", "blue"])
def test_eval(test_input):
    assert color_parser.parse(test_input) == test_input

def test_is_valid_game():
    assert is_valid_game([12, 13, 14], {"blue": 6, "green": 2, "red": 4}) == True
    assert is_valid_game([12, 13, 14], {"blue": 9, "green": 11, "red": 13}) == False
def test_sum_valid_ids():
    assert sum_valid_ids(example_input, example_limits) == 8
    # assert sum_valid_ids(input, [12, 13, 14]) == 1

