from circlemud_world_parser.zone import Zone


class TestZoneParsing:
    def test_parsing_zone(self):
        text = """60
Haon-Dor, Light Forest~
6000 6099 13 2
*
* Mobiles
M 0 6000 1 6009         John The Lumberjack
E 1 6000 2 16                   Lumber Axe
E 1 6001 10 5                   Chequered Shirt
M 0 6001 6 6012         Rabbit
G 1 6023 10                     Meat
P 1 1234 1 6023                       Maggot (not a real item)
* Objects
O 0 6011 10 6013        Mushroom
R 0 6016 6011
O 0 6017 1 6026         Corpse Of The Boar
P 1 6018 1 6017                 Meat
P 1 6019 1 6017                 Tusks
* Doors
D 0 6009 0 1            Cabin
D 0 6010 2 1
*
S"""

        zone = Zone.from_text(text)

        # Basic zone info
        assert zone.id == 60
        assert zone.name == "Haon-Dor, Light Forest"
        assert zone.bottom_room == 6000
        assert zone.top_room == 6099
        assert zone.lifespan == 13
        assert zone.reset_mode == 2

        # Mobs
        assert len(zone.mobs) == 2

        lumberjack = zone.mobs[0]
        assert lumberjack.mob == 6000
        assert lumberjack.max == 1
        assert lumberjack.room == 6009
        assert lumberjack.inventory == []

        assert len(lumberjack.equipped) == 2
        axe = lumberjack.equipped[0]
        assert axe.id == 6000
        assert axe.max == 2
        assert axe.location == 16
        assert axe.note == "WIELD"
        assert axe.contents == []

        shirt = lumberjack.equipped[1]
        assert shirt.id == 6001
        assert shirt.max == 10
        assert shirt.location == 5
        assert shirt.note == "BODY"
        assert shirt.contents == []

        rabbit = zone.mobs[1]
        assert rabbit.mob == 6001
        assert rabbit.max == 6
        assert rabbit.room == 6012
        assert rabbit.equipped == []

        assert len(rabbit.inventory) == 1
        meat = rabbit.inventory[0]
        assert meat.id == 6023
        assert meat.max == 10
        assert len(meat.contents) == 1
        maggot = meat.contents[0]
        assert maggot.id == 1234
        assert maggot.max == 1
        assert maggot.contents == []

        # Objects
        assert len(zone.objects) == 2

        mushroom = zone.objects[0]
        assert mushroom.id == 6011
        assert mushroom.room == 6013
        assert mushroom.max == 10
        assert mushroom.contents == []

        corpse = zone.objects[1]
        assert corpse.id == 6017
        assert corpse.room == 6026
        assert corpse.max == 1
        assert len(corpse.contents) == 2
        assert corpse.contents[0].id == 6018
        assert corpse.contents[0].max == 1
        assert corpse.contents[0].contents == []
        assert corpse.contents[1].id == 6019
        assert corpse.contents[1].max == 1
        assert corpse.contents[1].contents == []

        # Doors
        assert len(zone.doors) == 2

        cabin_door = zone.doors[0]
        assert cabin_door.room == 6009
        assert cabin_door.exit == 0
        assert cabin_door.state == 1

        other_door = zone.doors[1]
        assert other_door.room == 6010
        assert other_door.exit == 2
        assert other_door.state == 1

        # Remove objects
        assert len(zone.remove_objects) == 1
        removal = zone.remove_objects[0]
        assert removal.room == 6016
        assert removal.id == 6011
