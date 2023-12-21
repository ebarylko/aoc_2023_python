from day_1 import first_and_last_digit

input = open("input.txt", "r").readlines()

def test_first_and_last_digit():
    assert 12 == first_and_last_digit("1abc2")

