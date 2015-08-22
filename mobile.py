# coding: utf-8
from constants import MOB_ACTION_FLAGS
from constants import MOB_AFFECT_FLAGS
from constants import MOB_GENDER
from constants import MOB_POSITION
from utils import bitvector_to_flags
from utils import clean_bitvector
from utils import lookup_value_to_dict


def parse_dice_roll_string_to_tuple(roll_string):
    """
    given a dice roll string, e.g. 4d6+20, return tuple of number of dice,
    number sides of each die, bonus, e.g. (4, 6, 20)
    """
    dice, bonus = roll_string.split('+')
    dice, sides = dice.split('d')
    result = map(int, (dice, sides, bonus))
    return result


def parse_dice_roll_string_to_dict(roll_string):
    """
    given a dice roll string such as "4d6+20", return dict of number of dice,
    number sides of each die, and bonus:
        {
            "dice": 4,{}
            "sides": 6,
            "bonus": 20
        }
    """
    names = ['dice', 'sides', 'bonus']
    values = parse_dice_roll_string_to_tuple(roll_string)
    return dict(zip(names, values))


def parse_mob(text):
    fields = [line.rstrip() for line in text.strip().split('\n')]

    d = dict()
    d['id'] = int(fields[0])
    d['aliases'] = fields[1].rstrip('~').split()
    d['short_desc'] = fields[2].rstrip('~')
    d['long_desc'] = text.split('~')[2].strip('\n')
    d['detail_desc'] = text.split('~')[3].strip('\n')

    tildes = [i for i, a in enumerate(text) if a == '~']
    start_bottom_matter = tildes[3] + 1
    bottom_fields = text[start_bottom_matter:].strip('\n').split('\n')

    vector_line = bottom_fields[0]
    action, affect, alignment, mob_type = vector_line.split()

    d['mob_type'] = mob_type
    d['alignment'] = int(alignment)

    action = clean_bitvector(action)
    d['action_flags'] = bitvector_to_flags(action, MOB_ACTION_FLAGS)

    affect = clean_bitvector(affect)
    d['affect_flags'] = bitvector_to_flags(affect, MOB_AFFECT_FLAGS)

    level, thac0, ac, max_hp, bare_hand_dmg = bottom_fields[1].split()
    gold, xp = bottom_fields[2].split()
    load_position, default_position, gender = bottom_fields[3].split()

    d['level'] = int(level)
    d['thac0'] = int(thac0)
    d['armor_class'] = int(ac)
    d['max_hit_points'] = parse_dice_roll_string_to_dict(max_hp)
    d['bare_hand_damage'] = parse_dice_roll_string_to_dict(bare_hand_dmg)
    d['gold'] = int(gold)
    d['xp'] = int(xp)
    d['position'] = {
        'load': lookup_value_to_dict(int(load_position), MOB_POSITION),
        'default': lookup_value_to_dict(int(load_position), MOB_POSITION)
    }
    d['gender'] = lookup_value_to_dict(int(gender), MOB_GENDER)

    extra_spec = dict()
    if len(bottom_fields) > 4:
        assert mob_type == 'E'
        assert bottom_fields[-1] == 'E'

        for line in bottom_fields[4:]:
            if line == 'E':
                break  # we reached the end of this E-type mob
            key, value = line.split(': ')
            extra_spec[key] = int(value)
    d['extra_spec'] = extra_spec

    return d
