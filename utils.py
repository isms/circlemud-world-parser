# coding: utf-8
import re
import sys
import traceback


def split(file_text):
    # this is important because some room descriptions can
    # (and do) start with '#'
    split_re = r"""^\#(\d+)"""
    split_pattern = re.compile(split_re, re.MULTILINE)

    pieces = iter(split_pattern.split(file_text))
    _ = next(pieces)

    while pieces:
        vnum = next(pieces)
        text = next(pieces)
        yield ''.join((vnum, text))


def parse_from_string(file_text, parse_function):
    texts = split(file_text)

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


def parse_from_file(filename, parse_function):
    # read in the file
    with open(filename) as f:
        file_text = f.read().rstrip('$\n')

    return parse_from_string(file_text, parse_function)
