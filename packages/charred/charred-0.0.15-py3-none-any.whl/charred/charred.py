"""

author: @endormi

Very simple char functions

"""


def is_same_char(char):
    return all(c == char[0] for c in char[1:])


def repeat_char(char, num_of_times):
    return (char * (num_of_times//len(char) + 1))[:num_of_times]
