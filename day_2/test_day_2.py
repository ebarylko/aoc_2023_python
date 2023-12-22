import toolz.functoolz as tfz
import toolz.itertoolz as iter
from functools import partial
from operator import *

input = open("input.txt", "r").readlines()

line = open("input.txt", "r").readline()
example = line.split(r':')
divided = line.split(r':')[1].split(r';')

def cube_sets(games):
    """
    @param games: a collection of games
    @return: the cube sets for each game
    """
    return tfz.thread_last(
        games,
        iter.second,
        lambda cube_set: cube_set.split(r';'),
        (map, lambda cubes: cubes.split(r',')),
        list,
        (map, tfz.compose(list, partial(map, methodcaller('strip')))),
        list
    )

def game_id(game):
    """
    @param game: a pair of the form game_id, cube_sets
    @return: the numerical value of the game id
    """
    return tfz.thread_last(
        game,
        iter.first,
        iter.last,
        int
    )

def split_id_and_cube_sets(games):
    """
    @param games: a collection of games
    @return: a collection of pairs of game ids and their corresponding cube sets
    """
    return tfz.juxt(game_id, cube_sets)(games)

def parse_input(input):
    """
    @param input: the file containing the games
    @return: a collection of pairs of the form game id, cube sets
    """
    tfz.thread_last(
        input,
        open,
        lambda file: file.readlines(),
        lambda lines: lines.split(r':'),
        split_id_and_cube_sets
    )
# def test_input():
#     assert [line.strip() for line in divided] == "i"

def test_example():
    assert split_id_and_cube_sets(example) == "i"

# def test_sum_valid_ids():
#     assert sum_valid_ids(example, example_limits) == 8