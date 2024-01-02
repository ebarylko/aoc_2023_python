import day_3 as d3

data = open("input.txt").read().splitlines()
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


def test_parse_line():
    assert d3.parse_line("46.1408.") == [(46, (0, 2)), (1408, (3, 7))]
    assert not d3.parse_line("........")


def test_find_numbers_and_positions():
    assert d3.find_numbers_and_positions((1, "43..")) == [(43, 1, (0, 2))]


def test_is_part_number():
    assert d3.is_part_number(["...#..", "..12.."], (12, 1, (2, 4)))
    assert d3.is_part_number(["....#.", "..12.."], (12, 1, (2, 4)))
    assert not d3.is_part_number([".....#", "..12.."], (12, 1, (2, 4)))


def test_sum_part_numbers():
    assert d3.sum_part_numbers(sample) == 4361
    assert d3.sum_part_numbers(data) == 550934


def test_find_potential_gear_positions():
    assert d3.find_potential_gear_positions((1, "...*")) == [(1, 3)]
    assert d3.find_potential_gear_positions((1, "....")) == []
    assert d3.find_potential_gear_positions((1, "*.2*")) == [(1, 0), (1, 3)]


def test_valid_gears_product():
    sample_1 = {0: [(1, 0, (1, 2)), (3, 0, (3, 4)), (6, 0, (4, 5))]}
    sample_2 = {0: [(1, 0, (1, 2)), (3, 0, (3, 4)), (6, 0, (2, 3))]}
    assert d3.valid_gears_product(sample_1, (1, 2)) == 3
    assert d3.valid_gears_product(sample_2, (1, 2)) == 0

def test_adjacent_numbers():
    assert d3.adjacent_numbers(["..1..", "..*..", "..12."], (1, 2)) == [1, 12]

def test_find_surrounding_numbers():
    assert d3.find_surrounding_numbers(["..1..", "..*..", "..12."], [[(1, 2)]]) == [1, 12]


def test_generate_neighbours():
    assert d3.generate_neighbours((12, 1, (1, 3))) == 1


def test_sum_gear_ratios():
    assert d3.sum_gear_ratios(sample) == 467835
    assert d3.sum_gear_ratios(data) == 81997870
