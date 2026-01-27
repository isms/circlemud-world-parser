from circlemud_world_parser.room import Room
from circlemud_world_parser.utils import parse_from_string
from circlemud_world_parser.utils import split_on_vnums


class TestRoomParsing:
    def test_parsing_rooms(self):
        text = """#3028
The Thieves' Bar~
   The bar of the thieves.  Once upon a time this place was beautifully
furnished, but now it seems almost empty.  To the south is the yard, and to
the west is the entrance hall.
   (Maybe the furniture has been stolen?!)
~
30 cdh 0
D2
You see the secret yard.
~
~
0 -1 3029
D3
You see the entrance hall to the thieves' guild.
~
~
0 -1 3027
E
furniture~
As you look at the furniture, the chair you sit on disappears.
Also with multiple lines.
~
E
other~
A different thing.
~
S
#3029
The Secret Yard~
   The secret practice yard of thieves and assassins.  To the north is the
bar.  A well leads down into darkness.
~
30 cd 0
D0
You see the bar.
~
~
0 -1 3028
D5
You can't see what is down there, it is too dark.  Looks like it would be
impossible to climb back up.
~
~
0 -1 7043
S
"""
        rooms, errors = parse_from_string(text, Room.from_text, split_on_vnums)
        assert len(rooms) == 2

        # First room: The Thieves' Bar
        bar = rooms[0]
        assert bar.id == 3028
        assert bar.name == "The Thieves' Bar"
        assert bar.zone_number == 30
        assert bar.desc == "The bar of the thieves.  Once upon a time this place was beautifully\nfurnished, but now it seems almost empty.  To the south is the yard, and to\nthe west is the entrance hall.\n   (Maybe the furniture has been stolen?!)"

        assert bar.sector_type.value == 0
        assert bar.sector_type.note == "INSIDE"

        assert len(bar.flags) == 3
        flag_values = [(f.value, f.note) for f in bar.flags]
        assert (4, "NOMOB") in flag_values
        assert (8, "INDOORS") in flag_values
        assert (128, "NOMAGIC") in flag_values

        # exits
        assert len(bar.exits) == 2

        south_exit = bar.exits[0]
        assert south_exit.dir == 2
        assert south_exit.desc == "You see the secret yard."
        assert south_exit.keywords == []
        assert south_exit.key_number == -1
        assert south_exit.room_linked == 3029
        assert south_exit.door_flag.value == 0
        assert south_exit.door_flag.note == "NO_DOOR"

        west_exit = bar.exits[1]
        assert west_exit.dir == 3
        assert west_exit.desc == "You see the entrance hall to the thieves' guild."
        assert west_exit.keywords == []
        assert west_exit.key_number == -1
        assert west_exit.room_linked == 3027
        assert west_exit.door_flag.value == 0
        assert west_exit.door_flag.note == "NO_DOOR"

        # extra descriptions
        assert len(bar.extra_descs) == 2
        assert bar.extra_descs[0].keywords == ["furniture"]
        assert bar.extra_descs[0].desc == "As you look at the furniture, the chair you sit on disappears.\nAlso with multiple lines."
        assert bar.extra_descs[1].keywords == ["other"]
        assert bar.extra_descs[1].desc == "A different thing."

        # Second room: The Secret Yard
        yard = rooms[1]
        assert yard.id == 3029
        assert yard.name == "The Secret Yard"
        assert yard.zone_number == 30
        assert yard.desc == "The secret practice yard of thieves and assassins.  To the north is the\nbar.  A well leads down into darkness."

        assert yard.sector_type.value == 0
        assert yard.sector_type.note == "INSIDE"

        assert len(yard.flags) == 2
        flag_values = [(f.value, f.note) for f in yard.flags]
        assert (4, "NOMOB") in flag_values
        assert (8, "INDOORS") in flag_values

        assert len(yard.exits) == 2

        north_exit = yard.exits[0]
        assert north_exit.dir == 0
        assert north_exit.desc == "You see the bar."
        assert north_exit.room_linked == 3028

        down_exit = yard.exits[1]
        assert down_exit.dir == 5
        assert down_exit.desc == "You can't see what is down there, it is too dark.  Looks like it would be\nimpossible to climb back up."
        assert down_exit.room_linked == 7043

        assert yard.extra_descs == []

    def test_room_with_no_exit_description(self):
        text = """3374
A Sloping Tunnel~
   A bright light greets your eyes from the north, in
direct contrast to the darkness of the tunnel overhead.
You break  out in a sweat due to the overwhelming warmth
of the air.  The musky odor has grown quite intense,
drowning out everything else in the air and making it hard
to breathe.  Something in your gut begins squirming
uncomfortably as you wonder what's ahead...
~
33 adgj 4
D0
~
~
0 -1 3375
D4
~
~
0 -1 3373
S"""
        room = Room.from_text(text)
        assert len(room.exits) == 2
