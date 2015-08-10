# coding: utf-8
import string


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
    flags = [{'value': number,'flag': flag_dict.get(number, None)}
             for number in numbers]
    return flags
