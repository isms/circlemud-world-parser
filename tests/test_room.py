# coding: utf-8
from circlemud_world_parser.room import Room
from circlemud_world_parser.utils import parse_from_string
from circlemud_world_parser.utils import split_on_vnums


class TestRoomParsing:
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

        rooms, errors = parse_from_string(text, Room.parse_raw, split_on_vnums)
        assert [r.model_dump() for r in rooms] == expected

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
        room = Room.parse_raw(text)
        assert len(room.exits) == 2
