# coding: utf-8
import json
import logging
import os
from typing import Optional

import typer

from .mobile import Mobile
from .object import Object
from .room import Room
from .shop import Shop
from .zone import Zone
from .utils import parse_from_file
from .utils import split_on_vnums

app = typer.Typer()

PARSER_LOOKUP = {
    'mob': (Mobile.parse_raw, split_on_vnums, None),
    'obj': (Object.parse_raw, split_on_vnums, None),
    'wld': (Room.parse_raw, split_on_vnums, None),
    'shp': (Shop.parse_raw, split_on_vnums, None),
    'zon': (Zone.parse_raw, split_on_vnums, None),
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


@app.command()
def parse(
    src: str = typer.Argument(..., help="source file to parse"),
    dest: Optional[str] = typer.Option(None, help="output to file"),
):
    payload, errors = parse_based_on_filepath(src)
    log_errors(errors)

    payload_dicts = [item.model_dump() for item in payload]
    payload_json = json.dumps(payload_dicts, indent=2, sort_keys=True)

    if dest:
        with open(dest, 'w') as f:
            f.write(payload_json)
    else:
        print(payload_json)


if __name__ == '__main__':
    app()
