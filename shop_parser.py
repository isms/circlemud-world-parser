# coding: utf-8
import json
import os
import re
import sys

from constants import OBJECT_TYPE_FLAGS
from constants import SHOP_FLAGS
from constants import SHOP_TRADES_WITH
from utils import bitvector_to_flags
from utils import clean_bitvector
from utils import parse_from_file


def buy_type_to_dict(line):
    # optional namelist of form "<Buy Type 1 (int)> [Buy Namelist 1 (str)]"
    # ref: "The CircleMUD Builder's Manual," section 7.2
    try:
        split_index = line.index(' ')
        item_type = line[:split_index]
        namelist = line[split_index + 1:].lower()
    except ValueError:
        item_type = line
        namelist = None

    # lookup the bitvector value from the flag for standardization
    reverse = {v: k for k, v in OBJECT_TYPE_FLAGS.iteritems()}
    value = reverse.get(item_type, None)

    return dict(value=value, note=item_type, namelist=namelist)


def raw_messages_to_dict(messages):
    keys = ['buy_fails_object_does_not_exist', 'sell_fails_object_does_not_exist',
            'sell_fails_shop_does_not_buy_object', 'sell_fails_shop_cannot_afford_object',
            'buy_fails_player_cannot_afford_object', 'buy_succeeds', 'sell_succeeds']

    messages = [m.lstrip('%s ').rstrip('~').replace('%d', '{:d}') for m in messages]
    return dict(zip(keys, messages))


def times_to_dict(times):
    if not len(times) == 4:
        raise ValueError('Unexpected number of open/close times')

    open_1 = dict(open=times[0], close=times[1])
    open_2 = dict(open=times[2], close=times[3])
    return [open_1, open_2]


def parse_shop(text):
    d = {}

    fields = [line.rstrip() for line in text.strip().split('\n')]
    delimiters = [i for i, field in enumerate(fields) if field == '-1']

    d['vnum'] = int(fields[0].lstrip('#').rstrip('~'))

    objects_start, objects_stop = 1, delimiters[0]
    d['objects'] = [int(f) for f in fields[objects_start:objects_stop]]

    d['sell_rate'] = float(fields[objects_stop + 1])
    d['buy_rate'] = float(fields[objects_stop + 2])

    types_start, types_stop = objects_stop + 3, delimiters[1]
    buy_types = [buy_type_to_dict(t) for t in fields[types_start:types_stop]]
    d['buy_types'] = buy_types

    messages_start, messages_stop = delimiters[1] + 1, delimiters[1] + 8
    messages = fields[messages_start:messages_stop]
    d['messages'] = raw_messages_to_dict(messages)

    d['temper'] = int(fields[messages_stop])

    shop_bitvector = clean_bitvector(fields[messages_stop + 1])
    d['flags'] = bitvector_to_flags(shop_bitvector, SHOP_FLAGS)

    d['shopkeeper'] = int(fields[messages_stop + 2])

    trades_with = clean_bitvector(fields[messages_stop + 3])
    d['trades_with'] = bitvector_to_flags(trades_with, SHOP_TRADES_WITH)

    rooms_start, rooms_stop = messages_stop + 4, delimiters[2]
    d['rooms'] = [int(r) for r in fields[rooms_start:rooms_stop]]

    times = [int(t) for t in fields[rooms_stop + 1:]]
    d['times'] = times_to_dict(times)

    return d


if __name__ == '__main__':
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        print('Usage: python object_parser.py [file]')
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as f:
        first_line = f.readline().strip()
        print first_line

    if not first_line == 'CircleMUD v3.0 Shop File~':
        error = 'Shops must be in CircleMUD v3.0 format. See "The CircleMUD ' \
                'Builder\'s Manual" by Jeremy Elson, Section 7, for an ' \
                'explanation of the different formats, and how to convert ' \
                'older Diku-format shops to Circle v3.0.'
        raise NotImplementedError(error)

    dicts = parse_from_file(filename, parse_shop)
    payload = json.dumps(dicts, indent=2, sort_keys=True)
    print(payload)
