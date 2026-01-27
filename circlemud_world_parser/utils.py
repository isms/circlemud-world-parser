import re
import string
import traceback
from collections.abc import Callable, Iterator
from enum import IntEnum, IntFlag
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypedDict

if TYPE_CHECKING:
    from .models import Flag


class FlagDict(TypedDict):
    """Dictionary representing a parsed flag."""

    value: int
    note: str | None


type FlagEnum = type[IntEnum] | type[IntFlag]


class ErrorDict(TypedDict):
    """Dictionary representing a parsing error."""

    text: str
    trace: str


def clean_bitvector(bitvector: str) -> int | str:
    """Convert bitvector to int if numeric, otherwise return as-is."""
    try:
        return int(bitvector)
    except ValueError:
        return bitvector


def bitvector_letter_to_number(letter: str) -> int:
    """Convert a bitvector letter (a-zA-Z) to its numeric value."""
    index = string.ascii_letters.index(letter)
    return 2**index


def bitvector_letters_to_numbers(letters: str) -> Iterator[int]:
    """Convert bitvector letters to their numeric values."""
    for letter in letters:
        yield bitvector_letter_to_number(letter)


def bitvector_number_to_numbers(value: int) -> Iterator[int]:
    """Decompose a bitvector number into its component powers of 2."""
    bin_string = bin(value)[2:]  # e.g.: 129 -> '10000001'
    for i, v in enumerate(reversed(bin_string)):
        if v == '1':
            yield 2**i


def bitvector_to_numbers(value: int | str) -> list[int]:
    """Convert a bitvector (numeric or letter-based) to list of flag values."""
    if isinstance(value, int):
        return list(bitvector_number_to_numbers(value))
    return list(bitvector_letters_to_numbers(value))


def _lookup_enum(value: int, enum_cls: FlagEnum) -> str | None:
    """Look up a value in an IntEnum/IntFlag class, returning its name or None."""
    try:
        return enum_cls(value).name
    except ValueError:
        return None


def bitvector_to_flags(bitvector: int | str, enum_cls: FlagEnum) -> list[FlagDict]:
    """Convert a bitvector to a list of flag dictionaries with values and notes."""
    numbers = bitvector_to_numbers(bitvector)
    flags: list[FlagDict] = [
        {'value': number, 'note': _lookup_enum(number, enum_cls)} for number in numbers
    ]
    return flags


def parse_flags(raw_bitvector: str, enum_cls: FlagEnum) -> list["Flag"]:
    """Parse a raw bitvector string into a list of Flag objects.

    Combines clean_bitvector, bitvector_to_flags, and Flag creation into one step.
    """
    from .models import Flag  # Import here to avoid circular imports

    cleaned = clean_bitvector(raw_bitvector)
    flag_dicts = bitvector_to_flags(cleaned, enum_cls)
    return [Flag(**f) for f in flag_dicts]


def lookup_value_to_dict(value: int, enum_cls: FlagEnum) -> FlagDict:
    """Look up a single value in an enum class and return as FlagDict."""
    note = _lookup_enum(value, enum_cls)
    return {'value': value, 'note': note}


def split_on_vnums(file_text: str) -> Iterator[str]:
    """
    Split the file on lines in the form of a vnum (e.g. '#1234').

    This is important because lines within entries can (and do) start with '#'.
    """
    pattern = re.compile(r'^#(\d+)', re.MULTILINE)
    pieces = pattern.split(file_text)
    for vnum, text in zip(pieces[1::2], pieces[2::2]):
        yield vnum + text


def parse_from_string(
    file_text: str,
    parse_function: Callable[[str], Any],
    splitter: Callable[[str], Iterator[str]],
) -> tuple[list[Any], list[ErrorDict]]:
    """
    Split file text into entries and parse each one.

    Returns a tuple of (parsed_items, errors).
    """
    texts = splitter(file_text)

    dicts: list[Any] = []
    errors: list[ErrorDict] = []

    for text in texts:
        try:
            d = parse_function(text)
            dicts.append(d)
        except Exception:  # intentionally broad
            trace = traceback.format_exc()
            error: ErrorDict = {'text': text, 'trace': trace}
            errors.append(error)

    return dicts, errors


def parse_from_file(
    filename: str | Path,
    parser: Callable[[str], Any],
    splitter: Callable[[str], Iterator[str]] = split_on_vnums,
    validate: Callable[[str], None] | None = None,
) -> tuple[list[Any], list[ErrorDict]]:
    """
    Parse a CircleMUD world file.

    Reads the file, optionally validates it, and parses entries.
    """
    with open(filename) as f:
        file_text = f.read()

    if validate:
        validate(file_text)

    file_text = file_text.rstrip('$\n')  # world files
    file_text = file_text.rstrip('$~\n')  # shop files

    return parse_from_string(file_text, parser, splitter=splitter)
