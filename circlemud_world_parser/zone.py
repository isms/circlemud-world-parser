# coding: utf-8
import re

from pydantic import BaseModel, Field

from .constants import MOB_EQUIP

COMMAND_RE = r'(\d+)'
COMMAND_PATTERN = re.compile(COMMAND_RE)


class ObjectContainer(BaseModel):
    """An object that can contain other objects."""

    id: int = Field(..., description="Object VNUM")
    max: int = Field(..., description="Maximum number to load")
    contents: list["ObjectContainer"] = Field(default_factory=list, description="Contained objects")


class EquippedObject(BaseModel):
    """An object equipped on a mob."""

    id: int = Field(..., description="Object VNUM")
    max: int = Field(..., description="Maximum number to load")
    location: int = Field(..., description="Equipment slot code")
    note: str | None = Field(None, description="Human-readable slot name")
    contents: list[ObjectContainer] = Field(default_factory=list, description="Contained objects")


class InventoryObject(BaseModel):
    """An object in a mob's inventory."""

    id: int = Field(..., description="Object VNUM")
    max: int = Field(..., description="Maximum number to load")
    contents: list[ObjectContainer] = Field(default_factory=list, description="Contained objects")


class ZoneMob(BaseModel):
    """A mob to be loaded in a zone."""

    mob: int = Field(..., description="Mobile VNUM")
    max: int = Field(..., description="Maximum number to load")
    room: int = Field(..., description="Room VNUM to load in")
    inventory: list[InventoryObject] = Field(default_factory=list, description="Inventory items")
    equipped: list[EquippedObject] = Field(default_factory=list, description="Equipped items")


class ZoneObject(BaseModel):
    """An object to be loaded in a zone."""

    id: int = Field(..., description="Object VNUM")
    max: int = Field(..., description="Maximum number to load")
    room: int = Field(..., description="Room VNUM to load in")
    contents: list[ObjectContainer] = Field(default_factory=list, description="Contained objects")


class Door(BaseModel):
    """A door state to set on zone reset."""

    room: int = Field(..., description="Room VNUM")
    exit: int = Field(..., description="Exit direction")
    state: int = Field(..., description="Door state (0=open, 1=closed, 2=locked)")


class RemoveObject(BaseModel):
    """An object to remove from a room on zone reset."""

    room: int = Field(..., description="Room VNUM")
    id: int = Field(..., description="Object VNUM to remove")


class Zone(BaseModel):
    """A CircleMUD zone definition."""

    id: int = Field(..., description="Zone number")
    name: str = Field(..., description="Zone name")
    bottom_room: int = Field(..., description="First room VNUM in zone")
    top_room: int = Field(..., description="Last room VNUM in zone")
    lifespan: int = Field(..., description="Minutes between zone resets")
    reset_mode: int = Field(..., description="Reset mode (0=never, 1=empty, 2=always)")
    mobs: list[ZoneMob] = Field(default_factory=list, description="Mobs to load")
    objects: list[ZoneObject] = Field(default_factory=list, description="Objects to load")
    doors: list[Door] = Field(default_factory=list, description="Doors to set")
    remove_objects: list[RemoveObject] = Field(default_factory=list, description="Objects to remove")

    @classmethod
    def from_text(cls, text: str) -> "Zone":
        """Parse a CircleMUD zone definition from raw text."""
        fields = [line.rstrip() for line in text.strip().split('\n')]

        # remove comment lines
        fields = [f for f in fields if not f.startswith('*')]

        zone_id = int(fields[0])
        name = fields[1].rstrip('~')

        bottom, top, lifespan, reset_mode = map(int, fields[2].split())

        commands = fields[3:]
        mobs, objects, doors, remove_objects = cls._parse_commands(commands)

        return cls(
            id=zone_id,
            name=name,
            bottom_room=bottom,
            top_room=top,
            lifespan=lifespan,
            reset_mode=reset_mode,
            mobs=mobs,
            objects=objects,
            doors=doors,
            remove_objects=remove_objects,
        )

    @classmethod
    def _get_command_fields(cls, command: str, n_fields: int = 4) -> list[int]:
        """Extract numeric fields from a zone command."""
        results = COMMAND_PATTERN.findall(command)
        return [int(r) for r in results[:n_fields]]

    @classmethod
    def _get_contents(cls, commands: list[str], i: int, curr_obj: int) -> list[ObjectContainer]:
        """Recursively get contents of a container."""
        contents = []
        i += 1
        while i < len(commands) and commands[i].startswith('P'):
            _, new_object, max_count, container = cls._get_command_fields(commands[i])
            if container == curr_obj:
                subcontents = cls._get_contents(commands, i, new_object)
                contents.append(ObjectContainer(id=new_object, max=max_count, contents=subcontents))
            i += 1
        return contents

    @classmethod
    def _parse_commands(cls, commands: list[str]) -> tuple[list[ZoneMob], list[ZoneObject], list[Door], list[RemoveObject]]:
        """Parse zone commands into structured data."""
        mobs = []
        objects = []
        doors = []
        remove_objects = []

        for i, curr in enumerate(commands):
            if curr == 'S':
                break

            elif curr.startswith('M'):
                _, mob, max_count, room = cls._get_command_fields(curr)
                mobs.append(ZoneMob(mob=mob, max=max_count, room=room, inventory=[], equipped=[]))

            elif curr.startswith('E'):
                _, obj, max_count, location = cls._get_command_fields(curr)
                note = MOB_EQUIP.get(location, None)
                contents = cls._get_contents(commands, i, obj)
                mobs[-1].equipped.append(EquippedObject(
                    location=location, max=max_count, id=obj, note=note, contents=contents
                ))

            elif curr.startswith('G'):
                _, obj, max_count = cls._get_command_fields(curr, 3)
                contents = cls._get_contents(commands, i, obj)
                mobs[-1].inventory.append(InventoryObject(max=max_count, id=obj, contents=contents))

            elif curr.startswith('O'):
                _, obj, max_count, room = cls._get_command_fields(curr)
                contents = cls._get_contents(commands, i, obj)
                objects.append(ZoneObject(max=max_count, id=obj, room=room, contents=contents))

            elif curr.startswith('D'):
                _, room, exit_dir, state = cls._get_command_fields(curr)
                doors.append(Door(room=room, exit=exit_dir, state=state))

            elif curr.startswith('R'):
                _, room, obj = cls._get_command_fields(curr, 3)
                remove_objects.append(RemoveObject(room=room, id=obj))

        return mobs, objects, doors, remove_objects
