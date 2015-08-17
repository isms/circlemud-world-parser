# coding: utf-8
import unittest

from mob_parser import parse_mob
from object_parser import parse_object
from room_parser import parse_room
from zone_parser import parse_zone
from utils import bitvector_to_numbers
from utils import bitvector_letters_to_numbers
from utils import bitvector_number_to_numbers
from utils import bitvector_to_flags
from utils import parse_from_string
from utils import split_on_vnums


class BitvectorParsingTests(unittest.TestCase):
    def test_bitvector_number_to_numbers(self):
        bitvector = 8193
        expected = [1, 8192]
        actual = list(bitvector_number_to_numbers(8193))
        self.assertListEqual(actual, expected)

        actual = list(bitvector_to_numbers(bitvector))
        self.assertListEqual(actual, expected)

    def test_bitvector_letters_to_numbers(self):
        bitvector = 'adjmnoq'
        expected = [1, 8, 512, 4096, 8192, 16384, 65536]
        actual = list(bitvector_letters_to_numbers(bitvector))
        self.assertListEqual(actual, expected)

        actual = list(bitvector_to_numbers(bitvector))
        self.assertListEqual(actual, expected)

    def test_bitvector_to_flags(self):
        test_flags = {
            1: 'GLOWING',
            2: 'BUZZING',
            4: 'OOZING',
            8: 'BUBBLING'
        }

        bitvector = 6
        expected = [
            {"note": "BUZZING", "value": 2},
            {"note": "OOZING", "value": 4}
        ]
        actual = bitvector_to_flags(bitvector, test_flags)
        self.assertListEqual(actual, expected)


class ObjectParsingTests(unittest.TestCase):
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
                "wear_flags": [
                    {
                        "value": 1,
                        "note": "WEAR_TAKE"
                    },
                    {
                        "value": 8192,
                        "note": "WEAR_WIELD"
                    }
                ],
                "vnum": 12020,
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
                "extra_effects": [
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
                "rent_per_day": 25000,
                "short_desc": "Jupiter's Thunderbolt"
            },
            {
                "weight": 0,
                "wear_flags": [],
                "vnum": 15005,
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
                "extra_effects": [],
                "long_desc": "There is a large telescope here, pointing at the sky.",
                "rent_per_day": 0,
                "short_desc": "a large telescope"
            }
        ]

        objs = parse_from_string(text, parse_object, split_on_vnums)
        self.assertEqual(objs, expected)

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
        objs = parse_from_string(text, parse_object, split_on_vnums)
        thing = objs.pop()

        self.assertEqual(len(thing['extra_effects']), 4)

        expected = {
            'value': 274877906944,
            'note': None
        }
        self.assertIn(expected, thing['extra_effects'])


class RoomParsingTests(unittest.TestCase):
    def test_parsing_rooms(self):
        text = """#3028
The Thieves' Bar~
   The bar of the thieves.  Once upon a time this place was beautifully
furnished, but now it seems almost empty.  To the south is the yard, and to
the west is the entrance hall.
   (Maybe the furniture has been stolen?!)
~
30 cdh 0
D2
You see the secret yard.
~
~
0 -1 3029
D3
You see the entrance hall to the thieves' guild.
~
~
0 -1 3027
E
furniture~
As you look at the furniture, the chair you sit on disappears.
Also with multiple lines.
~
E
other~
A different thing.
~
S
#3029
The Secret Yard~
   The secret practice yard of thieves and assassins.  To the north is the
bar.  A well leads down into darkness.
~
30 cd 0
D0
You see the bar.
~
~
0 -1 3028
D5
You can't see what is down there, it is too dark.  Looks like it would be
impossible to climb back up.
~
~
0 -1 7043
S
"""
        expected = [
            {
                "zone_number": 30,
                "vnum": 3028,
                "sector_type": {
                    "value": 0,
                    "note": "INSIDE"
                },
                "name": "The Thieves' Bar",
                "flags": [
                    {
                        "value": 4,
                        "note": "NOMOB"
                    },
                    {
                        "value": 8,
                        "note": "INDOORS"
                    },
                    {
                        "value": 128,
                        "note": "NOMAGIC"
                    }
                ],
                "extra_descs": [
                    {
                        "keywords": [
                            "furniture"
                        ],
                        "desc": "As you look at the furniture, the chair you sit on disappears.\nAlso with multiple lines."
                    },
                    {
                        "keywords": [
                            "other"
                        ],
                        "desc": "A different thing."
                    }
                ],
                "exits": [
                    {
                        "room_linked": 3029,
                        "keywords": [],
                        "key_number": -1,
                        "door_flag": {
                            "value": 0,
                            "note": "NO_DOOR"
                        },
                        "dir": 2,
                        "desc": "You see the secret yard."
                    },
                    {
                        "room_linked": 3027,
                        "keywords": [],
                        "key_number": -1,
                        "door_flag": {
                            "value": 0,
                            "note": "NO_DOOR"
                        },
                        "dir": 3,
                        "desc": "You see the entrance hall to the thieves' guild."
                    }
                ],
                "desc": "The bar of the thieves.  Once upon a time this place was beautifully\nfurnished, but now it seems almost empty.  To the south is the yard, and to\nthe west is the entrance hall.\n   (Maybe the furniture has been stolen?!)"
            },
            {
                "zone_number": 30,
                "vnum": 3029,
                "sector_type": {
                    "value": 0,
                    "note": "INSIDE"
                },
                "name": "The Secret Yard",
                "flags": [
                    {
                        "value": 4,
                        "note": "NOMOB"
                    },
                    {
                        "value": 8,
                        "note": "INDOORS"
                    }
                ],
                "extra_descs": [],
                "exits": [
                    {
                        "room_linked": 3028,
                        "keywords": [],
                        "key_number": -1,
                        "door_flag": {
                            "value": 0,
                            "note": "NO_DOOR"
                        },
                        "dir": 0,
                        "desc": "You see the bar."
                    },
                    {
                        "room_linked": 7043,
                        "keywords": [],
                        "key_number": -1,
                        "door_flag": {
                            "value": 0,
                            "note": "NO_DOOR"
                        },
                        "dir": 5,
                        "desc": "You can't see what is down there, it is too dark.  Looks like it would be\nimpossible to climb back up."
                    }
                ],
                "desc": "The secret practice yard of thieves and assassins.  To the north is the\nbar.  A well leads down into darkness."
            }
        ]

        rooms = parse_from_string(text, parse_room, split_on_vnums)
        self.assertListEqual(rooms, expected)


