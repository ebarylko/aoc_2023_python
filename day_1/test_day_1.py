from day_1 import first_and_last_digit

input = open("input.txt", "r").readlines()

def test_first_and_last_digit():
    assert 12 == first_and_last_digit("1abc2")
    assert 15 == first_and_last_digit("a1b2c3d4e5f")
    assert 77 == first_and_last_digit("treb7uchet")

