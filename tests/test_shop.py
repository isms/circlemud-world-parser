import pytest

from circlemud_world_parser.shop import Shop


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
        shop = Shop.from_text(shop_text)

        # Basic shop info
        assert shop.id == 3000
        assert shop.objects == [3050, 3051, 3052, 3053, 3054]
        assert shop.sell_rate == 1.15
        assert shop.buy_rate == 0.15
        assert shop.temper == 0
        assert shop.shopkeeper == 3000
        assert shop.rooms == [3033]

        # Buy types
        assert len(shop.buy_types) == 4

        weapon_type = shop.buy_types[0]
        assert weapon_type.note == "WEAPON"
        assert weapon_type.value == 5
        assert weapon_type.namelist == ['[sword', '&', 'long', '|', 'short', '|', 'warhammer', '|', '^golden', '&', 'bow]', '&', 'magic']

        wand_type = shop.buy_types[1]
        assert wand_type.note == "WAND"
        assert wand_type.value == 3
        assert wand_type.namelist is None

        staff_type = shop.buy_types[2]
        assert staff_type.note == "STAFF"
        assert staff_type.value == 4
        assert staff_type.namelist is None

        potion_type = shop.buy_types[3]
        assert potion_type.note == "POTION"
        assert potion_type.value == 10
        assert potion_type.namelist is None

        # Messages
        assert shop.messages.buy_fails_object_does_not_exist == "Sorry, I haven't got exactly that item."
        assert shop.messages.sell_fails_object_does_not_exist == "You don't seem to have that."
        assert shop.messages.sell_fails_shop_does_not_buy_object == "I don't buy such items."
        assert shop.messages.sell_fails_shop_cannot_afford_object == "That is too expensive for me!"
        assert shop.messages.buy_fails_player_cannot_afford_object == "You can't afford it!"
        assert shop.messages.buy_succeeds == "That'll be %d coins, please."
        assert shop.messages.sell_succeeds == "You'll get %d coins for it!"

        # Flags
        assert len(shop.flags) == 1
        assert shop.flags[0].value == 2
        assert shop.flags[0].note == "WILL_BANK_MONEY"

        # Trades with
        assert len(shop.trades_with) == 1
        assert shop.trades_with[0].value == 2
        assert shop.trades_with[0].note == "NOEVIL"

        # Opening hours
        assert len(shop.times) == 2
        assert shop.times[0].open == 0
        assert shop.times[0].close == 28
        assert shop.times[1].open == 0
        assert shop.times[1].close == 0
