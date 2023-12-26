import toolz as tz
import itertools as it
def possible_part_number_locations(location):
    return tz.thread_last(
        range(-1, 2),
        lambda pos_shifts: it.product(pos_shifts, repeat=2),
        (filter, any),
        list

        # (it.product, repeat=2)
    )