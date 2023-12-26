input = open("input.txt").readlines()
import day_3 as d3

def test_possible_part_number_locations():
    assert (d3.possible_part_number_locations([1, 1]) ==
            {(1, 0), (0, 0), (0, 1), (2, 1), (2, 2), (1, 2), (2, 0), (0, 2)})

# def test_sum_part_numbers():
#     assert sum_part_numbers(sample) == 4361