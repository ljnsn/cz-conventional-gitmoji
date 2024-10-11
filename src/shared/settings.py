"""Settings."""

from typing import List, Optional

import attrs

from commitizen import config

DEFAULT_CONVERT_PREFIXES = ["Merge", "Revert", "Squash"]


@attrs.define(kw_only=True)
class MojiSettings:
    """Settings."""

    allowed_prefixes: List[str]
    convert_prefixes: List[str] = attrs.field(factory=lambda: DEFAULT_CONVERT_PREFIXES)
    conventional_types_only: bool = False
    conventional_messages: bool = False


def get_settings(filepath: Optional[str] = None) -> MojiSettings:
    """Get settings."""
    cfg = config.read_cfg(filepath)
    fields_used = {field.name for field in attrs.fields(MojiSettings)}
    return MojiSettings(**{k: v for k, v in cfg.settings.items() if k in fields_used})  # type: ignore[arg-type]
