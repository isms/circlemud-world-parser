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
        objs, errors = parse_from_string(text, Object.from_text, split_on_vnums)
        assert len(objs) == 2

        # First object: Jupiter's Thunderbolt
        thunderbolt = objs[0]
        assert thunderbolt.id == 12020
        assert thunderbolt.aliases == ["thunderbolt", "jupiter"]
        assert thunderbolt.short_desc == "Jupiter's Thunderbolt"
        assert thunderbolt.long_desc == "Jupiter's Thunderbolt has been left here."
        assert thunderbolt.weight == 22
        assert thunderbolt.cost == 100000
        assert thunderbolt.rent == 25000
        assert thunderbolt.values == [0, 4, 6, 6]

        assert thunderbolt.type.value == 5
        assert thunderbolt.type.note == "WEAPON"

        assert len(thunderbolt.wear) == 2
        assert thunderbolt.wear[0].value == 1
        assert thunderbolt.wear[0].note == "WEAR_TAKE"
        assert thunderbolt.wear[1].value == 8192
        assert thunderbolt.wear[1].note == "WEAR_WIELD"

        assert len(thunderbolt.effects) == 5
        effect_values = [(e.value, e.note) for e in thunderbolt.effects]
        assert (2, "HUM") in effect_values
        assert (64, "MAGIC") in effect_values
        assert (1024, "ANTI_EVIL") in effect_values
        assert (4096, "ANTI_MAGIC_USER") in effect_values
        assert (8192, "ANTI_CLERIC") in effect_values

        assert len(thunderbolt.affects) == 2
        assert thunderbolt.affects[0].location == 18
        assert thunderbolt.affects[0].note == "HITROLL"
        assert thunderbolt.affects[0].value == 3
        assert thunderbolt.affects[1].location == 19
        assert thunderbolt.affects[1].note == "DAMROLL"
        assert thunderbolt.affects[1].value == 3

        assert thunderbolt.extra_descs == []

        # Second object: telescope
        telescope = objs[1]
        assert telescope.id == 15005
        assert telescope.aliases == ["telescope", "scope"]
        assert telescope.short_desc == "a large telescope"
        assert telescope.long_desc == "There is a large telescope here, pointing at the sky."
        assert telescope.weight == 0
        assert telescope.cost == 0
        assert telescope.rent == 0
        assert telescope.values == [0, 0, 0, 0]

        assert telescope.type.value == 12
        assert telescope.type.note == "OTHER"

        assert telescope.wear == []
        assert telescope.effects == []

        assert len(telescope.affects) == 2
        assert telescope.affects[0].location == 18
        assert telescope.affects[0].note == "HITROLL"
        assert telescope.affects[0].value == 2
        assert telescope.affects[1].location == 19
        assert telescope.affects[1].note == "DAMROLL"
        assert telescope.affects[1].value == 2

        assert len(telescope.extra_descs) == 1
        assert telescope.extra_descs[0].keywords == ["telescope", "scope"]
        assert telescope.extra_descs[0].desc == "A small sign says:\n\nMade in Siberia.\n"

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
        objs, errors = parse_from_string(text, Object.from_text, split_on_vnums)
        thing = objs.pop()

        assert len(thing.effects) == 4

        # Check that one of the effects has the non-stock flag value
        effect_values = [e.value for e in thing.effects]
        assert 274877906944 in effect_values

        # The non-stock flag should have note=None
        non_stock = [e for e in thing.effects if e.value == 274877906944][0]
        assert non_stock.note is None
