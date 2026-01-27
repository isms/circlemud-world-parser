"""
Shops must be in CircleMUD v3.0 format. See "The CircleMUD
Builder's Manual" by Jeremy Elson, Section 7, for an
explanation of the different formats, and how to convert
older Diku-format shops to Circle v3.0.
"""
from pydantic import BaseModel, Field

from .constants import ObjectType, ShopFlag, ShopTradesWith
from .models import Flag
from .utils import parse_flags

# Reverse lookup for object type names to values (cached at module level)
OBJECT_TYPE_BY_NAME = {member.name: member.value for member in ObjectType}


class BuyType(BaseModel):
    """A type of item the shop will buy."""

    value: int | None = Field(None, description="Object type code")
    note: str = Field(..., description="Object type name")
    namelist: list[str] | None = Field(None, description="Optional keywords filter")

    @classmethod
    def from_line(cls, line: str) -> "BuyType":
        """Parse a buy type from a single line."""
        # at some point (2.x-3.x) the codebase went from `LIQ CONTAINER`` to `DRINKCON`
        # but some shops were not fixed; there are still many references on the web
        # to `LIQ CONTAINER` but this seems like an oversight in some cases and
        # outdated in others
        if "LIQ CONTAINER" in line:
            line = line.replace("LIQ CONTAINER", "DRINKCON")

        tokens = line.strip().split()
        if len(tokens) == 1:
            item_type = line.strip()
            namelist = None
        else:
            item_type = tokens[0]
            namelist = [token.lower() for token in tokens[1:]]

        # lookup the bitvector value from the flag for standardization
        value = OBJECT_TYPE_BY_NAME.get(item_type, None)

        return cls(value=value, note=item_type, namelist=namelist)


class ShopMessages(BaseModel):
    """Messages displayed by the shopkeeper."""

    buy_fails_object_does_not_exist: str = Field(..., description="When player tries to buy something not in stock")
    sell_fails_object_does_not_exist: str = Field(..., description="When player tries to sell something they don't have")
    sell_fails_shop_does_not_buy_object: str = Field(..., description="When shop won't buy that type of item")
    sell_fails_shop_cannot_afford_object: str = Field(..., description="When shop can't afford to buy the item")
    buy_fails_player_cannot_afford_object: str = Field(..., description="When player can't afford the item")
    buy_succeeds: str = Field(..., description="Successful purchase message")
    sell_succeeds: str = Field(..., description="Successful sale message")

    @classmethod
    def from_list(cls, messages: list[str]) -> "ShopMessages":
        """Parse shop messages from raw message lines."""
        keys = [
            'buy_fails_object_does_not_exist',
            'sell_fails_object_does_not_exist',
            'sell_fails_shop_does_not_buy_object',
            'sell_fails_shop_cannot_afford_object',
            'buy_fails_player_cannot_afford_object',
            'buy_succeeds',
            'sell_succeeds',
        ]
        cleaned = [m.lstrip('%s ').rstrip('~') for m in messages]
        return cls(**dict(zip(keys, cleaned)))


class OpeningHours(BaseModel):
    """A time period when the shop is open."""

    open: int = Field(..., description="Opening hour (0-28)")
    close: int = Field(..., description="Closing hour (0-28)")


class Shop(BaseModel):
    """A CircleMUD shop definition."""

    id: int = Field(..., description="Shop VNUM")
    objects: list[int] = Field(default_factory=list, description="VNUMs of objects for sale")
    sell_rate: float = Field(..., description="Price multiplier when selling to players")
    buy_rate: float = Field(..., description="Price multiplier when buying from players")
    buy_types: list[BuyType] = Field(default_factory=list, description="Types of items shop will buy")
    messages: ShopMessages = Field(..., description="Shopkeeper messages")
    temper: int = Field(..., description="Shopkeeper temper (0=normal)")
    flags: list[Flag] = Field(default_factory=list, description="Shop flags")
    shopkeeper: int = Field(..., description="VNUM of shopkeeper mobile")
    trades_with: list[Flag] = Field(default_factory=list, description="Restrictions on who can trade")
    rooms: list[int] = Field(default_factory=list, description="VNUMs of rooms where shop operates")
    times: list[OpeningHours] = Field(..., description="Opening hours (two periods)")

    @classmethod
    def from_text(cls, text: str) -> "Shop":
        """Parse a CircleMUD shop definition from raw text."""
        fields = [line.rstrip() for line in text.strip().split('\n')]
        delimiters = [i for i, field in enumerate(fields) if field == '-1']

        shop_id = int(fields[0].lstrip('#').rstrip('~'))

        objects_start, objects_stop = 1, delimiters[0]
        objects = [int(f) for f in fields[objects_start:objects_stop]]

        sell_rate = float(fields[objects_stop + 1])
        buy_rate = float(fields[objects_stop + 2])

        types_start, types_stop = objects_stop + 3, delimiters[1]
        buy_types = [BuyType.from_line(t) for t in fields[types_start:types_stop]]

        messages_start, messages_stop = delimiters[1] + 1, delimiters[1] + 8
        messages = ShopMessages.from_list(fields[messages_start:messages_stop])

        temper = int(fields[messages_stop])

        flags = parse_flags(fields[messages_stop + 1], ShopFlag)

        shopkeeper = int(fields[messages_stop + 2])

        trades_with = parse_flags(fields[messages_stop + 3], ShopTradesWith)

        rooms_start, rooms_stop = messages_stop + 4, delimiters[2]
        rooms = [int(r) for r in fields[rooms_start:rooms_stop]]

        times_raw = [int(t) for t in fields[rooms_stop + 1:]]
        if len(times_raw) != 4:
            raise ValueError('Unexpected number of open/close times')
        times = [
            OpeningHours(open=times_raw[0], close=times_raw[1]),
            OpeningHours(open=times_raw[2], close=times_raw[3]),
        ]

        return cls(
            id=shop_id,
            objects=objects,
            sell_rate=sell_rate,
            buy_rate=buy_rate,
            buy_types=buy_types,
            messages=messages,
            temper=temper,
            flags=flags,
            shopkeeper=shopkeeper,
            trades_with=trades_with,
            rooms=rooms,
            times=times,
        )
