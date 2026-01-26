# coding: utf-8
import pytest

from circlemud_world_parser.mobile import parse_mob
from circlemud_world_parser.utils import parse_from_string
from circlemud_world_parser.utils import split_on_vnums


class TestMobParsing:
    @pytest.fixture
    def mob_text(self):
        return """#3000
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

    def test_parsing_type_s_mob(self, mob_text):
        mobs, errors = parse_from_string(mob_text, parse_mob, split_on_vnums)
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
        assert mob == expected

    def test_parsing_type_e_mob(self, mob_text):
        e_type = mob_text.replace('ablno d 900 S', 'ablno d 900 E')
        e_type += '\nBareHandAttack: 4\nInt: 25\nE'
        mobs, errors = parse_from_string(e_type, parse_mob, split_on_vnums)
        expected = dict(BareHandAttack=4, Int=25)
        assert mobs[0]['extra_spec'] == expected
