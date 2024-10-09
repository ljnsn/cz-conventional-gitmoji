import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

from commitizen import config
from commitizen.exceptions import ConfigFileNotFound

from shared.model import Gitmoji
from shared.utils import get_gitmojis, get_pattern

UTF8 = "utf-8"


def _get_args() -> argparse.Namespace:
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


def _grouped_gitmojis() -> Dict[str, Gitmoji]:
    """Return the gitmojis grouped by type."""
    return {moji.type: moji for moji in get_gitmojis()}


def gitmojify(
    message: str,
    allowed_prefixes: Optional[List[str]] = None,
    *,
    convert: bool = False,
) -> str:
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
    if any(map(message.startswith, allowed_prefixes or [])):
        if convert:
            first_word, *rest = message.split()
            if first_word.endswith(":"):
                first_word = first_word[:-1]
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
    icon = _grouped_gitmojis()[gtype].icon
    return f"{icon} {message}"


def _get_allowed_prefixes(args: argparse.Namespace) -> List[str]:
    """Return the allowed prefixes."""
    if args.allowed_prefixes:
        return args.allowed_prefixes
    try:
        cfg = config.read_cfg(args.config)
    except ConfigFileNotFound:
        return []
    return cfg.settings["allowed_prefixes"]


def run() -> None:
    """The pre-commit hook that modifies the commit message."""
    args = _get_args()
    allowed_prefixes = _get_allowed_prefixes(args)
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
