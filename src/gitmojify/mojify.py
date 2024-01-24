import argparse
import re
import sys
from pathlib import Path
from typing import Dict

from shared.model import Gitmoji
from shared.utils import get_gitmojis, get_pattern


def get_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--commit-msg-file")
    group.add_argument("-m", "--message")
    return parser.parse_args()


def grouped_gitmojis() -> Dict[str, Gitmoji]:
    """Return the gitmojis grouped by type."""
    return {moji.type: moji for moji in get_gitmojis()}


def gitmojify(message: str) -> str:
    """
    Gitmojify the commit message.

    If a gitmoji is already present in the message, the message is returned
    as is. Otherwise, the gitmoji is looked up by type and is prepended to
    the message.

    Args:
        message: The complete commit message.

    Returns:
        The gitmojified message.
    """
    pat = re.compile(get_pattern())
    match = pat.match(message)
    if match is None:
        raise ValueError("invalid commit message")
    gtype = match.group(1)
    if " " in gtype:  # maybe do a better check?
        return message
    icon = grouped_gitmojis()[gtype].icon
    return f"{icon} {message}"


def run() -> None:
    """The pre-commit hook that modifies the commit message."""
    args = get_args()
    if args.commit_msg_file:
        filepath = Path(args.commit_msg_file)
        msg = filepath.read_text()
        with filepath.open("w", encoding="utf-8") as f:
            f.write(gitmojify(msg))
    else:
        msg = args.message
        sys.stdout.write(gitmojify(msg))
