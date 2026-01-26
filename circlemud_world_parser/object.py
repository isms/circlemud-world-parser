from pydantic import BaseModel, Field

from .constants import (OBJECT_AFFECT_LOCATION_FLAGS,
                        OBJECT_EXTRA_EFFECTS_FLAGS, OBJECT_TYPE_FLAGS,
                        OBJECT_WEAR_FLAGS)
from .models import ExtraDescription, Flag
from .utils import lookup_value_to_dict, parse_flags


class Affect(BaseModel):
    """An affect that modifies a character attribute."""

    location: int = Field(..., description="Affect location code")
    note: str | None = Field(None, description="Human-readable location name")
    value: int = Field(..., description="Modifier value")

    @classmethod
    def from_fields(cls, extra_fields: list[str]) -> list["Affect"]:
        """Parse affects from the 'A' blocks in object data."""
        results = []
        for i, field in enumerate(extra_fields):
            if field == 'A':
                loc, value = (int(v) for v in extra_fields[i + 1].split())
                note = OBJECT_AFFECT_LOCATION_FLAGS.get(loc, None)
                results.append(cls(location=loc, note=note, value=value))
        return results


def parse_extra_descriptions_from_fields(extra_fields: list[str]) -> list[ExtraDescription]:
    """Parse extra descriptions from the 'E' blocks in object data."""
    results = []
    i = 0
    while i < len(extra_fields):
        if extra_fields[i] == 'E':
            i += 1
            keywords = extra_fields[i].rstrip('~').split()
            i += 1
            desc_lines = []
            while i < len(extra_fields) and extra_fields[i] not in ('~', '$'):
                desc_lines.append(extra_fields[i])
                i += 1
            results.append(ExtraDescription(keywords=keywords, desc='\n'.join(desc_lines)))
        i += 1
    return results


class Object(BaseModel):
    """A CircleMUD object definition."""

    id: int = Field(..., description="Virtual number (VNUM)")
    aliases: list[str] = Field(..., description="Keywords for targeting the object")
    short_desc: str = Field(..., description="Name shown in inventory and actions")
    long_desc: str = Field(..., description="Description when object is on the ground")
    action_desc: str | None = Field(None, description="Description when used")
    type: Flag = Field(..., description="Object type (weapon, armor, etc.)")
    effects: list[Flag] = Field(default_factory=list, description="Extra effects (glow, hum, etc.)")
    wear: list[Flag] = Field(default_factory=list, description="Wear positions")
    values: list[int] = Field(..., description="Type-specific values")
    weight: int = Field(..., description="Object weight")
    cost: int = Field(..., description="Value in gold")
    rent: int = Field(..., description="Daily rent cost")
    affects: list[Affect] = Field(default_factory=list, description="Stat modifiers when worn")
    extra_descs: list[ExtraDescription] = Field(default_factory=list, description="Extra descriptions")

    @classmethod
    def from_text(cls, text: str) -> "Object":
        """Parse a CircleMUD object definition from raw text."""
        fields = [line.rstrip() for line in text.strip().split('\n')]

        # easy fields
        obj_id = int(fields[0])
        aliases = fields[1].rstrip('~').split()
        short_desc = fields[2].rstrip('~')
        long_desc = fields[3].rstrip('~')
        values = [int(v) for v in fields[6].split()]
        weight, cost, rent = (int(v) for v in fields[7].split())

        type_flag, effects_bits, wear_bitvector = fields[5].split()

        # type flag is always an int
        type_dict = lookup_value_to_dict(int(type_flag), OBJECT_TYPE_FLAGS)
        obj_type = Flag(**type_dict)

        # parse the bitvectors
        effects = parse_flags(effects_bits, OBJECT_EXTRA_EFFECTS_FLAGS)
        wear = parse_flags(wear_bitvector, OBJECT_WEAR_FLAGS)

        action_desc = fields[4].rstrip('~') or None

        affects = []
        extra_descs = []
        if len(fields) > 8:
            extra_fields = fields[8:]
            affects = Affect.from_fields(extra_fields)
            extra_descs = parse_extra_descriptions_from_fields(extra_fields)

        return cls(
            id=obj_id,
            aliases=aliases,
            short_desc=short_desc,
            long_desc=long_desc,
            action_desc=action_desc,
            type=obj_type,
            effects=effects,
            wear=wear,
            values=values,
            weight=weight,
            cost=cost,
            rent=rent,
            affects=affects,
            extra_descs=extra_descs,
        )
