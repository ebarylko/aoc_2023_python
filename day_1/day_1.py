import re
import operator
from functools import reduce
from toolz import *
import toolz.functoolz as tfz

word_to_number = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

def to_number(digit):
    return int(digit) if digit.isdigit() else word_to_number[digit]

def first_number(coll):
    """
    @param coll: a collection of numbers
    @return: the first number in the collection
    """
    return tfz.thread_last(
        coll,
        first,
        to_number
    )

def last_number(coll):
    """
    @param coll: a collection of numbers
    @return: the last number in the collection
    """
    return tfz.thread_last(
        coll,
        last,
        to_number
    )

def first_and_last(coll):
    """
    @param coll: a collection of numbers
    @return: the first and last number in the collection
    """
    return tfz.juxt(first_number, last_number)(coll)

def join_digits(digits):
    """
    @param digits: the first and last digits in a line
    @return: the calibration value for the line
    """
    first, last = digits
    return first * 10 + last

def first_and_last_digit(line):
    """
    @param line: the line to extract the calibration value from
    @return: the first and last digit in the line
    """
    return tfz.thread_last(
        line,
        (re.findall, r'(?=(\d|zero|one|two|three|four|five|six|seven|eight|nine))'),
        first_and_last,
        join_digits
    )

def sum_lines(lines):
    """
    @param lines: A collection of lines containing calibration values
    @return: the sum of all the calibration values in the collection
    """
    return tfz.thread_last(
        lines,
        (map, first_and_last_digit),
        (reduce, operator.add))