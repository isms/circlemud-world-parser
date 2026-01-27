from enum import IntEnum, IntFlag


class ObjectType(IntEnum):
    """Object type flags."""
    LIGHT = 1  # Item is a light source.
    SCROLL = 2  # Item is a magical scroll.
    WAND = 3  # Item is a magical wand.
    STAFF = 4  # Item is a magical staff.
    WEAPON = 5  # Item is a weapon.
    FIREWEAPON = 6  # Currently not implemented.  Do not use.
    MISSILE = 7  # Currently not implemented.  Do not use.
    TREASURE = 8  # Item is treasure other than gold coins (e.g. gems).
    ARMOR = 9  # Item is armor.
    POTION = 10  # Item is a magical potion.
    WORN = 11  # Currently not implemented.  Do not use.
    OTHER = 12  # Miscellaneous object with no special properties.
    TRASH = 13  # Trash -- junked by cleaners, not bought by shopkeepers.
    TRAP = 14  # Currently not implemented.  Do not use.
    CONTAINER = 15  # Item is a container.
    NOTE = 16  # Item is a note (can be written on).
    DRINKCON = 17  # Item is a drink container.
    KEY = 18  # Item is a key.
    FOOD = 19  # Item is food.
    MONEY = 20  # Item is money (gold coins).
    PEN = 21  # Item is a pen.
    BOAT = 22  # Item is a boat; allows you to traverse SECT_WATER_NOSWIM.
    FOUNTAIN = 23  # Item is a fountain.


class ObjectExtraEffect(IntFlag):
    """Object extra effects (bitvector)."""
    GLOW = 1  # Item is glowing (cosmetic).
    HUM = 2  # Item is humming (cosmetic).
    NORENT = 4  # Item cannot be rented.
    NODONATE = 8  # Item cannot be donated.
    NOINVIS = 16  # Item cannot be made invisible.
    INVISIBLE = 32  # Item is invisible.
    MAGIC = 64  # Item has a magical aura and can't be enchanted.
    NODROP = 128  # Item is cursed and cannot be dropped.
    BLESS = 256  # Item is blessed (cosmetic).
    ANTI_GOOD = 512  # Item can't be used by good-aligned characters.
    ANTI_EVIL = 1024  # Item can't be used by evil-aligned characters.
    ANTI_NEUTRAL = 2048  # Item can't be used by neutrally-aligned characters.
    ANTI_MAGIC_USER = 4096  # Item can't be used by the Mage class.
    ANTI_CLERIC = 8192  # Item can't be used by the Cleric class.
    ANTI_THIEF = 16384  # Item can't be used by the Thief class.
    ANTI_WARRIOR = 32768  # Item can't be used by the Warrior class.
    NOSELL = 65536  # Shopkeepers will not buy or sell the item.


class ObjectWear(IntFlag):
    """Object wear flags (bitvector)."""
    WEAR_TAKE = 1  # Item can be taken (picked up off the ground).
    WEAR_FINGER = 2  # Item can be worn on the fingers.
    WEAR_NECK = 4  # Item can be worn around the neck.
    WEAR_BODY = 8  # Item can be worn on the body.
    WEAR_HEAD = 16  # Item can be worn on the head.
    WEAR_LEGS = 32  # Item can be worn on the legs.
    WEAR_FEET = 64  # Item can be worn on the feet.
    WEAR_HANDS = 128  # Item can be worn on the hands.
    WEAR_ARMS = 256  # Item can be worn on the arms.
    WEAR_SHIELD = 512  # Item can be used as a shield.
    WEAR_ABOUT = 1024  # Item can be worn about the body.
    WEAR_WAIST = 2048  # Item can be worn around the waist.
    WEAR_WRIST = 4096  # Item can be worn around the wrist.
    WEAR_WIELD = 8192  # Item can be wielded; e.g. weapons.
    WEAR_HOLD = 16384  # Item can be held (the 'hold' command).