class MobParsingTests(unittest.TestCase):
    def setUp(self):
        self.text = """#3000
wizard~
the wizard~
A wizard walks around behind the counter, talking to himself.
~
The wizard looks old and senile, and yet he looks like a very powerful
wizard.  He is equipped with fine clothing, and is wearing many fine
rings and bracelets.
~
ablno d 900 S
33 2 2 1d1+30000 2d8+18
30000 160000
8 8 1"""

    def test_parsing_type_s_mob(self):
        mob = parse_from_string(self.text, parse_mob, split_on_vnums).pop()

        expected = {
            "xp": 160000,
            "vnum": 3000,
            "thac0": 2,
            "extra_spec": {},
            "detail_desc": "The wizard looks old and senile, and yet he looks like a very powerful\nwizard.  He is equipped with fine clothing, and is wearing many fine\nrings and bracelets.",
            "bare_hand_damage": {
                "n_sides": 8,
                "n_dice": 2,
                "bonus": 18
            },
            "armor_class": 2,
            "alignment": 900,
            "aliases": [
                "wizard"
            ],
            "affect_flags": [
                {
                    "value": 8,
                    "note": "DETECT_INVIS"
                }
            ],
            "action_flags": [
                {
                    "value": 1,
                    "note": "SPEC"
                },
                {
                    "value": 2,
                    "note": "SENTINEL"
                },
                {
                    "value": 2048,
                    "note": "MEMORY"
                },
                {
                    "value": 8192,
                    "note": "NOCHARM"
                },
                {
                    "value": 16384,
                    "note": "NOSUMMON"
                }
            ],
            "gender": {
                "value": 1,
                "note": "M"
            },
            "gold": 30000,
            "level": 33,
            "long_desc": "A wizard walks around behind the counter, talking to himself.",
            "max_hit_points": {
                "n_sides": 1,
                "n_dice": 1,
                "bonus": 30000
            },
            "mob_type": "S",
            "position": {
                "load": {
                    "value": 8,
                    "note": "POSITION_STANDING"
                },
                "default": {
                    "value": 8,
                    "note": "POSITION_STANDING"
                }
            },
            "short_desc": "the wizard"
        }
        self.assertEqual(mob, expected)

    def test_parsing_type_e_mob(self):
        e_type = self.text.replace('ablno d 900 S', 'ablno d 900 E')
        e_type += '\nBareHandAttack: 4\nInt: 25\nE'
        mob = parse_from_string(e_type, parse_mob, split_on_vnums).pop()
        expected = dict(BareHandAttack=4, Int=25)
        self.assertDictEqual(mob['extra_spec'], expected)


class ZoneParsingTests(unittest.TestCase):
    def setUp(self):
        self.text = """60
Haon-Dor, Light Forest~
6000 6099 13 2
*
* Mobiles
M 0 6000 1 6009         John The Lumberjack
E 1 6000 2 16                   Lumber Axe
E 1 6001 10 5                   Chequered Shirt
M 0 6001 6 6012         Rabbit
G 1 6023 10                     Meat
* Objects
O 0 6011 10 6013        Mushroom
R 0 6016 6011
O 0 6017 1 6026         Corpse Of The Boar
P 1 6018 1 6017                 Meat
P 1 6019 1 6017                 Tusks
* Doors
D 0 6009 0 1            Cabin
D 0 6010 2 1
*
S"""

    def test_parsing_zone(self):
        zone = parse_zone(self.text)

        expected_mobs = [
            {
                'room': 6009,
                'mob': 6000,
                'max': 1,
                'inventory': [],
                'equipped': [
                    {
                        'object': 6000,
                        'max': 2,
                        'location': 16,
                        'note': 'WIELD',
                    },
                    {
                        'object': 6001,
                        'max': 10,
                        'location': 5,
                        'note': 'BODY',
                    }
                ],
            },
            {
                'room': 6012,
                'mob': 6001,
                'max': 6,
                'inventory': [
                    {
                        'object': 6023,
                        'max': 10,
                    }
                ],
                'equipped': [],
            }
        ]
        self.assertListEqual(zone['mobs'], expected_mobs)

        expected_objects = [
            {
                'object': 6011,
                'room': 6013,
                'max': 10,
                'contents': [],
            },
            {
                'object': 6017,
                'room': 6026,
                'max': 1,
                'contents': [
                    {
                        'object': 6018,
                        'max': 1,
                    },
                    {
                        'object': 6019,
                        'max': 1,
                    }
                ],
            },
        ]
        self.assertListEqual(zone['objects'], expected_objects)

        expected_doors = [
            {
                'room': 6009,
                'exit': 0,
                'state': 1,
            },
            {
                'room': 6010,
                'exit': 2,
                'state': 1,
            }
        ]
        self.assertListEqual(zone['doors'], expected_doors)

        expected_removals = [
            {
                'room': 6016,
                'object': 6011,
            }
        ]
        self.assertListEqual(zone['remove_objects'], expected_removals)


if __name__ == '__main__':
    unittest.main()
