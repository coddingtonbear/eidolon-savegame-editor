import argparse
import logging

from .savegame import Savegame
from .commands import COMMANDS


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path', metavar='/path/to/savegame/', type=str,
        help="Path to your savegame file."
    )
    parser.add_argument(
        'command', metavar='COMMAND', type=str,
        choices=COMMANDS.keys(),
        help="What do you want to do?",
    )
    parser.add_argument(
        "--loglevel",
        help=(
            "Logging verbosity level; set to 'DEBUG' to see "
            "all logging messages"
        ),
        default='INFO',
    )
    parser.add_argument(
        "--no-backup",
        action='store_false',
        default=True,
        dest='backup',
        help=(
            "Do not automatically create a backup file before performing "
            "an edit."
        )
    )
    args, extra = parser.parse_known_args()
    command = args.command

    logging.basicConfig(
        level=logging.getLevelName(args.loglevel)
    )
    save = Savegame(args.path)

    COMMANDS[command](save, extra=extra, backup=args.backup)
