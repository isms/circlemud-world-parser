import re

from pydantic import BaseModel, Field

from .constants import RoomDoorFlag, RoomFlag, RoomSectorType
from .models import ExtraDescription, Flag
from .utils import (_lookup_enum, clean_bitvector, lookup_value_to_dict,
                    parse_flags)

EXIT_RE = r"""D(\d+)
(.*?)~
(.*?)~
(.*?)
"""
EXIT_PATTERN = re.compile(EXIT_RE, re.DOTALL | re.MULTILINE)

EXTRA_DESC_RE = r"""E
(.*?)~
(.*?)
~"""
EXTRA_DESC_PATTERN = re.compile(EXTRA_DESC_RE, re.DOTALL)


class Exit(BaseModel):
    """An exit leading to another room."""

    dir: int = Field(..., description="Direction code (0=N, 1=E, 2=S, 3=W, 4=U, 5=D)")
    desc: str = Field(..., description="Description when looking in this direction")
    keywords: list[str] = Field(default_factory=list, description="Keywords for the door")
    key_number: int = Field(..., description="VNUM of key object, or -1 if none")
    room_linked: int = Field(..., description="VNUM of destination room")
    door_flag: Flag = Field(..., description="Door type (none, door, pickproof)")

    @classmethod
    def from_text(cls, text: str) -> list["Exit"]:
        """Parse exits from room bottom matter text."""
        exits = []
        matches = EXIT_PATTERN.findall(text)
        for match in matches:
            direction, desc, keys, other = match
            desc = desc.rstrip('\n')
            flag, key_num, to = other.strip().split()

            door_flag = Flag(value=int(flag), note=_lookup_enum(int(flag), RoomDoorFlag))
            exits.append(cls(
                dir=int(direction),
                desc=desc,
                keywords=keys.split(),
                key_number=int(key_num),
                room_linked=int(to),
                door_flag=door_flag,
            ))
        return exits


class Room(BaseModel):
    """A CircleMUD room definition."""

    id: int = Field(..., description="Virtual number (VNUM)")
    name: str = Field(..., description="Room name shown to players")
    desc: str = Field(..., description="Room description")
    zone_number: int = Field(..., description="Zone this room belongs to")
    flags: list[Flag] = Field(default_factory=list, description="Room flags (dark, nomob, etc.)")
    sector_type: Flag = Field(..., description="Terrain type")
    exits: list[Exit] = Field(default_factory=list, description="Exits to other rooms")
    extra_descs: list[ExtraDescription] = Field(default_factory=list, description="Extra descriptions")

    @staticmethod
    def parse_extra_descriptions_from_text(text: str) -> list[ExtraDescription]:
        """Parse extra descriptions from room bottom matter text."""
        extra_descs = []
        for keywords, desc in EXTRA_DESC_PATTERN.findall(text):
            extra_descs.append(ExtraDescription(keywords=keywords.split(), desc=desc))
        return extra_descs

    @classmethod
    def from_text(cls, text: str) -> "Room":
        """Parse a CircleMUD room definition from raw text."""
        parts = text.split('~')
        vnum, name = parts[0].split('\n')
        desc = parts[1].strip()
        zone, flags_raw, sector = parts[2].strip().split('\n')[0].strip().split(' ')

        flags_clean = clean_bitvector(flags_raw)
        flags = parse_flags(flags_raw, RoomFlag) if flags_clean else []

        sector_dict = lookup_value_to_dict(int(sector), RoomSectorType)
        sector_type = Flag(**sector_dict)

        bottom_matter = '~'.join(parts[2:])
        exits = Exit.from_text(bottom_matter)
        extra_descs = cls.parse_extra_descriptions_from_text(bottom_matter)

        return cls(
            id=int(vnum),
            name=name.strip(),
            desc=desc.strip('\n'),
            zone_number=int(zone),
            flags=flags,
            sector_type=sector_type,
            exits=exits,
            extra_descs=extra_descs,
        )
