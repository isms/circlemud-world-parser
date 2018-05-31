# coding: utf-8
import re

from src.constants import ROOM_DOOR_FLAGS
from src.constants import ROOM_FLAGS
from src.constants import ROOM_SECTOR_TYPES
from src.utils import bitvector_to_flags
from src.utils import clean_bitvector
from src.utils import lookup_value_to_dict

EXIT_RE = r"""D(\d+)
(.*?)~
(.*?)~
(.*?)
"""
EXIT_PATTERN = re.compile(EXIT_RE, re.DOTALL | re.MULTILINE)

EXTRA_DESC_RE = r"""E
(.*?)~
(.*?)
~"""
EXTRA_DESC_PATTERN = re.compile(EXTRA_DESC_RE, re.DOTALL)


def parse_exits(text):
    exits = []

    matches = EXIT_PATTERN.findall(text)
    for match in matches:
        direction, desc, keys, other = match
        desc = desc.rstrip('\n')
        flag, key_num, to = other.strip().split()

        exit = dict()
        exit['dir'] = int(direction)
        exit['desc'] = desc
        exit['keywords'] = keys.split()
        exit['key_number'] = int(key_num)
        exit['room_linked'] = int(to)
        exit['door_flag'] = {
            'value': int(flag),
            'note': ROOM_DOOR_FLAGS.get(int(flag), None)
        }
        exits.append(exit)

    return exits


def parse_extra_descs(text):
    extra_descs = []
    for keywords, desc in EXTRA_DESC_PATTERN.findall(text):
        extra_desc = dict(keywords=keywords.split(), desc=desc)
        extra_descs.append(extra_desc)
    return extra_descs


def parse_room(text):
    parts = text.split('~')
    vnum, name = parts[0].split('\n')
    desc = parts[1].strip()
    zone, flags, sector = parts[2].strip() \
        .split('\n')[0].strip().split(' ')

    d = dict()
    d['id'] = int(vnum)
    d['name'] = name.strip()
    d['desc'] = desc.strip('\n')
    d['zone_number'] = int(zone)

    flags = clean_bitvector(flags)
    d['flags'] = []
    if flags:
        d['flags'] = bitvector_to_flags(flags, ROOM_FLAGS)

    # sector type flag is always an int
    d['sector_type'] = lookup_value_to_dict(int(sector), ROOM_SECTOR_TYPES)

    bottom_matter = '~'.join(parts[2:])
    d['exits'] = parse_exits(bottom_matter)
    d['extra_descs'] = parse_extra_descs(bottom_matter)

    return d
