# coding: utf-8
from constants import OBJECT_AFFECT_LOCATION_FLAGS
from constants import OBJECT_EXTRA_EFFECTS_FLAGS
from constants import OBJECT_TYPE_FLAGS
from constants import OBJECT_WEAR_FLAGS
from utils import bitvector_to_flags
from utils import clean_bitvector
from utils import lookup_value_to_dict


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

                yield dict(keywords=keywords, desc=desc)

        except StopIteration:
            break


def parse_affects(extra_fields):
    extra_iterator = iter(extra_fields)

    while True:
        try:
            new = next(extra_iterator)

            if new == 'A':
                loc, value = [int(v) for v in next(extra_iterator).split()]
                note = OBJECT_AFFECT_LOCATION_FLAGS.get(loc, None)
                yield dict(location=loc, note=note, value=value)

        except StopIteration:
            break


def parse_object(text):
    fields = [line.rstrip() for line in text.strip().split('\n')]

    d = dict()

    # easy fields
    d['id'] = int(fields[0])
    d['aliases'] = fields[1].rstrip('~').split()
    d['short_desc'] = fields[2].rstrip('~')
    d['long_desc'] = fields[3].rstrip('~')
    d['values'] = [int(v) for v in fields[6].split()]
    weight, cost, rent = [int(v) for v in fields[7].split()]
    d['weight'] = weight
    d['cost'] = cost
    d['rent'] = rent

    type_flag, effects_bits, wear_bitvector = fields[5].split()

    # type flag is always an int
    d['type'] = lookup_value_to_dict(int(type_flag), OBJECT_TYPE_FLAGS)

    # parse the bitvectors
    effects_bits = clean_bitvector(effects_bits)
    effects = bitvector_to_flags(effects_bits, OBJECT_EXTRA_EFFECTS_FLAGS)
    d['effects'] = effects

    wear_bitvector = clean_bitvector(wear_bitvector)
    d['wear'] = bitvector_to_flags(wear_bitvector, OBJECT_WEAR_FLAGS)

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
