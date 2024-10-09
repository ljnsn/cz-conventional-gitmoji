import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List

from commitizen import config

from shared.model import Gitmoji
from shared.utils import get_gitmojis, get_pattern

UTF8 = "utf-8"


def get_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-f",
        "--commit-msg-file",
        help="path to the commit message file",
    )
    group.add_argument("-m", "--message", help="the commit message")
    parser.add_argument("--config", help="path to the configuration file")
    parser.add_argument(
        "--allowed-prefixes",
        nargs="*",
        help="allowed gitmoji prefixes",
    )
    parser.add_argument(
        "--convert",
        action="store_true",
        default=False,
        help="convert allowed prefixes to gitmoji format",
    )
    return parser.parse_args()


def grouped_gitmojis() -> Dict[str, Gitmoji]:
    """Return the gitmojis grouped by type."""
    return {moji.type: moji for moji in get_gitmojis()}


def gitmojify(message: str, allowed_prefixes: List[str], *, convert: bool) -> str:
    """
    Gitmojify the commit message.

    If a gitmoji is already present in the message, the message is returned
    as is. Otherwise, the gitmoji is looked up by type and is prepended to
    the message.

    Args:
        message: The complete commit message.
        allowed_prefixes: Prefixes that should not raise an error, even though
            they're not following conventional standard.
        convert: Whether to convert the allowed prefixes to gitmoji format.

    Returns:
        The gitmojified message.
    """
    if any(map(message.startswith, allowed_prefixes)):
        if convert:
            first_word, *rest = message.split()
            message = f"{first_word.lower()}: {' '.join(rest)}"
        else:
            return message

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
    cz_cfg = config.read_cfg(args.config)
    allowed_prefixes = args.allowed_prefixes or cz_cfg.settings["allowed_prefixes"]
    if args.commit_msg_file:
        filepath = Path(args.commit_msg_file)
        # TODO: commit message file encoding can be set via git config
        # key 'i18n.commitEncoding' and defaults to UTF-8, get encoding
        # from there.
        msg = filepath.read_text(encoding=UTF8)
        with filepath.open("w", encoding=UTF8) as f:
            f.write(gitmojify(msg, allowed_prefixes, convert=args.convert))
    else:
        msg = args.message
        sys.stdout.write(gitmojify(msg, allowed_prefixes, convert=args.convert))