class ObjectAffectLocation(IntEnum):
    """Object affect location flags."""
    NONE = 0  # No effect (typically not used).
    STR = 1  # Apply to strength.
    DEX = 2  # Apply to dexterity.
    INT = 3  # Apply to intelligence.
    WIS = 4  # Apply to wisdom.
    CON = 5  # Apply to constitution.
    CHA = 6  # Apply to charisma.
    CLASS = 7  # Unimplemented.  Do not use.
    LEVEL = 8  # Unimplemented.  Do not use.
    AGE = 9  # Apply to character's MUD age, in MUD years.
    CHAR_WEIGHT = 10  # Apply to weight.
    CHAR_HEIGHT = 11  # Apply to height.
    MANA = 12  # Apply to MAX mana points.
    HIT = 13  # Apply to MAX hit points.
    MOVE = 14  # Apply to MAX movement points.
    GOLD = 15  # Unimplemented.  Do not use.
    EXP = 16  # Unimplemented.  Do not use.
    AC = 17  # Apply to armor class (AC).
    HITROLL = 18  # Apply to hitroll.
    DAMROLL = 19  # Apply to damage roll bonus.
    SAVING_PARA = 20  # Apply to save throw: paralyze
    SAVING_ROD = 21  # Apply to save throw: rods
    SAVING_PETRI = 22  # Apply to save throw: petrif
    SAVING_BREATH = 23  # Apply to save throw: breath
    SAVING_SPELL = 24  # Apply to save throw: spells


class RoomFlag(IntFlag):
    """Room flags (bitvector)."""
    DARK = 1  # Room is dark.
    DEATH = 2  # Room is a death trap; char 'dies' (no xp lost).
    NOMOB = 4  # MOBs (monsters) cannot enter room.
    INDOORS = 8  # Room is indoors.
    PEACEFUL = 16  # Room is peaceful (violence not allowed).
    SOUNDPROOF = 32  # Shouts, gossips, etc. won't be heard in room.
    NOTRACK = 64  # 'track' can't find a path through this room.
    NOMAGIC = 128  # All magic attempted in this room will fail.
    TUNNEL = 256  # Only one person allowed in room at a time.
    PRIVATE = 512  # Cannot teleport in or GOTO if two people here.
    GODROOM = 1024  # Only LVL_GOD and above allowed to enter.
    HOUSE = 2048  # Reserved for internal use. Do not set.
    HOUSE_CRASH = 4096  # Reserved for internal use. Do not set.
    ATRIUM = 8192  # Reserved for internal use. Do not set.
    OLC = 16384  # Reserved for internal use. Do not set.
    BFS_MARK = 32768  # Reserved for internal use. Do not set.


class RoomSectorType(IntEnum):
    """Room sector types."""
    INSIDE = 0  # Indoors (small number of move points needed).
    CITY = 1  # The streets of a city.
    FIELD = 2  # An open field.
    FOREST = 3  # A dense forest.
    HILLS = 4  # Low foothills.
    MOUNTAIN = 5  # Steep mountain regions.
    WATER_SWIM = 6  # Water (swimmable).
    WATER_NOSWIM = 7  # Unswimmable water - boat required for passage.
    FLYING = 8  # Wheee!
    UNDERWATER = 9  # Underwater.


class RoomDoorFlag(IntEnum):
    """Room door flags."""
    NO_DOOR = 0
    DOOR = 1
    PICKPROOF = 2


class MobAction(IntFlag):
    """Mob action flags (bitvector)."""
    SPEC = 1
    # This flag must be set on mobiles which have special procedures
    # written in C.  In addition to setting this bit, the procedure must be
    # assigned in spec_assign.c, and the specproc itself must (of course)
    # must be written.  See the section on Special Procedures in the file
    # coding.doc for more information.
    SENTINEL = 2
    # Mobiles wander around randomly by default; this bit should be set
    # for mobiles which are to remain stationary.
    SCAVENGER = 4
    # The mob should pick up valuables it finds on the ground.  More
    # expensive items will be taken first.
    ISNPC = 8  # Reserved for internal use. Do not set.
    AWARE = 16
    # Set for mobs which cannot be backstabbed. Replaces the
    # ACT_NICE_THIEF bit from Diku Gamma.
    AGGRESSIVE = 32
    # Mob will hit all players in the room it can see. See also the WIMPY bit.
    STAY_ZONE = 64
    # Mob will not wander out of its own zone -- good for keeping your mobs
    # as only part of your own area.
    WIMPY = 128
    # Mob will flee when being attacked if it has less than 20% of its hit
    # points.  If the WIMPY bit is set in conjunction with any of
    # the forms of the AGGRESSIVE bit, the mob will only attack
    # mobs that are unconscious (sleeping or incapacitated).
    AGGR_EVIL = 256  # Mob will attack players that are evil-aligned.
    AGGR_GOOD = 512  # Mob will attack players that are good-aligned.
    AGGR_NEUTRAL = 1024  # Mob will attack players that are neutrally aligned.
    MEMORY = 2048
    # Mob will remember the players that initiate attacks on it, and
    # initiate an attack on that player if it ever runs into him again.
    HELPER = 4096
    # The mob will attack any player it sees in the room that is fighting
    # with a mobile in the room. Useful for groups of mobiles that travel
    # together; i.e. three snakes in a pit, to force players to fight all
    # three simultaneously instead of picking off one at a time.
    NOCHARM = 8192  # Mob cannot be charmed.
    NOSUMMON = 16384  # Mob cannot be summoned.
    NOSLEEP = 32768  # Sleep spell cannot be cast on mob.
    NOBASH = 65536  # Large mobs such as trees that cannot be bashed.
    NOBLIND = 131072  # Mob cannot be blinded.
    NOTDEADYET = 262144  # Reserved for internal use. Do not set.


