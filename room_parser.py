# coding: utf-8
import json
import re
import os
import sys
import traceback

from bitvectors import bitvector_to_flags
from bitvectors import clean_bitvector
from constants import ROOM_DOOR_FLAGS
from constants import ROOM_FLAGS
from constants import ROOM_SECTOR_TYPES


# ROOM_RE = r"""^\#(\d+)
# (.*?)~
# (.*?)
# ~
# (\S+?) (\S+?)\ (\S+?)
# (.*?)
# S"""

EXIT_RE = r"""D(\d+)
(.*?)
~
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

        flag, key_num, to = other.strip().split()
        exit = {}
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

def parse_room(room_text):
   
    try:
        parts = room_text.split('~')
        vnum, name = parts[0].split('\n')
        desc = parts[1].strip()
        zone, flags, sector = parts[2].strip() \
            .split('\n')[0].strip().split(' ')
        extra_string = parts[2]
        
        room = {}
        room['vnum'] = int(vnum)
        room['name'] = name.strip()
        room['desc'] = desc.strip('\n')
        room['zone_number'] = int(zone)
        
        flags = clean_bitvector(flags)
        room['flags'] = []
        if flags:
            room['flags'] = bitvector_to_flags(flags, ROOM_FLAGS)
      
        # sector type flag is always an int
        room['sector_type'] = {
            'value': int(sector),
            'note': ROOM_SECTOR_TYPES.get(int(sector), None),
        }
        
        bottom_matter = '~'.join(parts[2:])
        room['exits'] = parse_exits(bottom_matter)
        room['extra_descs'] = parse_extra_descs(bottom_matter)
        
        
    except Exception as e:
        print 'error parsing room:', room_text
        traceback.print_exc(file=sys.stdout)
        return None
        
    return room

def split_rooms(file_text):
    # this is important because some room descriptions can
    # (and do) start with '#'
    split_re = r"""^\#(\d+)"""
    split_pattern = re.compile(split_re)

    split_re = r"""^\#(\d+)"""
    split_pattern = re.compile(split_re, re.MULTILINE)

    pieces = iter(split_pattern.split(file_text))
    _ = next(pieces)

    while pieces:
        vnum = next(pieces)
        text = next(pieces)
        yield ''.join((vnum, text))

def parse_rooms_from_string(file_text):
    room_texts = split_rooms(file_text)
    
    rooms = []
    for room_text in room_texts:
        room = parse_room(room_text)
        rooms.append(room)
    
    return rooms

def parse_rooms_from_file(wld_filename):
    # read in the file
    with open(wld_filename) as f:
        file_text = f.read()

    return parse_rooms_from_string(file_text)


if __name__ == '__main__':
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        print('Usage: python object_parser.py [file]')
        sys.exit(1)

    objects = parse_objects_from_file(sys.argv[1])
    payload = json.dumps(objects, indent=2, sort_keys=True)
    print(payload)
