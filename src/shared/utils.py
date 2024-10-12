from typing import List

from shared.model import Gitmoji
from shared.spec import mojis

# global pattern to validate commit messages
PATTERN = (
    r"(?s)"
    r"(?P<type_group>{type_group})"
    r"(?P<scope>(\(\S+\))?!?:)"
    r"(?P<subject>( [^\n\r]+))"
    r"(?P<body>((\n\n.*)|(\s*))?$)"
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
