import toolz.functoolz as tfz
import toolz.itertoolz as iter
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
