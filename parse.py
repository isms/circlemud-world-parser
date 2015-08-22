import json
import os

import click

from mobile import parse_mob
from object import parse_object
from room import parse_room
from shop import parse_shop
from zone import parse_zone
from utils import parse_from_file
from utils import split_on_vnums


def get_file_type(filepath):
    _, filename = os.path.split(filepath)
    _, file_type = filename.split('.')
    return file_type


def parse_based_on_filepath(filepath):
    lookup = {
        'mob': (parse_mob, split_on_vnums, None),
        'obj': (parse_object, split_on_vnums, None),
        'wld': (parse_room, split_on_vnums, None),
        'shp': (parse_shop, split_on_vnums, None),
        'zon': (parse_zone, split_on_vnums, None),
    }

    # figure out which type of Tinyworld file we've been pointed at
    file_type = get_file_type(filepath)

    if file_type not in lookup:
        fmt = 'No parser found for file type: "{}"'
        raise RuntimeError(fmt.format(file_type))

    args = lookup[file_type]
    payload, errors = parse_from_file(filepath, *args)

    return payload, errors


@click.command()
@click.option('--output', default=None, help='output to file')
@click.argument('src')
def parse(src, output):
    payload, errors = parse_based_on_filepath(src)
    payload_json = json.dumps(payload, indent=2, sort_keys=True)

    if output:
        with open(output, 'w') as f:
            f.write(payload_json)
    else:
        click.echo(payload_json)


if __name__ == '__main__':
    parse()
