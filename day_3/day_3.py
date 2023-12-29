import toolz as tz
import itertools as it
import operator as op
import parsy as p
import re

non_digit_parser = p.regex(r'\D').many()
digit_parser = non_digit_parser >> p.regex(r'\d+')
line_parser = digit_parser.many().map(tz.compose(list, tz.partial(map, int)))


def is_valid_coordinate(coordinate, coordinate_range):
    return tz.first(coordinate_range) <= coordinate <= tz.last(coordinate_range)


def is_valid_location(x_coordinate_range, y_coordinate_range, location):
    """
    @param location: a pair with an x, y coordinate
    @param x_coordinate_range: the lower and upper bounds of the x coordinates
    @param y_coordinate_range: the lower and upper bounds of the y coordinates
    @return: true if the location has a valid x and y coordinate
    ex: is_valid_location([0, 1], [0, 1], [1, 1]) == true
    is_valid_location([0, 1], [0, 1], [-1, 1]) == false
    """
    return is_valid_coordinate(tz.first(location), x_coordinate_range) and is_valid_coordinate(tz.second(location),
                                                                                               y_coordinate_range)


def possible_surrounding_symbols(location, coordinate_restrictions):
    """
    @param location: the x,y coordinates of the digit
    @param coordinate_restrictions: the boundaries for the x and y coordinates
    @return: all the possible locations for a symbol
    adjacent to the digit
    ex: possible_part_number_locations([0,0], [[0, 1], [0, 1]]) == {(1, 0), (0, 1), (1, 1)}
    """
    return tz.thread_last(
        range(-1, 2),
        lambda pos_shifts: it.product(pos_shifts, repeat=2),
        (filter, any),
        (zip, it.repeat(location)),
        (map, lambda coll: tuple(map(op.add, *coll))),
        (filter, tz.partial(is_valid_location, tz.first(coordinate_restrictions), tz.last(coordinate_restrictions))),
        set,
    )


def possible_symbol_locations(partial_schematic):
    """
    @param partial_schematic: two or three line of the schematic
    @return: a collection of all the possible locations for a symbol
    adjacent to the numbers in the second line of the partial schematic
    ex: possible_part_number_locations([0, 1])
    """
    return tz.thread_last(
        partial_schematic,
        tz.second,
        (re.finditer, r"\d+"),
        (map, tz.partial(op.methodcaller("span"))),
        list,
        (map, (tz.juxt(
            tz.first,
            tz.compose(
                tz.partial(op.neg),
                tz.partial(op.sub, 1),
                tz.partial(tz.second))))),
        list,

    )


def get_all_schematic_triplets(schematics):
    """
    @param schematics: a collection of lines containing symbols, periods, and numbers
    @return: the collection partitioned into sets of three schematics
    ex: get_all_schematic_triplets([".1", ".2", ".3", ".4"]) -> [{".1", ".2", ".3"}]
    """
    return tz.thread_last(
        schematics,
        (tz.sliding_window, 3),
        (tz.remove, lambda coll: len(coll) < 3),
        list
    )


def get_first_and_last_schematic_duplet(schematic):
    """
    @param schematic: a collection of lines containing symbols, periods, and numbers
    @return: the first partition after reversing it and the last partition
    of the schematic after partitioning it into sets of two
    ex: get_first_and_last_schematic_duplet([".1", ".2", ".3", ".4"]) == [(".2", ".1"), (".3", ".4")]
    """
    return tz.thread_last(
        schematic,
        (tz.sliding_window, 2),
        (tz.juxt(
            tz.compose(
                tz.juxt(tz.last, tz.first), tz.first),
            tz.last))
    )


def sum_part_numbers(schematic):
    """
    @param schematic: a collection of lines containing symbols, periods, and numbers
    @return: the sum of all the part numbers in the schematic
    """
    return tz.thread_last(
        schematic,
        get_all_schematic_triplets,
        (it.chain, get_first_and_last_schematic_duplet(schematic)),
        tz.first,
        # tz.second,
        # list
    )