class MobAffect(IntFlag):
    """Mob affect flags (bitvector)."""
    BLIND = 1  # Mob is blind.
    INVISIBLE = 2  # Mob is invisible.
    DETECT_ALIGN = 4  # Mob is sensitive to the alignment of others.
    DETECT_INVIS = 8  # Mob can see invisible characters and objects.
    DETECT_MAGIC = 16  # Mob is sensitive to magical presence.
    SENSE_LIFE = 32  # Mob can sense hidden life.
    WATERWALK = 64  # Mob can traverse unswimmable water sectors.
    SANCTUARY = 128  # Mob is protected by sanctuary (half damage).
    GROUP = 256  # Reserved for internal use. Do not set.
    CURSE = 512  # Mob is cursed.
    INFRAVISION = 1024  # Mob can see in dark.
    POISON = 2048  # Reserved for internal use. Do not set.
    PROTECT_EVIL = 4096  # Mob is protected from evil characters. No effect at present.
    PROTECT_GOOD = 8192  # Mob is protected from good characters. No effect at present.
    SLEEP = 16384  # Reserved for internal use. Do not set.
    NOTRACK = 32768  # Mob cannot be tracked.
    UNUSED16 = 65536  # Unused (room for future expansion).
    UNUSED17 = 131072  # Unused (room for future expansion).
    SNEAK = 262144  # Mob can move quietly (room not informed).
    HIDE = 524288  # Mob is hidden (only visible with sense life).
    UNUSED20 = 1048576  # Unused (room for future expansion).
    CHARM = 2097152  # Reserved for internal use. Do not set.


class MobPosition(IntEnum):
    """Mob position."""
    POSITION_DEAD = 0  # Reserved for internal use. Do not set.
    POSITION_MORTALLYW = 1  # Reserved for internal use. Do not set.
    POSITION_INCAP = 2  # Reserved for internal use. Do not set.
    POSITION_STUNNED = 3  # Reserved for internal use. Do not set.
    POSITION_SLEEPING = 4  # The monster is sleeping.
    POSITION_RESTING = 5  # The monster is resting.
    POSITION_SITTING = 6  # The monster is sitting.
    POSITION_FIGHTING = 7  # Reserved for internal use. Do not set.
    POSITION_STANDING = 8  # The monster is standing.


class MobGender(IntEnum):
    """Mob gender."""
    N = 0  # (it/its)
    M = 1  # (he/his)
    F = 2  # (she/her)


class MobEquipSlot(IntEnum):
    """Mob equipment slots."""
    LIGHT = 0  # Used as light
    RING_R = 1  # Worn on right finger
    RING_L = 2  # Worn on left finger
    NECK_1 = 3  # First object worn around neck
    NECK_2 = 4  # Second object worn around neck
    BODY = 5  # Worn on body
    HEAD = 6  # Worn on head
    LEGS = 7  # Worn on legs
    FEET = 8  # Worn on feet
    HANDS = 9  # Worn on hands
    ARMS = 10  # Worn on arms
    SHIELD = 11  # Worn as shield
    ABOUT_BODY = 12  # Worn about body
    WAIST = 13  # Worn around waist
    WRIST_R = 14  # Worn around right wrist
    WRIST_L = 15  # Worn around left wrist
    WIELD = 16  # Wielded as a weapon
    HOLD = 17  # Held


class ShopFlag(IntFlag):
    """Shop flags (bitvector)."""
    WILL_START_FIGHT = 1  # Players can try to kill shopkeeper.
    WILL_BANK_MONEY = 2  # Shopkeeper will put money over 15000 coins in the bank.


class ShopTradesWith(IntFlag):
    """Shop trades-with restrictions (bitvector)."""
    NOGOOD = 1  # Don't trade with positively-aligned players.
    NOEVIL = 2  # Don't trade with evilly-aligned players.
    NONEUTRAL = 4  # Don't trade with neutrally-aligned players.
    NOMAGIC_USER = 8  # Don't trade with the Mage class.
    NOCLERIC = 16  # Don't trade with the Cleric class.
    NOTHIEF = 32  # Don't trade with the Thief class.
    NOWARRIOR = 64  # Don't trade with the Warrior class.
