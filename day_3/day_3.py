import toolz as tz
import itertools as it
import operator as op
import parsy as p
import re

non_digit_parser = p.regex(r'\D').many()
digit_parser = non_digit_parser >> p.regex(r'\d+') << non_digit_parser


@p.generate
def digit_with_range_parser():
    yield non_digit_parser
    start = yield p.index
    number = yield p.regex(r'\d+').map(int)
    end = yield p.index
    yield non_digit_parser
    return number, (start, end - 1)


line_parser = digit_with_range_parser.many()


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


def possible_surrounding_symbols(coordinate_restrictions, location):
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
        (filter, tz.partial(is_valid_location, tz.first(coordinate_restrictions), tz.second(coordinate_restrictions))),
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
        (map, lambda coll: tz.thread_last(
            range(*coll),
            list)),
        list,
        (map, tz.partial(generate_symbol_locations_for_number, [0, len(tz.first(partial_schematic)) - 1],
                         [0, len(partial_schematic) - 1])),
        list,
        (zip, line_parser.parse(tz.second(partial_schematic)))
        # (map, generate_symbol_locations_for_number, [0, len(tz.first(partial_schematic))], [0, len(partial_schematic)]),
        # list
        # (map, (tz.juxt(
        #     tz.first,
        #     tz.compose(
        #         tz.partial(op.neg),
        #         tz.partial(op.sub, 1),
        #         tz.partial(tz.second))))),
        # list,
        # (map, )

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


def coordinates_spanned_by_number(x_coordinate_range):
    """
    @param x_coordinate_range: the x coordinates the number spans
    @return: a collection of the coordinates spanned by the number
    coordinates_spanned_by_number([0, 2]) = {(0, 1), (1, 1), (2, 1)}
    """
    return tz.thread_first(
        x_coordinate_range,
        (zip, it.repeat(1)),
        set
    )


def generate_symbol_locations_for_number(x_coordinate_limits, y_coordinate_limits, span_of_number):
    """
    @param span_of_number: a collection of the x coordinates that the number occupies
    @param x_coordinate_limits: the lower and upper bound for the x coordinates
    @param y_coordinate_limits: the lower and upper bound for the y coordinates
    @return: the union of all the possible symbol locations for each x coordinate
    """
    return tz.thread_last(
        span_of_number,
        coordinates_spanned_by_number,
        list,
        (map, tz.partial(possible_surrounding_symbols, [x_coordinate_limits, y_coordinate_limits])),
        list,
        (tz.juxt(tz.first,
                 tz.compose(
                     list,
                     tz.partial(
                         tz.drop, 1)))),
        lambda coll: tz.first(coll).union(*tz.second(coll)),
        lambda s: s - coordinates_spanned_by_number(span_of_number)

        # lambda coll: x.union(*coll),
        # list
        # (map, list),
        # (map, op.methodcaller("insert", 1, 1)),
    )


def find_numbers_and_positions(line):
    """
    @param line: a line of the schematic
    @return: a collection of pairs of the numbers in the line and their span
    ex: find_numbers_and_positions("46..") -> [(46, [0, 1])]
    """
    pass


def sum_part_numbers(schematic):
    """
    @param schematic: a collection of lines containing symbols, periods, and numbers
    @return: the sum of all the part numbers in the schematic
    """
    return tz.thread_last(
        schematic,
        (tz.mapcat, find_numbers_and_positions),  # (46, [[0,1], [0,2]])
        (filter, tz.partial(is_part_number, schematic)),
        (map, tz.first),
        sum
    )
    # return tz.thread_last(
    #     schematic,
    #     get_all_schematic_triplets,
    #     (it.chain, get_first_and_last_schematic_duplet(schematic)),
    #     tz.first,
    #     # tz.second,
    #     # list
    # )
