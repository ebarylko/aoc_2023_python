import toolz as tz
import itertools as it
import operator as op

def generate_valid_locations(x_coordinates, y_coordinates):
    return

def is_valid_coordinate(coordinate, coordinate_range):
    return tz.first(coordinate_range) <= coordinate <= tz.last(coordinate_range)

def is_valid_location(location, x_coordinate_range, y_coordinate_range):
    """
    @param location: a pair with an x, y coordinate
    @param x_coordinate_range: a collection of valid x coordinates
    @param y_coordinate_range: a collection of valid y coordinates
    @return: true if the location has a valid x and y coordinate
    """
    return is_valid_coordinate(tz.first(location), x_coordinate_range) and is_valid_coordinate(tz.second(location), y_coordinate_range)

def possible_part_number_locations(location):
    """
    @param location: the x,y coordinates of the symbol
    @return: all the possible locations for a part number
    adjacent to the symbol
    """
    # return list(it.repeat(location, 2))
    return tz.thread_last(
        range(-1, 2),
        lambda pos_shifts: it.product(pos_shifts, repeat=2),
        (filter, any),
        (zip, it.repeat(location)),
        (map, lambda coll: tuple(map(op.add, *coll))),
        # (filter, is_valid_location),
        set,
    )
