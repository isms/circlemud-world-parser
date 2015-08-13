# coding: utf-8
import unittest

from mob_parser import parse_mob
from object_parser import parse_object
from room_parser import parse_room
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
    def setUp(self):
        self.text = """#12020
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

    def test_parsing_objects(self):
        objs = parse_from_string(self.text, parse_object, split_on_vnums)
        self.assertEqual(len(objs), 2)

        thunderbolt, telescope = objs

        self.assertEqual(thunderbolt['short_desc'], "Jupiter's Thunderbolt")
        self.assertEqual(thunderbolt['long_desc'], "Jupiter's Thunderbolt has been left here.")
        self.assertListEqual(thunderbolt['aliases'], ['thunderbolt', 'jupiter'])

        effects = thunderbolt['extra_effects']
        self.assertEqual(len(effects), 5)

        effect_flags = [effect['note'] for effect in effects]
        expected = ['HUM', 'MAGIC', 'ANTI_EVIL', 'ANTI_MAGIC_USER', 'ANTI_CLERIC']
        self.assertListEqual(effect_flags, expected)

        self.assertEqual(len(thunderbolt['affects']), 2)
        self.assertEqual(len(telescope['affects']), 2)
        self.assertEqual(len(thunderbolt['extra_descs']), 0)
        self.assertEqual(len(telescope['extra_descs']), 1)
        self.assertEqual(len(telescope['extra_descs'][0]['keywords']), 2)

        expected = "A small sign says:\n\nMade in Siberia.\n"
        self.assertEqual(telescope['extra_descs'][0]['desc'], expected)

        self.assertEqual(len(telescope['extra_effects']), 0)
        expected = {
            "note": "ANTI_EVIL",
            "value": 1024
        }
        self.assertIn(expected, thunderbolt['extra_effects'])

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
    def setUp(self):
        self.text = """#3028
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

    def test_parsing_rooms(self):
        rooms = parse_from_string(self.text, parse_room, split_on_vnums)
        self.assertEqual(len(rooms), 2)

        bar, yard = rooms

        self.assertEqual(len(bar['exits']), 2)
        self.assertEqual(len(yard['exits']), 2)

        self.assertEqual(len(bar['extra_descs']), 2)
        self.assertEqual(len(yard['extra_descs']), 0)


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

        expected = ['SPEC', 'SENTINEL', 'MEMORY', 'NOCHARM', 'NOSUMMON']
        actual = [d['note'] for d in mob["action_flags"]]
        self.assertListEqual(actual, expected)

        expected = ['DETECT_INVIS']
        actual = [d['note'] for d in mob["affect_flags"]]
        self.assertListEqual(actual, expected)

        self.assertListEqual(mob["aliases"], ['wizard'])

        self.assertEqual(mob["alignment"], 900)
        self.assertEqual(mob["armor_class"], 2)

        expected = dict(n_dice=2, n_sides=8, bonus=18)
        self.assertEqual(mob["bare_hand_damage"], expected)

        expected = """The wizard looks old and senile, and yet he looks like a very powerful
wizard.  He is equipped with fine clothing, and is wearing many fine
rings and bracelets."""
        self.assertEqual(mob["detail_desc"], expected)

        self.assertDictEqual(mob["extra_spec"], {})

        self.assertEqual(mob["gender"]['note'], 'M')
        self.assertEqual(mob["gold"], 30000)
        self.assertEqual(mob["level"], 33)

        expected = 'A wizard walks around behind the counter, talking to himself.'
        self.assertEqual(mob["long_desc"], expected)

        expected = dict(n_dice=1, n_sides=1, bonus=30000)
        self.assertDictEqual(mob["max_hit_points"], expected)

        self.assertEqual(mob["mob_type"], 'S')
        self.assertEqual(mob["position"]['default']['value'], 8)
        self.assertEqual(mob["position"]['load']['value'], 8)
        self.assertEqual(mob["short_desc"], 'the wizard')
        self.assertEqual(mob["thac0"], 2)
        self.assertEqual(mob["vnum"], 3000)
        self.assertEqual(mob["xp"], 160000)

    def test_parsing_type_e_mob(self):
        e_type = self.text.replace('ablno d 900 S', 'ablno d 900 E')
        e_type += '\nBareHandAttack: 4\nInt: 25\nE'
        mob = parse_from_string(e_type, parse_mob, split_on_vnums).pop()
        expected = dict(BareHandAttack=4, Int=25)
        self.assertDictEqual(mob['extra_spec'], expected)

if __name__ == '__main__':
    unittest.main()
