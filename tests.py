# coding: utf-8
import glob
import os
import unittest

import parse
from mobile import parse_mob
from object import parse_object
from room import parse_room
from shop import parse_shop
from zone import parse_zone
from utils import bitvector_to_numbers
from utils import bitvector_letters_to_numbers
from utils import bitvector_number_to_numbers
from utils import bitvector_to_flags
from utils import parse_from_file
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
    maxDiff = None

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
                "wear_flags": [],
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

        objs, errors = parse_from_string(text, parse_object, split_on_vnums)
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
        objs, errors = parse_from_string(text, parse_object, split_on_vnums)
        thing = objs.pop()

        self.assertEqual(len(thing['effects']), 4)

        expected = {
            'value': 274877906944,
            'note': None
        }
        self.assertIn(expected, thing['effects'])


class RoomParsingTests(unittest.TestCase):
    maxDiff = None

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
                "id": 3028,
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
                "id": 3029,
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

        rooms, errors = parse_from_string(text, parse_room, split_on_vnums)
        self.assertListEqual(rooms, expected)

    def test_room_with_no_exit_description(self):
        text = """3374
A Sloping Tunnel~
   A bright light greets your eyes from the north, in
direct contrast to the darkness of the tunnel overhead.
You break  out in a sweat due to the overwhelming warmth
of the air.  The musky odor has grown quite intense,
drowning out everything else in the air and making it hard
to breathe.  Something in your gut begins squirming
uncomfortably as you wonder what's ahead...
~
33 adgj 4
D0
~
~
0 -1 3375
D4
~
~
0 -1 3373
S"""
        room = parse_room(text)
        self.assertEqual(len(room['exits']), 2)


