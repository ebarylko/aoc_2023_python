import toolz.functoolz as tfz
import toolz.itertoolz as iter
import toolz.dicttoolz as tzd
from functools import partial
from operator import *
import parsy as p

number_parser = p.regex(r'\d+').map(int)
color_parser = p.string("red") | p.string("green") | p.string("blue")

number_color_parser = p.seq(number_parser << p.whitespace, color_parser << p.string("\n").optional()).map(lambda t: [t[1], t[0]])
set_parser = number_color_parser.sep_by(p.string(",") << p.whitespace, min=1, max=3).map(dict)
game_parser = set_parser.sep_by(p.string(";") << p.whitespace, min=1).map(tfz.partial(tzd.merge_with, max))
id_parser = p.string("Game ") >> number_parser
line_parser = p.seq(id_parser << p.string(": "), game_parser)
def input_parser(lines):
    return tfz.thread_last(
        lines,
(map, lambda line: line_parser.parse(line)),
        dict
    )
def parse_input(input):
    """
    @param input: all the games with the corresponding sets of cubes
    @return: a collection of pairs of the form game id, cube sets
    """
    # return input_parser(input)
    # return tfz.thread_last(
    #     input,
    #     list,
    #     (map, methodcaller("split", r':')),
    #     list,
    #     (map, tfz.compose(list, split_id_and_cube_sets)),
    #     list,
    #     (map, id_and_max_number_of_all_cube_types),
    #     list
    # )

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
        lambda id: id.split(),
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
    return tzd.assoc(coll, iter.second(cube), int(iter.first(cube)))

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
        (tzd.merge_with, max),
    )}

def all_cube_numbers():
    return itemgetter("red", "green", "blue")
def is_valid_game(cube_limits, cube_sets):
    """
    @param cube_limits: the maximum number of red, blue, and green cubes
    @param game: a collection with the game id and the largest number of red, blue, and green cubes drawn
    @return: true if the number of drawn cubes for every color is less than or equal to the maximum
    number of cubes for that color
    """
    [max_red_cubes, max_green_cubes, max_blue_cubes] = cube_limits
    [red_cubes, green_cubes, blue_cubes] = itemgetter("red", "green", "blue")(cube_sets)
    return red_cubes <= max_red_cubes and green_cubes <= max_green_cubes and blue_cubes <= max_blue_cubes

def sum_valid_ids(games, cube_limits):
    """
    @param games: a collection of games which have an id and corresponding cube sets
    @param cube_limits: the maximum number of red, blue, and green cubes that can be drawn
    @return: the sum of all game ids which have cube sets which draw less than or the same amount of cubes in cube_limits for that specific color
    """
    return tfz.thread_last(
        games,
        input_parser,
        (tzd.valfilter, tfz.partial(is_valid_game, cube_limits)),
        lambda m: m.keys(),
        list,
        sum
    )

def game_power(game):
    """
    @param game: a map with key value pairs of game id, cube sets
    @return: the power of the set
    """
    return tfz.pipe(
        game,
        methodcaller("values"),
        list,
        iter.first,
        itemgetter("red", "green", "blue"),
        tfz.partial(tfz.reduce, mul)
    )


def sum_power_of_games(games):
    """
    @param games: A collection of games containing a game id and the corresponding cube sets
    @return: the sum of the power of all games
    """
    return tfz.thread_last(
        games,
        input_parser,
        (map, game_power)
    )