import toolz.functoolz as tfz
import toolz.itertoolz as iter
import toolz.dicttoolz as dict
from functools import partial
from operator import *

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

def add_cube(coll, cube):
    return dict.assoc(coll, iter.second(cube), int(iter.first(cube)))

def add_cube_information(coll, cube_info):
    """
    @param coll: a map with key value pairs of the form cube color, number of cubes
    @param cube_info: the number of cubes and the color of the cubes
    @return: a new map with an additional entry corresponding to cube being added
    """
    return tfz.thread_last(
        cube_info.split(),
        (add_cube, coll)
    )


def cube_set_to_map(cube_set):
    """
    @param cube_set: a collection of cube colors and their corresponding number of cubes
    @return: a map with key value pairs of the form cube color, number of cubes
    """
    return tfz.reduce(add_cube_information, cube_set, {})

def id_and_max_number_of_all_cube_types(game):
    """
    @param game: a collection with the game id and the cube sets obtained in the game
    @return: a map with the key value pairs of game id and a collection containing the maximum number of cubes for each color type
    """
    return {iter.first(game): tfz.thread_last(
        game,
        iter.second,
        (map, cube_set_to_map),
        list,
        (dict.merge_with, max),
    )}
