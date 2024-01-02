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


def find_numbers_and_positions(t):
    """
    @param t: a tuple with the row index and a line of the schematic
    @return: a collection of triplets of the numbers in the line, the row index, and their span
    ex: find_numbers_and_positions((1, "46..")) -> [(46, 1, (0, 2))]
    """
    index, line = t
    parsed = parse_line(line)
    return [] if not parsed else [(a, index, b) for a, b in parsed]


def generate_neighbours(t):
    number, row, x_coordinates = t
    column_span = range(*x_coordinates)
    surrounding_rows = [row - 1, row, row + 1]
    return set([(row - 1, y) for y in column_span] +
               [(row + 1, y) for y in column_span] +
               [(r, x_coordinates[0] - 1) for r in surrounding_rows] +
               [(r, x_coordinates[1]) for r in surrounding_rows])


def is_part_number(schematic, number_info):
    """
    @param schematic: a collection of lines containing numbers, symbols, and periods
    @param number_info: a triplet containing a number, the row it is in, and the x coordinates it spans
    @return: true if there is a symbol adjacent to the number. False otherwise
    ex: is_part_number(["....", "..1."], [(1, 1, (2, 3))]) -> false
    ex: is_part_number(["..*.", "..1."], [(1, 1, (2, 3))]) -> true
    """
    def contains_symbol(pos):
        x, y = pos
        return x in range(0, len(schematic)) and y in range(0, len(schematic[0])) and schematic[x][
            y] not in ".0123456789"

    return tz.thread_last(
        number_info,
        generate_neighbours,
        (filter, contains_symbol),
        tz.count
    )



def sum_part_numbers(schematic):
    """
    @param schematic: a collection of lines containing symbols, periods, and numbers
    @return: the sum of all the part numbers in the schematic
    """
    return tz.thread_last(
        schematic,
        enumerate,
        (tz.mapcat, find_numbers_and_positions),  # (46, (1, 2))
        (filter, tz.partial(is_part_number, schematic)),
        (map, tz.first),
        sum,
    )


def find_potential_gear_positions(t):
    """
    @param t: a tuple containing the row number and the line of the schematic corresponding to that row
    @return: the positions of all potential gears in the line
    ex: find_potential_gear_positions((1, "12...*..*)) -> [(1, 5), (1, 8)]
    """
    row_number, line = t
    return tz.thread_last(
        line,
        (re.finditer, r"\*"),
        (map, tz.compose(tz.first, op.methodcaller("span"))),
        (zip, it.repeat(row_number)),
    )


def adjacent_numbers(schematic, possible_gear_location):
    """
    @param schematic: a collection of lines containing symbols, periods, and digits
    @param possible_gear_location: the x, y coordinates of a potential gear
    @return: a collection of the numbers surrounding each gear
    """
    x, y = possible_gear_location
    possible_positions = it.product([x - 1, x, x + 1], [y - 1, y, y + 1])
    return tz.thread_last(
        possible_positions,
        list
    )


#     return tz.thread_last(
#         range(-1, 2),
# (lambda r: it.product(r, repeat=2)),
#         list,
#         (map, lambda c1, c2: (c1[0] + c2[0], c1[1] + c2[1]), it.repeat(possible_gear_location)),
#         list
#
#     )


def find_surrounding_numbers(schematic, coll):
    """
    @param coll: a collection of the positions of potential gears in a row
    @return: a collection of the numbers surrounding each potential gear
    """
    return tz.thread_last(
        coll,
        (map, adjacent_numbers)
    )


def valid_gears_product(positions_of_numbers, gear_position):
    """
    @param positions_of_numbers: a dictionary with the row and all the numbers in that row
    @param gear_position: the x, y coordinates of a gear
    @return: 0 if the gear is not surrounded by two numbers. Otherwise, returns the product of the two numbers
    """
    x, y = gear_position
    return tz.thread_last(
        [x - 1, x, x + 1],
        (tz.mapcat, lambda row: positions_of_numbers.get(row, [])),
        (filter, lambda number_info: gear_position in generate_neighbours(number_info)),
        (tz.map, tz.first),
        list,
        lambda numbers: tz.reduce(op.mul, numbers) if len(numbers) == 2 else 0
    )


def sum_gear_ratios(schematic):
    """
    @param schematic: a collection of lines containing symbols, periods, and digits
    @return: the sum of all the gear ratios in the schematic
    ex: sum_gear_ratios(["....*4..", "....5..."]) -> 20
    """
    numbers_and_positions = tz.thread_last(
        schematic,
        enumerate,
        (tz.mapcat, find_numbers_and_positions),
        (tz.groupby, tz.second))

    return tz.thread_last(
        schematic,
        enumerate,
        (tz.mapcat, find_potential_gear_positions),  # [(0, 1), (0, 5), (1, 3)]
        (tz.map, tz.partial(valid_gears_product, numbers_and_positions)),  # [1, 3, 17, 19]
        list,
        sum
    )
