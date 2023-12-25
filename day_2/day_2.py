import toolz.functoolz as tfz
import toolz.itertoolz as itz
import toolz.dicttoolz as tzd
import operator as op
import parsy as p

number_parser = p.regex(r'\d+').map(int)
color_parser = p.string("red") | p.string("green") | p.string("blue")

number_color_parser = p.seq(number_parser << p.whitespace, color_parser << p.string("\n").optional()).map(
    lambda t: [t[1], t[0]])

set_parser = number_color_parser.sep_by(p.string(",") << p.whitespace, min=1, max=3).map(dict)

game_parser = set_parser.sep_by(p.string(";") << p.whitespace, min=1).map(tfz.partial(tzd.merge_with, max))

id_parser = p.string("Game ") >> number_parser
line_parser = p.seq(id_parser << p.string(": "), game_parser)


def input_parser(lines):
    """
    @param lines: all the games
    @return: a map with key value pairs of the form game id and a collection noting the maximum number
    of each cube color in the game
    """

    return tfz.thread_last(lines, (map, line_parser.parse), dict)


def is_valid_game(cube_limits, cube_sets):
    """
    @param cube_limits: the maximum number of red, blue, and green cubes
    @param cube_sets: the largest number of red, blue, and green cubes drawn in the game
    @return: true if the number of drawn cubes for every color is less than or equal to the maximum
    number of cubes for that color
    """
    return tfz.thread_last(
        cube_sets,
        (op.itemgetter("red", "green", "blue")),
        (zip, cube_limits),
        (itz.filterfalse, lambda p: p[0] >= p[1]),
        list,
        op.not_
    )


def sum_valid_ids(games, cube_limits):
    """
    @param games: a collection of games which have an id and corresponding cube sets
    @param cube_limits: the maximum number of red, blue, and green cubes that can be drawn
    @return: the sum of all game ids which have cube sets which draw less than or the same amount of cubes in cube_limits for that specific color
    """
    return tfz.pipe(
        games,
        input_parser,
        tfz.partial(tzd.valfilter, tfz.partial(is_valid_game, cube_limits)),
        op.methodcaller("keys"),
        sum
    )


def game_power(game):
    """
    @param game: a map with key value pairs of colors and the amount of cubes for that color
    @return: the product of all cubes
    """
    return tfz.pipe(
        game,
        op.itemgetter("red", "green", "blue"),
        tfz.partial(tfz.reduce, op.mul)
    )


def sum_power_of_games(games):
    """
    @param games: A collection of games containing a game id and the corresponding cube sets
    @return: the sum of the power of all games
    """
    return tfz.thread_last(
        games,
        input_parser,
        (tzd.valmap, game_power),
        lambda m: m.values(),
        sum
    )
