# coding: utf-8
import json
import os
import re
import sys

from constants import MOB_EQUIP
from utils import parse_from_file

COMMAND_RE = r'(\d+)'
COMMAND_PATTERN = re.compile(COMMAND_RE)


def get_command_fields(command, n_fields=4):
    results = COMMAND_PATTERN.findall(command)
    fields = map(int, results[:n_fields])
    return fields


def parse_commands(commands, d):
    commands = iter(commands)

    mobs = []
    objects = []
    remove_objects = []
    doors = []

    while True:
        curr = next(commands)

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
            eq = dict(location=location, max=max, object=obj, note=note)
            mobs[-1]['equipped'].append(eq)

        # put an object in a mob's inventory
        elif curr.startswith('G'):
            _, obj, max = get_command_fields(curr, 3)
            inv = dict(max=max, object=obj)

            # give the object to the most recently parsed mob
            mobs[-1]['inventory'].append(inv)

        # load an object in a room
        elif curr.startswith('O'):
            _, obj, max, room = get_command_fields(curr)
            obj = dict(max=max, object=obj, room=room, contents=list())
            objects.append(obj)

        # put an object in another object
        elif curr.startswith('P'):
            _, contents, max, container = get_command_fields(curr)
            put = dict(object=contents, max=max)

            # sanity check to make sure last object is the expected container
            assert container == objects[-1]['object']

            # put the contained object into the most recently parsed object
            objects[-1]['contents'].append(put)

        # set the state of a door
        elif curr.startswith('D'):
            _, room, exit, state = get_command_fields(curr)
            door = dict(room=room, exit=exit, state=state)
            doors.append(door)

        # remove an object from a room
        elif curr.startswith('R'):
            _, room, obj = get_command_fields(curr, 3)
            remove = dict(room=room, object=obj)
            remove_objects.append(remove)

    d['mobs'] = mobs
    d['objects'] = objects
    d['doors'] = doors
    d['remove_objects'] = remove_objects

    return d


def parse_zone(text):
    d = {}

    fields = [line.rstrip() for line in text.strip().split('\n')]

    # remove comment lines
    actual_line = lambda line: not line.startswith('*')
    fields = filter(actual_line, fields)

    d['vnum'] = int(fields[0])
    d['name'] = fields[1].rstrip('~')

    bottom, top, lifespan, reset_mode = map(int, fields[2].split())
    d['bottom_room'] = bottom
    d['top_room'] = top
    d['lifespan'] = lifespan
    d['reset_mode'] = reset_mode

    commands = fields[3:]
    d = parse_commands(commands, d)

    return d


if __name__ == '__main__':
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        print('Usage: python object_parser.py [file]')
        sys.exit(1)

    filename = sys.argv[1]
    dicts = parse_from_file(filename, parse_zone)
    payload = json.dumps(dicts, indent=2, sort_keys=True)
    print(payload)
