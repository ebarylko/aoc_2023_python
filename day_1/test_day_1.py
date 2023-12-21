from day_1 import first_and_last_digit, sum_lines

input = open("input.txt", "r").readlines()

example_input = ["1abc2", "a1b2c3d4e5f", "treb7uchet", "pqr3stu8vwx"]

def test_first_and_last_digit():
    assert 12 == first_and_last_digit("1abc2")
    assert 15 == first_and_last_digit("a1b2c3d4e5f")
    assert 77 == first_and_last_digit("treb7uchet")

def test_sum_lines():
    assert 142 == sum_lines(example_input)