class MobParsingTests(unittest.TestCase):
    maxDiff = None

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
        mobs, errors = parse_from_string(self.text, parse_mob, split_on_vnums)
        mob = mobs.pop()

        expected = {
            "xp": 160000,
            "id": 3000,
            "thac0": 2,
            "extra_spec": {},
            "detail_desc": "The wizard looks old and senile, and yet he looks like a very powerful\nwizard.  He is equipped with fine clothing, and is wearing many fine\nrings and bracelets.",
            "bare_hand_damage": {
                "sides": 8,
                "dice": 2,
                "bonus": 18
            },
            "armor_class": 2,
            "alignment": 900,
            "aliases": [
                "wizard"
            ],
            "affects": [
                {
                    "value": 8,
                    "note": "DETECT_INVIS"
                }
            ],
            "flags": [
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
                "sides": 1,
                "dice": 1,
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
        mobs, errors = parse_from_string(e_type, parse_mob, split_on_vnums)
        expected = dict(BareHandAttack=4, Int=25)
        self.assertDictEqual(mobs[0]['extra_spec'], expected)


class ZoneParsingTests(unittest.TestCase):
    maxDiff = None

    def test_parsing_zone(self):
        text = """60
Haon-Dor, Light Forest~
6000 6099 13 2
*
* Mobiles
M 0 6000 1 6009         John The Lumberjack
E 1 6000 2 16                   Lumber Axe
E 1 6001 10 5                   Chequered Shirt
M 0 6001 6 6012         Rabbit
G 1 6023 10                     Meat
P 1 1234 1 6023                       Maggot (not a real item)
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

        zone = parse_zone(text)

        expected_mobs = [
            {
                'room': 6009,
                'mob': 6000,
                'max': 1,
                'inventory': [],
                'equipped': [
                    {
                        'id': 6000,
                        'max': 2,
                        'location': 16,
                        'note': 'WIELD',
                        'contents': [],
                    },
                    {
                        'id': 6001,
                        'max': 10,
                        'location': 5,
                        'note': 'BODY',
                        'contents': [],
                    }
                ],
            },
            {
                'room': 6012,
                'mob': 6001,
                'max': 6,
                'inventory': [
                    {
                        'id': 6023,
                        'max': 10,
                        'contents': [
                            {
                                'id': 1234,
                                'max': 1,
                                'contents': [],
                            }
                        ],
                    }
                ],
                'equipped': [],
            }
        ]
        self.assertListEqual(zone['mobs'], expected_mobs)

        expected_objects = [
            {
                'id': 6011,
                'room': 6013,
                'max': 10,
                'contents': [],
            },
            {
                'id': 6017,
                'room': 6026,
                'max': 1,
                'contents': [
                    {
                        'id': 6018,
                        'max': 1,
                        'contents': [],
                    },
                    {
                        'id': 6019,
                        'max': 1,
                        'contents': [],
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
                'id': 6011,
            }
        ]
        self.assertListEqual(zone['remove_objects'], expected_removals)


class ShopParsingTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.text = """#3000~
3050
3051
3052
3053
3054
-1
1.15
0.15
WEAPON [sword & long | short | warhammer | ^golden & bow] & magic
WAND
STAFF
POTION
-1
%s Sorry, I haven't got exactly that item.~
%s You don't seem to have that.~
%s I don't buy such items.~
%s That is too expensive for me!~
%s You can't afford it!~
%s That'll be %d coins, please.~
%s You'll get %d coins for it!~
0
2
3000
2
3033
-1
0
28
0
0"""

    def test_parsing_zone(self):
        expected = {
            'id': 3000,
            'objects': [3050, 3051, 3052, 3053, 3054],
            'sell_rate': 1.15,
            'buy_rate': 0.15,
            'buy_types': [
                {
                    'note': 'WEAPON',
                    'value': 5,
                    'namelist': '[sword & long | short | warhammer | ^golden & bow] & magic'
                },
                {'note': 'WAND', 'value': 3, 'namelist': None},
                {'note': 'STAFF', 'value': 4, 'namelist': None},
                {'note': 'POTION', 'value': 10, 'namelist': None}
            ],
            'messages': {
                'buy_fails_object_does_not_exist': "Sorry, I haven't got exactly that item.",
                'sell_fails_object_does_not_exist': "You don't seem to have that.",
                'sell_fails_shop_does_not_buy_object': "I don't buy such items.",
                'sell_fails_shop_cannot_afford_object': "That is too expensive for me!",
                'buy_fails_player_cannot_afford_object': "You can't afford it!",
                'buy_succeeds': "That'll be %d coins, please.",
                'sell_succeeds': "You'll get %d coins for it!",
            },
            'temper': 0,
            'shopkeeper': 3000,
            'flags': [
                {
                    'value': 2,
                    'note': 'WILL_BANK_MONEY',
                }
            ],
            'trades_with': [
                {
                    'value': 2,
                    'note': 'NOEVIL',
                }
            ],
            'rooms': [3033],
            'times': [
                {
                    'open': 0,
                    'close': 28,
                },
                {
                    'open': 0,
                    'close': 0,
                }
            ]
        }
        shop = parse_shop(self.text)
        self.assertDictEqual(shop, expected)


class TestParsingActualTinyworldFiles(unittest.TestCase):
    def get_all_filenames(self, file_type):
        if file_type not in parse.PARSER_LOOKUP:
            raise KeyError('No parser found for file type: "{}"'.format(file_type))

        caw_path = os.path.join(os.path.abspath('.'), 'assets')
        pattern = os.path.join(caw_path, file_type, '*.' + file_type)
        filenames = glob.glob(pattern)

        return filenames

    def test_parse_all_files(self):
        """
        parse all of the stock CircleMUD files in the CAW archive
        """
        for file_type, args in parse.PARSER_LOOKUP.items():
            filenames = self.get_all_filenames(file_type)

            for filename in filenames:
                payload, errors = parse_from_file(filename, *args)

                if os.path.split(filename)[1] == '0.obj':
                    self.assertEqual(len(errors), 1)
                    expected = '0\nbug~\na bug~\nThis object is BAD!'
                    self.assertIn(expected, errors[0]['text'])
                else:
                    self.assertListEqual(errors, [])


if __name__ == '__main__':
    unittest.main()
