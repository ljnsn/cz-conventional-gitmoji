import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

from shared.model import Gitmoji
from shared.settings import get_settings
from shared.utils import get_gitmojis, get_pattern


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
        "--convert-prefixes",
        nargs="*",
        help="prefixes to convert to gitmoji format",
    )
    return parser.parse_args()


def _grouped_gitmojis() -> Dict[str, Gitmoji]:
    """Return the gitmojis grouped by type."""
    return {moji.type: moji for moji in get_gitmojis()}


def gitmojify(
    message: str,
    allowed_prefixes: Optional[List[str]] = None,
    convert_prefixes: Optional[List[str]] = None,
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
        convert_prefixes: Prefixes that should be converted to gitmoji format.

    Returns:
        The gitmojified message.
    """
    convert_prefixes = convert_prefixes or []
    if any(map(message.startswith, convert_prefixes)):
        first_word, *rest = message.split(" ", maxsplit=1)
        if first_word.endswith(":"):
            first_word = first_word[:-1]
        if first_word in convert_prefixes:
            message = f"{first_word.lower()}: {''.join(rest)}"
    if any(map(message.startswith, allowed_prefixes or [])):
        return message

    pat = get_pattern()
    match = re.match(pat, message)
    if match is None:
        msg = "invalid commit message"
        raise ValueError(msg)
    gtype = match.group("type_group")
    if " " in gtype:  # maybe do a better check?
        return message
    icon = _grouped_gitmojis()[gtype].icon
    return f"{icon} {message}"


def _write(filepath: Optional[Path], message: str, encoding: str) -> None:
    """Write the message to the file."""
    if filepath is None:
        sys.stdout.write(message)
        return
    with filepath.open("w", encoding=encoding) as f:
        f.write(message)


def _filter_comments(message: str) -> str:
    """Filter out comments from the message.

    Copied from https://github.com/commitizen-tools/commitizen/blob/a54bf542012257a338edb54ca16d11ba6beef0ba/commitizen/commands/check.py#L113-L141
    """
    lines = []
    for line in message.split("\n"):
        if "# ------------------------ >8 ------------------------" in line:
            break
        if not line.startswith("#"):
            lines.append(line)
    return "\n".join(lines)


def run() -> None:
    """The pre-commit hook that modifies the commit message."""
    args = _get_args()
    settings = get_settings(args.config)
    if args.commit_msg_file:
        filepath = Path(args.commit_msg_file)
        msg = filepath.read_text(encoding=settings.encoding)
    else:
        filepath = None
        msg = args.message
    _write(
        filepath,
        gitmojify(
            _filter_comments(msg),
            args.allowed_prefixes or settings.allowed_prefixes,
            args.convert_prefixes or settings.convert_prefixes,
        ),
        settings.encoding,
    )
