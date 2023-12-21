import re
import operator
from functools import reduce

def first_and_last_digit(line):
    '''
    :param line: the line to extract the calibration value from
    :return: the first and last digit in the line
    '''
    matches = re.findall(r'[0-9]+', line)
    return int("".join([matches[i] for i in (0, -1)]))

def sum_lines(lines):
    '''
    @param lines: A collection of lines containing calibration values
    @return: the sum of all the calibration values in the collection
    '''
    return reduce(operator.add, map(first_and_last_digit, lines))