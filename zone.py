# coding: utf-8
import re

from constants import MOB_EQUIP

COMMAND_RE = r'(\d+)'
COMMAND_PATTERN = re.compile(COMMAND_RE)


def get_command_fields(command, n_fields=4):
    results = COMMAND_PATTERN.findall(command)
    fields = [int(r) for r in results[:n_fields]]
    return fields


def get_contents(commands, i, curr_obj):
    # get the current container
    contents = []

    i += 1
    while i < len(commands) and commands[i].startswith('P'):
        _, new_object, max, container = get_command_fields(commands[i])

        # only append object if the listed container is th
        if container == curr_obj:
            subcontents = get_contents(commands, i, new_object)
            to_append = dict(id=new_object, max=max, contents=subcontents)
            contents.append(to_append)

        i += 1

    return contents


def parse_commands(commands, d):
    mobs = []
    objects = []
    remove_objects = []
    doors = []

    for i, curr in enumerate(commands):

        if curr == 'S':
            break  # we're done

        # load a mob in a room
        elif curr.startswith('M'):
            _, mob, max, room = get_command_fields(curr)
            mobs.append(dict(mob=mob, max=max, room=room,
                             inventory=[], equipped=[]))

        # equip a mob with an object
        elif curr.startswith('E'):
            _, obj, max, location = get_command_fields(curr)
            note = MOB_EQUIP.get(location, None)
            contents = get_contents(commands, i, obj)
            new_obj = dict(location=location, max=max, id=obj,
                           note=note, contents=contents)
            mobs[-1]['equipped'].append(new_obj)

        # put an object in a mob's inventory
        elif curr.startswith('G'):
            _, obj, max = get_command_fields(curr, 3)
            contents = get_contents(commands, i, obj)
            new_obj = dict(max=max, id=obj, contents=contents)

            # give the object to the most recently parsed mob
            mobs[-1]['inventory'].append(new_obj)

        # load an object in a room
        elif curr.startswith('O'):
            _, obj, max, room = get_command_fields(curr)
            contents = get_contents(commands, i, obj)
            new_obj = dict(max=max, id=obj, room=room, contents=contents)
            objects.append(new_obj)

        # set the state of a door
        elif curr.startswith('D'):
            _, room, exit, state = get_command_fields(curr)
            door = dict(room=room, exit=exit, state=state)
            doors.append(door)

        # remove an object from a room
        elif curr.startswith('R'):
            _, room, obj = get_command_fields(curr, 3)
            remove = dict(room=room, id=obj)
            remove_objects.append(remove)

    d['mobs'] = mobs
    d['objects'] = objects
    d['doors'] = doors
    d['remove_objects'] = remove_objects

    return d


def parse_zone(text):
    d = dict()

    fields = [line.rstrip() for line in text.strip().split('\n')]

    # remove comment lines
    actual_line = lambda line: not line.startswith('*')
    fields = [f for f in fields if actual_line(f)]

    d['id'] = int(fields[0])
    d['name'] = fields[1].rstrip('~')

    bottom, top, lifespan, reset_mode = map(int, fields[2].split())
    d['bottom_room'] = bottom
    d['top_room'] = top
    d['lifespan'] = lifespan
    d['reset_mode'] = reset_mode

    commands = fields[3:]
    d = parse_commands(commands, d)

    return d
