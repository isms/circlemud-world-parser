# coding: utf-8
import re
import string
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


def lookup_note_to_dict(note, flag_dict):
    reverse_dict = {v: k for k, v in flag_dict.items()}
    value = reverse_dict.get(note, None)
    return dict(value=value, note=note)


def split_on_vnums(file_text):
    """
    function specifically to split the file on lines in the form
    of a vnum (e.g. the entire line is something like '#1234'). this is
    important because lines within entries can (and do) start with '#'
    """
    split_re = r"""^\#(\d+)"""
    split_pattern = re.compile(split_re, re.MULTILINE)

    pieces = iter(split_pattern.split(file_text))
    next(pieces)  # burn the next one, we won't use it

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
    errors = []

    for text in texts:

        try:
            d = parse_function(text)
            dicts.append(d)
        except Exception:  # intentionally broad
            trace = traceback.format_exc()
            error = dict(text=text, trace=trace)
            errors.append(error)

    return dicts, errors


def parse_from_file(filename, parser, splitter=split_on_vnums, validate=None):
    """
    given a filename and an individual item parsing function, read the
    file contents and pass to the string parser.
    """
    with open(filename) as f:
        file_text = f.read()

    if validate:
        validate(file_text)

    file_text = file_text.rstrip('$\n')  # world files
    file_text = file_text.rstrip('$~\n')  # shop files

    return parse_from_string(file_text, parser, splitter=splitter)
