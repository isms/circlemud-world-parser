# coding: utf-8
import json
import os
import sys

from constants import OBJECT_AFFECT_LOCATION_FLAGS
from constants import OBJECT_EXTRA_EFFECTS_FLAGS
from constants import OBJECT_TYPE_FLAGS
from constants import OBJECT_WEAR_FLAGS
from utils import bitvector_to_flags
from utils import clean_bitvector
from utils import lookup_value_to_dict
from utils import parse_from_file


def parse_extra_descs(extra_fields):
    extra_iterator = iter(extra_fields)

    while True:
        try:
            new = next(extra_iterator)

            if new == 'E':

                keywords = next(extra_iterator).rstrip('~').split()
                new = next(extra_iterator)

                desc_lines = []
                while new not in ('~', '$'):
                    desc_lines.append(new)
                    new = next(extra_iterator)
                desc = '\n'.join(desc_lines)

                yield {'keywords': keywords, 'desc': desc}

        except StopIteration:
            break


def parse_affects(extra_fields):
    extra_iterator = iter(extra_fields)

    while True:
        try:
            new = next(extra_iterator)

            if new == 'A':
                location, value = map(int, next(extra_iterator).split())
                flag = OBJECT_AFFECT_LOCATION_FLAGS.get(location, None)
                d = {
                    'location': location,
                    'note': flag,
                    'value': value,
                }
                yield d

        except StopIteration:
            break


def parse_object(text):
    fields = [line.rstrip() for line in text.strip().split('\n')]

    d = {}

    # easy fields
    d['vnum'] = int(fields[0])
    d['aliases'] = fields[1].rstrip('~').split()
    d['short_desc'] = fields[2].rstrip('~')
    d['long_desc'] = fields[3].rstrip('~')
    d['values'] = map(int, fields[6].split())
    d['weight'], d['cost'], d['rent_per_day'] = map(int, fields[7].split())

    type_flag, extra_effects_bitvector, wear_bitvector = fields[5].split()

    # type flag is always an int
    d['type'] = lookup_value_to_dict(int(type_flag), OBJECT_TYPE_FLAGS)

    # parse the bitvectors
    extra_effects_bitvector = clean_bitvector(extra_effects_bitvector)
    extra_effects = bitvector_to_flags(extra_effects_bitvector, OBJECT_EXTRA_EFFECTS_FLAGS)
    d['extra_effects'] = extra_effects

    wear_bitvector = clean_bitvector(wear_bitvector)
    d['wear_flags'] = bitvector_to_flags(wear_bitvector, OBJECT_WEAR_FLAGS)

    action_desc = fields[4].rstrip('~')
    if action_desc:
        d['action_desc'] = action_desc

    d['affects'] = []
    d['extra_descs'] = []
    if len(fields) > 8:
        extra_fields = fields[8:]

        d['affects'] = list(parse_affects(extra_fields))
        d['extra_descs'] = list(parse_extra_descs(extra_fields))

    return d


if __name__ == '__main__':
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        print('Usage: python object_parser.py [file]')
        sys.exit(1)

    filename = sys.argv[1]
    dicts = parse_from_file(filename, parse_object)
    payload = json.dumps(dicts, indent=2, sort_keys=True)
    print(payload)
