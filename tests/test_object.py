# coding: utf-8
from circlemud_world_parser.object import Object
from circlemud_world_parser.utils import parse_from_string
from circlemud_world_parser.utils import split_on_vnums


class TestObjectParsing:
    def test_parsing_objects(self):
        text = """#12020
thunderbolt jupiter~
Jupiter's Thunderbolt~
Jupiter's Thunderbolt has been left here.~
~
5 bgkmn 8193
0 4 6 6
22 100000 25000
A
18 3
A
19 3
#15005
telescope scope~
a large telescope~
There is a large telescope here, pointing at the sky.~
~
12 0 0
0 0 0 0
0 0 0
E
telescope scope~
A small sign says:

Made in Siberia.

~
A
18 2
A
19 2
$
"""
        expected = [
            {
                "weight": 22,
                "wear": [
                    {
                        "value": 1,
                        "note": "WEAR_TAKE"
                    },
                    {
                        "value": 8192,
                        "note": "WEAR_WIELD"
                    }
                ],
                "id": 12020,
                "values": [
                    0,
                    4,
                    6,
                    6
                ],
                "type": {
                    "value": 5,
                    "note": "WEAPON"
                },
                "affects": [
                    {
                        "value": 3,
                        "note": "HITROLL",
                        "location": 18
                    },
                    {
                        "value": 3,
                        "note": "DAMROLL",
                        "location": 19
                    }
                ],
                "aliases": [
                    "thunderbolt",
                    "jupiter"
                ],
                "cost": 100000,
                "extra_descs": [],
                "effects": [
                    {
                        "value": 2,
                        "note": "HUM"
                    },
                    {
                        "value": 64,
                        "note": "MAGIC"
                    },
                    {
                        "value": 1024,
                        "note": "ANTI_EVIL"
                    },
                    {
                        "value": 4096,
                        "note": "ANTI_MAGIC_USER"
                    },
                    {
                        "value": 8192,
                        "note": "ANTI_CLERIC"
                    }
                ],
                "long_desc": "Jupiter's Thunderbolt has been left here.",
                "rent": 25000,
                "short_desc": "Jupiter's Thunderbolt"
            },
            {
                "weight": 0,
                "wear": [],
                "id": 15005,
                "values": [
                    0,
                    0,
                    0,
                    0
                ],
                "type": {
                    "value": 12,
                    "note": "OTHER"
                },
                "affects": [
                    {
                        "value": 2,
                        "note": "HITROLL",
                        "location": 18
                    },
                    {
                        "value": 2,
                        "note": "DAMROLL",
                        "location": 19
                    }
                ],
                "aliases": [
                    "telescope",
                    "scope"
                ],
                "cost": 0,
                "extra_descs": [
                    {
                        "keywords": [
                            "telescope",
                            "scope"
                        ],
                        "desc": "A small sign says:\n\nMade in Siberia.\n"
                    }
                ],
                "effects": [],
                "long_desc": "There is a large telescope here, pointing at the sky.",
                "rent": 0,
                "short_desc": "a large telescope"
            }
        ]

        objs, errors = parse_from_string(text, Object.parse_raw, split_on_vnums)
        assert [obj.model_dump(exclude_none=True) for obj in objs] == expected

    def test_parsing_object_with_non_stock_flag(self):
        text = """#42
thing~
thing~
A thing is here.~
~
5 abcM 8193
0 4 6 6
22 100000 25000
$
"""
        objs, errors = parse_from_string(text, Object.parse_raw, split_on_vnums)
        thing = objs.pop()

        assert len(thing.effects) == 4

        expected = {
            'value': 274877906944,
            'note': None
        }
        effects_as_dicts = [e.model_dump() for e in thing.effects]
        assert expected in effects_as_dicts
