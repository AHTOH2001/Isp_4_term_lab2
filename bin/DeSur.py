#!usr/bin/python3

import argparse
import logging
import os
import sys

from DeSurLib import fabric

parser = argparse.ArgumentParser(description='Convert file to other format')
parser.add_argument('file_path', help='path to the file that will be converted')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--json', '-j', action="store_true")
group.add_argument('--pickle', '-p', action="store_true")
group.add_argument('--toml', '-t', action="store_true")
group.add_argument('--yaml', '-y', action="store_true")


# parser.add_argument('file', help='path to the file that will be converted')

def convert(file_path, new_format):
    if not os.path.exists(file_path):
        logging.error(f'file {file_path} not found')
        sys.exit(1)

    filename, file_extension = os.path.splitext(file_path)
    try:
        serializer_old = fabric.create_serialzer(file_extension[1:])
    except NameError:
        logging.error('file extension should be one of the supported formats')
        sys.exit(1)

    serializer_new = fabric.create_serialzer(new_format)
    if serializer_old.__class__ is serializer_new.__class__:
        logging.error('formats are equal, no need to convert')
        sys.exit(1)

    with open(file_path, serializer_old.read_type) as fp:
        loaded_obj = serializer_old.load(fp)

    with open(f'{filename}.{serializer_new.__class__.__name__.lower()}', serializer_new.write_type) as fp:
        serializer_new.dump(loaded_obj, fp)

    os.remove(file_path)
    logging.info('convertation successful!')


args = parser.parse_args()
if args.json:
    convert(args.file_path, 'json')
elif args.pickle:
    convert(args.file_path, 'pickle')
elif args.toml:
    convert(args.file_path, 'toml')
elif args.yaml:
    convert(args.file_path, 'yaml')
