import re
import operator
from functools import reduce
from toolz import *

word_to_number = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

def to_number(digit):
    return int(digit) if digit.isdigit() else word_to_number[digit]

def convert_all_digits_to_numerical_digits(coll):
    """
    @param coll: a collection of word and numerical digits
    @return: the original collection after converting the word digits to their numerical equivalent
    """
    return map(to_number, coll)

def first_and_last_digit(line):
    """
    @param line: the line to extract the calibration value from
    @return: the first and last digit in the line
    """
    matches = re.findall(r'(?=(\d|zero|one|two|three|four|five|six|seven|eight|nine))', line)
    return pipe(matches, lambda m: [to_number(m[i]) for i in (0, -1)], lambda coll: coll[0] * 10 + coll[1])

def sum_lines(lines):
    '''
    @param lines: A collection of lines containing calibration values
    @return: the sum of all the calibration values in the collection
    '''
    return reduce(operator.add, map(first_and_last_digit, lines))