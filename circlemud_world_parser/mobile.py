# coding: utf-8
from pydantic import BaseModel, Field

from .constants import MOB_ACTION_FLAGS
from .constants import MOB_AFFECT_FLAGS
from .constants import MOB_GENDER
from .constants import MOB_POSITION
from .utils import bitvector_to_flags
from .utils import clean_bitvector
from .utils import lookup_value_to_dict


class Flag(BaseModel):
    """A flag with a numeric value and optional descriptive note."""

    value: int = Field(..., description="Numeric flag value")
    note: str | None = Field(None, description="Human-readable flag name")


class DiceRoll(BaseModel):
    """A dice roll formula (e.g., 2d6+10)."""

    dice: int = Field(..., description="Number of dice to roll")
    sides: int = Field(..., description="Number of sides per die")
    bonus: int = Field(..., description="Flat bonus added to roll")

    @classmethod
    def parse_from_string(cls, roll_string: str) -> "DiceRoll":
        """Parse a dice roll string like '4d6+20' into a DiceRoll."""
        dice_part, bonus = roll_string.split('+')
        dice, sides = dice_part.split('d')
        return cls(dice=int(dice), sides=int(sides), bonus=int(bonus))


class Position(BaseModel):
    """Position states for a mobile."""

    load: Flag = Field(..., description="Position when loaded")
    default: Flag = Field(..., description="Default position")


class Mobile(BaseModel):
    """A CircleMUD mobile (NPC) definition."""

    id: int = Field(..., description="Virtual number (VNUM)")
    aliases: list[str] = Field(..., description="Keywords for targeting")
    short_desc: str = Field(..., description="Name shown in actions")
    long_desc: str = Field(..., description="Description in room")
    detail_desc: str = Field(..., description="Description when examined")
    mob_type: str = Field(..., description="Mobile type (S=simple, E=extended)")
    alignment: int = Field(..., description="Alignment (-1000 to 1000)")
    flags: list[Flag] = Field(default_factory=list, description="Action flags")
    affects: list[Flag] = Field(default_factory=list, description="Affect flags")
    level: int = Field(..., description="Mobile level")
    thac0: int = Field(..., description="To-hit armor class 0")
    armor_class: int = Field(..., description="Armor class")
    max_hit_points: DiceRoll = Field(..., description="HP dice formula")
    bare_hand_damage: DiceRoll = Field(..., description="Barehanded damage dice")
    gold: int = Field(..., description="Gold carried")
    xp: int = Field(..., description="Experience points awarded")
    position: Position = Field(..., description="Position states")
    gender: Flag = Field(..., description="Gender (N/M/F)")
    extra_spec: dict[str, int] = Field(default_factory=dict, description="Extended specs for E-type mobs")

    @classmethod
    def parse_raw(cls, text: str) -> "Mobile":
        """Parse a CircleMUD mobile definition from raw text."""
        fields = [line.rstrip() for line in text.strip().split('\n')]

        mob_id = int(fields[0])
        aliases = fields[1].rstrip('~').split()
        short_desc = fields[2].rstrip('~')
        long_desc = text.split('~')[2].strip('\n')
        detail_desc = text.split('~')[3].strip('\n')

        tildes = [i for i, a in enumerate(text) if a == '~']
        start_bottom_matter = tildes[3] + 1
        bottom_fields = text[start_bottom_matter:].strip('\n').split('\n')

        vector_line = bottom_fields[0]
        action, affect, alignment, mob_type = vector_line.split()

        action_clean = clean_bitvector(action)
        flags_dicts = bitvector_to_flags(action_clean, MOB_ACTION_FLAGS)
        flags = [Flag(**f) for f in flags_dicts]

        affect_clean = clean_bitvector(affect)
        affects_dicts = bitvector_to_flags(affect_clean, MOB_AFFECT_FLAGS)
        affects = [Flag(**f) for f in affects_dicts]

        level, thac0, ac, max_hp, bare_hand_dmg = bottom_fields[1].split()
        gold, xp = bottom_fields[2].split()
        load_position, default_position, gender = bottom_fields[3].split()

        load_dict = lookup_value_to_dict(int(load_position), MOB_POSITION)
        default_dict = lookup_value_to_dict(int(load_position), MOB_POSITION)
        position = Position(load=Flag(**load_dict), default=Flag(**default_dict))

        gender_dict = lookup_value_to_dict(int(gender), MOB_GENDER)

        extra_spec = {}
        if len(bottom_fields) > 4:
            assert mob_type == 'E'
            assert bottom_fields[-1] == 'E'

            for line in bottom_fields[4:]:
                if line == 'E':
                    break
                key, value = line.split(': ')
                extra_spec[key] = int(value)

        return cls(
            id=mob_id,
            aliases=aliases,
            short_desc=short_desc,
            long_desc=long_desc,
            detail_desc=detail_desc,
            mob_type=mob_type,
            alignment=int(alignment),
            flags=flags,
            affects=affects,
            level=int(level),
            thac0=int(thac0),
            armor_class=int(ac),
            max_hit_points=DiceRoll.parse_from_string(max_hp),
            bare_hand_damage=DiceRoll.parse_from_string(bare_hand_dmg),
            gold=int(gold),
            xp=int(xp),
            position=position,
            gender=Flag(**gender_dict),
            extra_spec=extra_spec,
        )
