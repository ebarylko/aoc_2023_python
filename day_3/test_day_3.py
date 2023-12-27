import day_3 as d3

data = open("input.txt").readlines()
sample = ["467..114..",
          "...*......",
          "..35..633.",
          "......#...",
          "617*......",
          ".....+.58.",
          "..592.....",
          "......755.",
          "...$.*....",
          ".664.598.."
          ]


def test_is_valid_coordinate():
    assert d3.is_valid_coordinate(1, [0, 2])
    assert not d3.is_valid_coordinate(-1, [0, 2])


def test_is_valid_location():
    assert d3.is_valid_location([0, 0], [0, 2], [0, 2]) == 1
    assert not d3.is_valid_location([0, -1], [0, 2], [0, 2]) == 1
    assert not d3.is_valid_location([4, -1], [0, 2], [0, 2]) == 1


def test_possible_part_number_locations():
    assert (d3.possible_part_number_locations((1, 1)) ==
            {(1, 0), (0, 0), (0, 1), (2, 1), (2, 2), (1, 2), (2, 0), (0, 2)})
    assert (d3.possible_part_number_locations((0, 0)) ==
            {(1, 0), (0, 1), (1, 1)})


def test_get_all_schematic_triplets():
    assert d3.get_all_schematic_triplets([".1", ".2", ".3", ".4"]) == [(".1", ".2", ".3"), (".2", ".3", ".4")]


def test_get_first_and_last_schematic_duplet():
    assert d3.get_first_and_last_schematic_duplet((".1", ".2", ".3", ".4")) == ((".1", ".2"), (".3", ".4"))


def test_sum_part_numbers():
    assert d3.sum_part_numbers(sample) == 4361
