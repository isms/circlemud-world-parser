# coding: utf-8
from circlemud_world_parser.zone import parse_zone


class TestZoneParsing:
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
        assert zone['mobs'] == expected_mobs

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
        assert zone['objects'] == expected_objects

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
        assert zone['doors'] == expected_doors

        expected_removals = [
            {
                'room': 6016,
                'id': 6011,
            }
        ]
        assert zone['remove_objects'] == expected_removals
