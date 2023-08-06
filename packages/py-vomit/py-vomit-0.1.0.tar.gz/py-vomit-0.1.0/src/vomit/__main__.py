import os
import sys
import argparse
from typing import Callable

from vomit import to_unicode, to_utf8


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='python -m vomit')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encode', action='store_true', help='indicate the file should be encoded')
    group.add_argument('-d', '--decode', action='store_true', help='indicate the file should be decoded')

    parser.add_argument('-f', '--file', type=str, help='the file to encode or decode, default to stdin')
    parser.add_argument('-o', '--out', type=str, help='the output destination, default to stdout')
    return parser


def _output(code: str, dest: str):
    if not dest:
        print(code)
        return

    with open(dest, 'w') as f:
        f.write(code)


def _input(action: Callable[[str], str], src: str) -> str:
    if not src:
        code = ''.join(line for line in sys.stdin)
        return action(code)

    with open(src, 'r') as f:
        code = f.read()
        return action(code)


if __name__ == '__main__':
    args = _parser().parse_args()

    if args.file and not os.path.exists(args.file):
        print(f'file "{args.file}" not found')
        os._exit(1)

    if args.file and not os.path.isfile(args.file):
        print(f'"{args.file}" not a file')
        os._exit(1)

    action = to_unicode if args.encode else to_utf8
    code = _input(action, args.file or "")
    _output(code, args.out or "")
