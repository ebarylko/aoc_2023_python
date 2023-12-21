import re

def first_and_last_digit(line):
    '''
    :param line: the line to extract the first and last digit from
    :return: the first and last digit in line
    '''
    matches = re.findall(r'[0-9]+', line)
    return int("".join([matches[i] for i in (0, -1)]))