# coding: utf-8
"""
Shops must be in CircleMUD v3.0 format. See "The CircleMUD
Builder's Manual" by Jeremy Elson, Section 7, for an
explanation of the different formats, and how to convert
older Diku-format shops to Circle v3.0.
"""
from constants import OBJECT_TYPE_FLAGS
from constants import SHOP_FLAGS
from constants import SHOP_TRADES_WITH
from utils import bitvector_to_flags
from utils import clean_bitvector


def buy_type_to_dict(line):
    # optional namelist of form "<Buy Type 1 (int)> [Buy Namelist 1 (str)]"
    # ref: "The CircleMUD Builder's Manual," section 7.2

    # at some point (2.x-3.x) the codebase went from `LIQ CONTAINER`` to `DRINKCON`
    # but some shops were not fixed; there are still many references on the web
    # to `LIQ CONTAINER` but this seems like an oversight in some cases and
    # outdated in others
    #
    # as it happens, this also caused a parsing problem because the item type
    # was not expected to have spaces, and `LIQ CONTAINER` was the only type
    # that did have a space in it
    #
    # ref: https://github.com/isms/circlemud-world-parser/issues/1
    if "LIQ CONTAINER" in line:
        line = line.replace("LIQ CONTAINER", "DRINKCON")

    tokens = line.strip().split()
    if len(tokens) == 1:
        item_type = line
        namelist = None
    else:
        item_type = tokens[0]
        namelist = [token.lower() for token in tokens[1:]]

    # lookup the bitvector value from the flag for standardization
    reverse = {v: k for k, v in OBJECT_TYPE_FLAGS.items()}
    value = reverse.get(item_type, None)

    return dict(value=value, note=item_type, namelist=namelist)


def raw_messages_to_dict(messages):
    keys = [
        'buy_fails_object_does_not_exist',
        'sell_fails_object_does_not_exist',
        'sell_fails_shop_does_not_buy_object',
        'sell_fails_shop_cannot_afford_object',
        'buy_fails_player_cannot_afford_object',
        'buy_succeeds',
        'sell_succeeds',
    ]
    messages = [m.lstrip('%s ').rstrip('~') for m in messages]
    return dict(zip(keys, messages))


def times_to_dict(times):
    if not len(times) == 4:
        raise ValueError('Unexpected number of open/close times')

    open_1 = dict(open=times[0], close=times[1])
    open_2 = dict(open=times[2], close=times[3])
    return [open_1, open_2]


def parse_shop(text):
    d = dict()

    fields = [line.rstrip() for line in text.strip().split('\n')]
    delimiters = [i for i, field in enumerate(fields) if field == '-1']

    d['id'] = int(fields[0].lstrip('#').rstrip('~'))

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

    times = [int(t) for t in fields[rooms_stop + 1 :]]
    d['times'] = times_to_dict(times)

    return d
