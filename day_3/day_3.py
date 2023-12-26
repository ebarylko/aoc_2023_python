import toolz as tz
import itertools as it
import operator as op
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
        # (map, op.add, it.repeat(location)),
        list

        # (it.product, repeat=2)
    )