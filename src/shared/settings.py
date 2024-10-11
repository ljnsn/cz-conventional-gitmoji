"""Settings."""

from typing import Any, Dict, List, Optional, Tuple

import attrs

from commitizen.defaults import CzSettings
from commitizen import config

DEFAULT_CONVERT_PREFIXES = ["Merge", "Revert", "Squash"]


@attrs.define(kw_only=True)
class MojiSettings:
    """Settings."""

    name: str
    version: Optional[str]
    version_files: List[str]
    version_provider: Optional[str]
    version_scheme: Optional[str]
    version_type: Optional[str] = None
    tag_format: str
    bump_message: Optional[str]
    retry_after_failure: bool
    allow_abort: bool
    allowed_prefixes: List[str]
    convert_prefixes: List[str] = attrs.field(factory=lambda: DEFAULT_CONVERT_PREFIXES)
    changelog_file: str
    changelog_format: Optional[str]
    changelog_incremental: bool
    changelog_start_rev: Optional[str]
    changelog_merge_prerelease: bool
    update_changelog_on_bump: bool
    use_shortcuts: bool
    style: Optional[List[Tuple[str, str]]] = None
    customize: Optional[CzSettings] = None
    major_version_zero: bool
    pre_bump_hooks: Optional[List[str]]
    post_bump_hooks: Optional[List[str]]
    prerelease_offset: int
    encoding: str
    always_signoff: bool
    template: Optional[str]
    extras: Dict[str, Any]
    conventional_types_only: bool = False
    conventional_messages: bool = False


def get_settings(filepath: Optional[str] = None) -> MojiSettings:
    """Get settings."""
    cfg = config.read_cfg(filepath)
    return MojiSettings(**cfg.settings)
