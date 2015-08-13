# coding: utf-8
import json
import os
import sys
import traceback

from bitvectors import bitvector_to_flags
from bitvectors import clean_bitvector
from constants import OBJECT_AFFECT_LOCATION_FLAGS
from constants import OBJECT_EXTRA_EFFECTS_FLAGS
from constants import OBJECT_TYPE_FLAGS
from constants import OBJECT_WEAR_FLAGS


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


def parse_object(object_text):
    fields = object_text.strip().split('\n')

    try:
        item = {}

        # easy fields
        item['vnum'] = int(fields[0])
        item['aliases'] = fields[1].rstrip('~').split()
        item['short_desc'] = fields[2].rstrip('~')
        item['long_desc'] = fields[3].rstrip('~')
        item['values'] = map(int, fields[6].split())
        item['weight'], item['cost'], item['rent_per_day'] = map(int, fields[7].split())

        type_flag, extra_effects_bitvector, wear_bitvector = fields[5].split()

        # type flag is always an int
        item['type'] = {
            'value': int(type_flag),
            'note': OBJECT_TYPE_FLAGS.get(int(type_flag), None)
        }

        # parse the bitvectors
        extra_effects_bitvector = clean_bitvector(extra_effects_bitvector)
        extra_effects = bitvector_to_flags(extra_effects_bitvector, OBJECT_EXTRA_EFFECTS_FLAGS)
        item['extra_effects'] = extra_effects

        wear_bitvector = clean_bitvector(wear_bitvector)
        item['wear_flags'] = bitvector_to_flags(wear_bitvector, OBJECT_WEAR_FLAGS)

        action_desc = fields[4].rstrip('~')
        if action_desc:
            item['action_desc'] = action_desc

        item['affects'] = []
        item['extra_descs'] = []
        if len(fields) > 8:
            extra_fields = fields[8:]

            item['affects'] = list(parse_affects(extra_fields))
            item['extra_descs'] = list(parse_extra_descs(extra_fields))

    except Exception as e:
        print 'error parsing item:', object_text
        traceback.print_exc(file=sys.stdout)
        return None

    return item


def parse_objects_from_string(file_text):
    # ignore short artifacts
    object_texts = [t for t in file_text.split('#')
                    if t and t != '$\n']

    objects = []
    for obj_text in object_texts:
        obj = parse_object(obj_text)
        if obj:
            objects.append(obj)

    return objects


def parse_objects_from_file(obj_filename):
    # read in the file
    with open(obj_filename) as f:
        file_text = f.read()

    return parse_objects_from_string(file_text)


if __name__ == '__main__':
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        print('Usage: python object_parser.py [file]')
        sys.exit(1)

    filename = sys.argv[1]
    dicts = parse_objects_from_file(filename)
    payload = json.dumps(dicts, indent=2, sort_keys=True)
    print(payload)
