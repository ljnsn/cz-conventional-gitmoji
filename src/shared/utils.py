from typing import List

from shared.model import Gitmoji
from shared.spec import mojis

# global pattern to validate commit messages
PATTERN = (
    # To explictly make . match new line
    r"(?s)"
    # gitmoji and type
    r"({type_group})"
    # scope
    r"(\(\S+\))?!?:"
    # subject
    r"( [^\n\r]+)"
    # body
    r"((\n\n.*)|(\s*))?$"
)


def get_gitmojis() -> List[Gitmoji]:
    """Return the list of Gitmoji objects."""
    return [Gitmoji(**moji) for moji in mojis]


def get_type_group_pattern() -> str:
    """Return the type group pattern."""
    return "|".join([f"({moji.icon} {{1,2}})?{moji.type}" for moji in get_gitmojis()])


def get_pattern() -> str:
    """Return the complete validation pattern."""
    type_group = get_type_group_pattern()
    return PATTERN.format(type_group=type_group)
