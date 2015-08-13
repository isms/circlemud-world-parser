# coding: utf-8
import re
import string
import sys
import traceback


def clean_bitvector(bitvector):
    try:
        return int(bitvector)
    except ValueError:
        return bitvector


def bitvector_letter_to_number(letter):
    index = string.ascii_letters.index(letter)
    return 2 ** index


def bitvector_letters_to_numbers(letters):
    for letter in letters:
        yield bitvector_letter_to_number(letter)


def bitvector_number_to_numbers(value):
    bin_string = bin(value)[2:]  # e.g.: 129 -> '10000001'
    for i, v in enumerate(reversed(bin_string)):
        if v == '1':
            yield 2 ** i


def bitvector_to_numbers(value):
    if type(value) == int:
        return list(bitvector_number_to_numbers(value))
    return list(bitvector_letters_to_numbers(value))


def bitvector_to_flags(bitvector, flag_dict):
    numbers = bitvector_to_numbers(bitvector)
    flags = [{'value': number, 'note': flag_dict.get(number, None)}
             for number in numbers]
    return flags


def lookup_value_to_dict(value, flag_dict):
    note = flag_dict.get(value, None)
    return dict(value=value, note=note)


def split_on_vnums(file_text):
    """
    function specifically to split the file on lines like in the form
    of a vnum (e.g. the entire line is something like '#1234'). this is
    important because lines within entries can (and do) start with '#'
    """
    split_re = r"""^\#(\d+)"""
    split_pattern = re.compile(split_re, re.MULTILINE)

    pieces = iter(split_pattern.split(file_text))
    _ = next(pieces)

    while pieces:
        vnum = next(pieces)
        text = next(pieces)
        yield ''.join((vnum, text))


def parse_from_string(file_text, parse_function, splitter):
    """
    given the text of a file, split it up into individual entries using
    the passed splitting function, then feed each piece into the
    individual entry parser, accumulating all results into an array.

     returns the resulting array of dictionaries.
    """
    texts = splitter(file_text)

    dicts = []
    for text in texts:

        try:
            d = parse_function(text)
            dicts.append(d)
        except Exception as e:
            print 'error parsing:', text
            traceback.print_exc(file=sys.stdout)
            return None

    return dicts


def parse_from_file(filename, parse_function, splitter=split_on_vnums):
    """
    given a filename and an individual item parsing function, read the
    file contents and pass to the string parser.
    """
    # read in the file
    with open(filename) as f:
        file_text = f.read().rstrip('$\n')

    return parse_from_string(file_text, parse_function, splitter=splitter)


def parse_dice_roll_string_to_tuple(roll_string):
    """
    given a dice roll string, e.g. 4d6+20, return tuple of number of dice,
    number sides of each die, bonus, e.g. (4, 6, 20)
    """
    dice, bonus = roll_string.split('+')
    n_dice, n_sides = dice.split('d')
    result = map(int, (n_dice, n_sides, bonus))
    return result


def parse_dice_roll_string_to_dict(roll_string):
    """
    given a dice roll string, e.g. 4d6+20, return dict of number of dice,
    number sides of each die, bonus, e.g.:
    {
        "n_dice": 4,
        "n_sides": 6,
        "bonus": 20
    }
    """
    names = ['n_dice', 'n_sides', 'bonus']
    values = parse_dice_roll_string_to_tuple(roll_string)
    return dict(zip(names, values))
