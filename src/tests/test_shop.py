# coding: utf-8
import pytest

from shop import parse_shop


class TestShopParsing:
    @pytest.fixture
    def shop_text(self):
        return """#3000~
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

    def test_parsing_shop(self, shop_text):
        expected = {
            'id': 3000,
            'objects': [3050, 3051, 3052, 3053, 3054],
            'sell_rate': 1.15,
            'buy_rate': 0.15,
            'buy_types': [
                {
                    'note': 'WEAPON',
                    'value': 5,
                    'namelist': ['[sword', '&', 'long', '|', 'short', '|', 'warhammer', '|', '^golden', '&', 'bow]', '&', 'magic']
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
        shop = parse_shop(shop_text)
        assert shop == expected
