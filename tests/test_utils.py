from enum import IntFlag

from circlemud_world_parser.utils import bitvector_to_numbers
from circlemud_world_parser.utils import bitvector_letters_to_numbers
from circlemud_world_parser.utils import bitvector_number_to_numbers
from circlemud_world_parser.utils import bitvector_to_flags


class TestBitvectorParsing:
    def test_bitvector_number_to_numbers(self):
        bitvector = 8193
        expected = [1, 8192]
        actual = list(bitvector_number_to_numbers(8193))
        assert actual == expected

        actual = list(bitvector_to_numbers(bitvector))
        assert actual == expected

    def test_bitvector_letters_to_numbers(self):
        bitvector = 'adjmnoq'
        expected = [1, 8, 512, 4096, 8192, 16384, 65536]
        actual = list(bitvector_letters_to_numbers(bitvector))
        assert actual == expected

        actual = list(bitvector_to_numbers(bitvector))
        assert actual == expected

    def test_bitvector_to_flags(self):
        class TestFlags(IntFlag):
            GLOWING = 1
            BUZZING = 2
            OOZING = 4
            BUBBLING = 8

        bitvector = 6
        expected = [
            {"note": "BUZZING", "value": 2},
            {"note": "OOZING", "value": 4}
        ]
        actual = bitvector_to_flags(bitvector, TestFlags)
        assert actual == expected
