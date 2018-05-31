# coding: utf-8
import json
import logging
import os

import click

from mobile import parse_mob
from object import parse_object
from room import parse_room
from shop import parse_shop
from zone import parse_zone
from utils import parse_from_file
from utils import split_on_vnums

PARSER_LOOKUP = {
    'mob': (parse_mob, split_on_vnums, None),
    'obj': (parse_object, split_on_vnums, None),
    'wld': (parse_room, split_on_vnums, None),
    'shp': (parse_shop, split_on_vnums, None),
    'zon': (parse_zone, split_on_vnums, None),
}


def indent(text):
    lines = text.split('\n')
    indented = ['\t' + line for line in lines]
    new_text = '\n'.join(indented)
    return new_text


def log_errors(errors):
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    logger = logging.getLogger(__name__)

    for error in errors:
        text, trace = indent(error['text']), indent(error['trace'])
        logger.error('Error parsing:\n\n%s\n%s', text, trace)


def get_file_type(filepath):
    _, filename = os.path.split(filepath)
    _, file_type = filename.split('.')
    return file_type


def parse_based_on_filepath(filepath):
    # figure out which type of tinyworld file we've been pointed at
    file_type = get_file_type(filepath)

    if file_type not in PARSER_LOOKUP:
        fmt = 'No parser found for file type: "{}"'
        raise RuntimeError(fmt.format(file_type))

    args = PARSER_LOOKUP[file_type]
    payload, errors = parse_from_file(filepath, *args)

    return payload, errors


@click.command()
@click.option('--dest', default=None, help='output to file')
@click.argument('src')
def parse(src, dest):
    payload, errors = parse_based_on_filepath(src)
    log_errors(errors)

    payload_json = json.dumps(payload, indent=2, sort_keys=True)

    if dest:
        with open(dest, 'w') as f:
            f.write(payload_json)
    else:
        click.echo(payload_json)


if __name__ == '__main__':
    parse()
