OBJECT_TYPE_FLAGS = {
    1: 'LIGHT',  # Item is a light source.
    2: 'SCROLL',  # Item is a magical scroll.
    3: 'WAND',  # Item is a magical wand.
    4: 'STAFF',  # Item is a magical staff.
    5: 'WEAPON',  # Item is a weapon.
    6: 'FIREWEAPON',  # Currently not implemented.  Do not use.
    7: 'MISSILE',  # Currently not implemented.  Do not use.
    8: 'TREASURE',  # Item is treasure other than gold coins (e.g. gems).
    9: 'ARMOR',  # Item is armor.
    10: 'POTION',  # Item is a magical potion.
    11: 'WORN',  # Currently not implemented.  Do not use.
    12: 'OTHER',  # Miscellaneous object with no special properties.
    13: 'TRASH',  # Trash -- junked by cleaners, not bought by shopkeepers.
    14: 'TRAP',  # Currently not implemented.  Do not use.
    15: 'CONTAINER',  # Item is a container.
    16: 'NOTE',  # Item is a note (can be written on).
    17: 'DRINKCON',  # Item is a drink container.
    18: 'KEY',  # Item is a key.
    19: 'FOOD',  # Item is food.
    20: 'MONEY',  # Item is money (gold coins).
    21: 'PEN',  # Item is a pen.
    22: 'BOAT',  # Item is a boat; allows you to traverse SECT_WATER_NOSWIM.
    23: 'FOUNTAIN',  # Item is a fountain.
}

OBJECT_EXTRA_EFFECTS_FLAGS = {
    1: 'GLOW',  # Item is glowing (cosmetic).
    2: 'HUM',  # Item is humming (cosmetic).
    4: 'NORENT',  # Item cannot be rented.
    8: 'NODONATE',  # Item cannot be donated.
    16: 'NOINVIS',  # Item cannot be made invisible.
    32: 'INVISIBLE',  # Item is invisible.
    64: 'MAGIC',  # Item has a magical aura and can't be enchanted.
    128: 'NODROP',  # Item is cursed and cannot be dropped.
    256: 'BLESS',  # Item is blessed (cosmetic).
    512: 'ANTI_GOOD',  # Item can't be used by good-aligned characters.
    1024: 'ANTI_EVIL',  # Item can't be used by evil-aligned characters.
    2048: 'ANTI_NEUTRAL',  # Item can't be used by neutrally- aligned characters.
    4096: 'ANTI_MAGIC_USER',  # Item can't be used by the Mage class.
    8192: 'ANTI_CLERIC',  # Item can't be used by the Cleric class.
    16384: 'ANTI_THIEF',  # Item can't be used by the Thief class.
    32768: 'ANTI_WARRIOR',  # Item can't be used by the Warrior class.
    65536: 'NOSELL',  # Shopkeepers will not buy or sell the item.
}

OBJECT_WEAR_FLAGS = {
    1: 'WEAR_TAKE',  # Item can be taken (picked up off the ground).
    2: 'WEAR_FINGER',  # Item can be worn on the fingers.
    4: 'WEAR_NECK',  # Item can be worn around the neck.
    8: 'WEAR_BODY',  # Item can be worn on the body.
    16: 'WEAR_HEAD',  # Item can be worn on the head.
    32: 'WEAR_LEGS',  # Item can be worn on the legs.
    64: 'WEAR_FEET',  # Item can be worn on the feet.
    128: 'WEAR_HANDS',  # Item can be worn on the hands.
    256: 'WEAR_ARMS',  # Item can be worn on the arms.
    512: 'WEAR_SHIELD',  # Item can be used as a shield.
    1024: 'WEAR_ABOUT',  # Item can be worn about the body.
    2048: 'WEAR_WAIST',  # Item can be worn around the waist.
    4096: 'WEAR_WRIST',  # Item can be worn around the wrist.
    8192: 'WEAR_WIELD',  # Item can be wielded; e.g. weapons.
    16384: 'WEAR_HOLD',  # Item can be held (the 'hold' command).
}

OBJECT_AFFECT_LOCATION_FLAGS = {
    0: 'NONE',  # No effect (typically not used).
    1: 'STR',  # Apply to strength.
    2: 'DEX',  # Apply to dexterity.
    3: 'INT',  # Apply to intelligence.
    4: 'WIS',  # Apply to wisdom.
    5: 'CON',  # Apply to constitution.
    6: 'CHA',  # Apply to charisma.
    7: 'CLASS',  # Unimplemented.  Do not use.
    8: 'LEVEL',  # Unimplemented.  Do not use.
    9: 'AGE',  # Apply to character's MUD age, in MUD years.
    10: 'CHAR_WEIGHT',  # Apply to weight.
    11: 'CHAR_HEIGHT',  # Apply to height.
    12: 'MANA',  # Apply to MAX mana points.
    13: 'HIT',  # Apply to MAX hit points.
    14: 'MOVE',  # Apply to MAX movement points.
    15: 'GOLD',  # Unimplemented.  Do not use.
    16: 'EXP',  # Unimplemented.  Do not use.
    17: 'AC',  # Apply to armor class (AC).
    18: 'HITROLL',  # Apply to hitroll.
    19: 'DAMROLL',  # Apply to damage roll bonus.
    20: 'SAVING_PARA',  # Apply to save throw: paralyze
    21: 'SAVING_ROD',  # Apply to save throw: rods
    22: 'SAVING_PETRI',  # Apply to save throw: petrif
    23: 'SAVING_BREATH',  # Apply to save throw: breath
    24: 'SAVING_SPELL',  # Apply to save throw: spells
}