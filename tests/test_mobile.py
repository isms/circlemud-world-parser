import pytest

from circlemud_world_parser.mobile import Mobile
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
        mobs, errors = parse_from_string(mob_text, Mobile.from_text, split_on_vnums)
        mob = mobs.pop()

        assert mob.id == 3000
        assert mob.aliases == ["wizard"]
        assert mob.short_desc == "the wizard"
        assert mob.long_desc == "A wizard walks around behind the counter, talking to himself."
        assert mob.detail_desc == "The wizard looks old and senile, and yet he looks like a very powerful\nwizard.  He is equipped with fine clothing, and is wearing many fine\nrings and bracelets."
        assert mob.mob_type == "S"
        assert mob.alignment == 900
        assert mob.level == 33
        assert mob.thac0 == 2
        assert mob.armor_class == 2
        assert mob.gold == 30000
        assert mob.xp == 160000
        assert mob.extra_spec == {}

        # max_hit_points dice roll
        assert mob.max_hit_points.dice == 1
        assert mob.max_hit_points.sides == 1
        assert mob.max_hit_points.bonus == 30000

        # bare_hand_damage dice roll
        assert mob.bare_hand_damage.dice == 2
        assert mob.bare_hand_damage.sides == 8
        assert mob.bare_hand_damage.bonus == 18

        # flags
        assert len(mob.flags) == 5
        flag_values = [(f.value, f.note) for f in mob.flags]
        assert (1, "SPEC") in flag_values
        assert (2, "SENTINEL") in flag_values
        assert (2048, "MEMORY") in flag_values
        assert (8192, "NOCHARM") in flag_values
        assert (16384, "NOSUMMON") in flag_values

        # affects
        assert len(mob.affects) == 1
        assert mob.affects[0].value == 8
        assert mob.affects[0].note == "DETECT_INVIS"

        # gender
        assert mob.gender.value == 1
        assert mob.gender.note == "M"

        # position
        assert mob.position.load.value == 8
        assert mob.position.load.note == "POSITION_STANDING"
        assert mob.position.default.value == 8
        assert mob.position.default.note == "POSITION_STANDING"

    def test_parsing_type_e_mob(self, mob_text):
        e_type = mob_text.replace('ablno d 900 S', 'ablno d 900 E')
        e_type += '\nBareHandAttack: 4\nInt: 25\nE'
        mobs, errors = parse_from_string(e_type, Mobile.from_text, split_on_vnums)
        mob = mobs[0]

        assert mob.extra_spec == {"BareHandAttack": 4, "Int": 25}
