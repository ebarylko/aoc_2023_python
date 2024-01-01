import toolz as tz
import itertools as it
import operator as op
import parsy as p
import re


def parse_line(line):
    """
    @param line: the line from the schematic
    @return: a collection of the results of calling line_parser multiple times
    ex: parse_line('1.2') == [(1, (0)), (2, (2))]
    """
    return tz.thread_last(
        line,
        (re.finditer, r"\d+"),
        (map, lambda m: (int(m.group(0)), m.span())),
        list
    )


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


def find_numbers_and_positions(t):
    """
    @param t: a tuple with the row index and a line of the schematic
    @return: a collection of triplets of the numbers in the line, the row index, and their span
    ex: find_numbers_and_positions((1, "46..")) -> [(46, 1, [0, 1])]
    """
    index, line = t
    parsed = parse_line(line)
    return [] if not parsed else [(a, index, b) for a, b in parsed]


def is_part_number(schematic, number_info):
    """
    @param schematic: a collection of lines containing numbers, symbols, and periods
    @param number_info: a triplet containing a number, the row it is in, and the x coordinates it spans
    @return: true if there is a symbol adjacent to the number. False otherwise
    """

    num, row, x_coordinates = number_info

    possible_locations = [[row - 1, y] for y in range(*x_coordinates)] + \
                         [[row + 1, y] for y in range(*x_coordinates)] + \
                         [[r, x_coordinates[0] - 1] for r in [row - 1, row, row + 1]] + \
                         [[r, x_coordinates[1]] for r in [row - 1, row, row + 1]]

    def contains_symbol(pos):
        x, y = pos
        return x in range(0, len(schematic)) and y in range(0, len(schematic[0])) and schematic[x][y] not in ".0123456789"

    locations = list(filter(contains_symbol, possible_locations))
    return tz.thread_last(
        possible_locations,
        (filter, contains_symbol),
        tz.count
    )


def sum_part_numbers(schematic):
    """
    @param schematic: a collection of lines containing symbols, periods, and numbers
    @return: the sum of all the part numbers in the schematic
    """
    return tz.thread_last(
        enumerate(schematic),
        (tz.mapcat, find_numbers_and_positions),  # (46, (1, 2))
        (filter, tz.partial(is_part_number, schematic)),
        (map, tz.first),
        sum,
    )


def find_potential_gear_positions(t):
    """
    @param t: a tuple containing the row number and the line of the schematic corresponding to that row
    @return: the positions of all the potential gears in the line
    """
    row_number, line = t
    return tz.thread_last(
        line,
        (re.finditer, r"\*"),
        (map, tz.compose(tz.first, op.methodcaller("span"))),
        (zip, it.repeat(row_number)),
        list
    )



def sum_gear_ratios(schematic):
    """
    @param schematic: a collection of lines containing symbols, periods, and digits
    @return: the sum of all the gear ratios in the schematic
    encontrar las posiciones de todas las estrellas en el schematic
    encontrar la cantidad de numeros al rededor de las estrellas
    filtrar las estrellas que solo tienen dos numeros
    tomar el producto de los numeros en cada estrella
    """
    return tz.thread_last(
        schematic,
        enumerate,
        list,
        (map, find_potential_gear_positions)
    )
