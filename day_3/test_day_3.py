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


def test_non_digit_parser():
    assert d3.non_digit_parser.parse("......&#%@(%@(&%")


def test_digit_parser():
    assert d3.digit_parser.parse("....123") == '123'


def test_line_parser():
    assert d3.line_parser.parse("..20...19") == [20, 19]


def test_is_valid_coordinate():
    assert d3.is_valid_coordinate(1, [0, 2])
    assert not d3.is_valid_coordinate(-1, [0, 2])


def test_is_valid_location():
    assert d3.is_valid_location([0, 0], [0, 2], [0, 2]) == 1
    assert not d3.is_valid_location([0, -1], [0, 2], [0, 2]) == 1
    assert not d3.is_valid_location([4, -1], [0, 2], [0, 2]) == 1


def test_possible_surrounding_symbols():
    assert (d3.possible_surrounding_symbols((1, 1), [[0, 2], [0, 2]]) ==
            {(1, 0), (0, 0), (0, 1), (2, 1), (2, 2), (1, 2), (2, 0), (0, 2)})
    assert (d3.possible_surrounding_symbols((0, 0), [[0, 1], [0, 1]]) ==
            {(1, 0), (0, 1), (1, 1)})


def test_get_all_schematic_triplets():
    assert d3.get_all_schematic_triplets([".1", ".2", ".3", ".4"]) == [(".1", ".2", ".3"), (".2", ".3", ".4")]


def test_get_first_and_last_schematic_duplet():
    assert d3.get_first_and_last_schematic_duplet((".1", ".2", ".3", ".4")) == ((".2", ".1"), (".3", ".4"))


def test_possible_symbol_locations():
    assert d3.possible_symbol_locations(("...*..", "46.14.")) == {46: ([0, 0], [0, 1], [0, 2], [1, 3], [0, 3]),
                                                                  14: ([1, 2], [1, 5], [0, 2], [0, 3], [0, 4], [0, 5])}


def test_sum_part_numbers():
    assert d3.sum_part_numbers(sample) == 4361
