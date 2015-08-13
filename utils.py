# coding: utf-8
import re


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
        d = parse_function(text)
        dicts.append(d)

    return dicts


def parse_from_file(filename, parse_function):
    # read in the file
    with open(filename) as f:
        file_text = f.read().rstrip('$\n')

    return parse_from_string(file_text, parse_function)
