"""Gitmoji commitizen style."""

__all__ = ("CommitizenGitmojiCz",)

import re
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List

from commitizen.cz.base import BaseCommitizen
from commitizen.cz.utils import multiple_line_breaker, required_validator
from commitizen.defaults import MAJOR, MINOR, PATCH

from shared import utils
from shared.gitmojis import *


def parse_scope(text: str) -> str:
    if not text:
        return ""

    scope = text.strip().split()
    return "-".join(scope)


def parse_subject(text: str) -> str:
    if isinstance(text, str):
        text = text.strip(".").strip()

    return required_validator(text, msg="Subject is required.")


class CommitizenGitmojiCz(BaseCommitizen):
    # pattern to match messages for bumping
    # if none of these match, version will not be bumped (unless manually specified)
    bump_pattern = (
        rf"^((BREAKING[\-\ ]CHANGE"
        rf"|{GJ_BOOM}? ?boom"
        rf"|{GJ_FEAT}? ?feat"
        rf"|{GJ_FIX}? ?fix"
        rf"|{GJ_HOTFIX}? ?hotfix"
        rf"|{GJ_REFACTOR}? +refactor"
        rf"|{GJ_PERF}? ?perf)"
        r"(\(.+\))?"  # scope
        r"!?):"  # breaking
    )
    # map types to SemVer
    bump_map = OrderedDict(
        (
            (r"^.+!$", MAJOR),
            (r"^BREAKING[\-\ ]CHANGE", MAJOR),
            (rf"^{GJ_BOOM}? ?boom", MAJOR),
            (rf"^{GJ_FEAT}? ?feat", MINOR),
            (rf"^{GJ_FIX}? ?fix", PATCH),
            (rf"^{GJ_HOTFIX}? ?hotfix", PATCH),
            (rf"^{GJ_REFACTOR}? ?refactor", PATCH),
            (rf"^{GJ_PERF}? ?perf", PATCH),
        )
    )
    bump_map_major_version_zero = OrderedDict(
        (
            (r"^.+!$", MINOR),
            (r"^BREAKING[\-\ ]CHANGE", MINOR),
            (rf"^{GJ_BOOM}? ?boom", MINOR),
            (rf"^{GJ_FEAT}? ?feat", MINOR),
            (rf"^{GJ_FIX}? ?fix", PATCH),
            (rf"^{GJ_HOTFIX}? ?hotfix", PATCH),
            (rf"^{GJ_REFACTOR}? ?refactor", PATCH),
            (rf"^{GJ_PERF}? ?perf", PATCH),
        )
    )
    # parse information for generating the change log
    commit_parser = (
        rf"^(?P<change_type>{utils.get_type_group_pattern()}|BREAKING CHANGE)"
        r"(?:\((?P<scope>[^()\r\n]*)\)|\()?(?P<breaking>!)?:\s(?P<message>.*)?"
    )
    # exclude from changelog
    changelog_pattern = (
        rf"^(?!{GJ_INIT}? ?init)(?!{GJ_MERGE}? ?merge)(?!{GJ_BUMP}? ?bump).*"
    )
    # map types to changelog sections
    change_type_map = {
        # boom
        f"{GJ_BOOM} boom": f"{GJ_BOOM} Boom",
        # features
        f"{GJ_FEAT} feat": f"{GJ_FEAT} Features",
        # fixes
        f"{GJ_FIX} fix": f"{GJ_FIX}{GJ_HOTFIX} Fixes",
        f"{GJ_HOTFIX} hotfix": f"{GJ_FIX}{GJ_HOTFIX} Fixes",
        # security
        f"{GJ_SECURITY} security": f"{GJ_SECURITY} Security",
        # license
        f"{GJ_LICENSE} license": f"{GJ_LICENSE} License",
        # refactorings
        f"{GJ_REFACTOR} refactor": f"{GJ_REFACTOR} Refactorings",
        # style & architecture
        f"{GJ_STYLE} style": f"{GJ_STYLE}{GJ_ARCH} Style & Architecture",
        f"{GJ_ARCH} arch": f"{GJ_STYLE}{GJ_ARCH} Style & Architecture",
        # performance
        f"{GJ_PERF} perf": f"{GJ_PERF} Performance",
        # docs
        f"{GJ_DOCS} docs": f"{GJ_DOCS}{GJ_SOURCE_DOCS} Documentation",
        f"{GJ_SOURCE_DOCS} source-docs": f"{GJ_DOCS}{GJ_SOURCE_DOCS} Documentation",
        # tests
        f"{GJ_TEST} test": f"{GJ_TEST}{GJ_MOCK}{GJ_TEST_FAIL} Tests",
        f"{GJ_MOCK} mock": f"{GJ_TEST}{GJ_MOCK}{GJ_TEST_FAIL} Tests",
        f"{GJ_TEST_FAIL} test-fail": f"{GJ_TEST}{GJ_MOCK}{GJ_TEST_FAIL} Tests",
        # auth
        f"{GJ_AUTH} auth": f"{GJ_AUTH} Authentication",
        # ci & build
        f"{GJ_BUILD} build": f"{GJ_CI}{GJ_BUILD} CI & Build",
        f"{GJ_CI} ci": f"{GJ_CI}{GJ_BUILD} CI & Build",
        # ui & uix
        f"{GJ_UI} ui": f"{GJ_UI}{GJ_UX} UI & UIX",
        f"{GJ_UX} ux": f"{GJ_UI}{GJ_UX} UI & UIX",
        # configuration & scripts & packages
        f"{GJ_CONFIG} config": f"{GJ_CONFIG}{GJ_SCRIPT}{GJ_PACKAGE} Configuration, Scripts, Packages",
        f"{GJ_SCRIPT} script": f"{GJ_CONFIG}{GJ_SCRIPT}{GJ_PACKAGE} Configuration, Scripts, Packages",
        f"{GJ_PACKAGE} package": f"{GJ_CONFIG}{GJ_SCRIPT}{GJ_PACKAGE} Configuration, Scripts, Packages",
        # cleanup
        f"{GJ_DUMP} dump": f"{GJ_DUMP}{GJ_DEAD} Clean up",
        f"{GJ_DEAD} dead": f"{GJ_DUMP}{GJ_DEAD} Clean up",
        # dependencies
        f"{GJ_DEP_ADD} dep-add": f"{GJ_PIN}{GJ_DEP_ADD}{GJ_DEP_DROP}{GJ_DEP_RM}{GJ_DEP_BUMP} Dependencies",
        f"{GJ_DEP_RM} dep-rm": f"{GJ_PIN}{GJ_DEP_ADD}{GJ_DEP_DROP}{GJ_DEP_RM}{GJ_DEP_BUMP} Dependencies",
        f"{GJ_DEP_BUMP} dep-bump": f"{GJ_PIN}{GJ_DEP_ADD}{GJ_DEP_DROP}{GJ_DEP_RM}{GJ_DEP_BUMP} Dependencies",
        f"{GJ_DEP_DROP} dep-drop": f"{GJ_PIN}{GJ_DEP_ADD}{GJ_DEP_DROP}{GJ_DEP_RM}{GJ_DEP_BUMP} Dependencies",
        f"{GJ_PIN} pin": f"{GJ_PIN}{GJ_DEP_ADD}{GJ_DEP_DROP}{GJ_DEP_RM}{GJ_DEP_BUMP} Dependencies",
        # types
        f"{GJ_TYPES} types": f"{GJ_TYPES} Types",
        # language & accessibility
        f"{GJ_LANG} lang": f"{GJ_LANG}{GJ_ACCESSIBILITY} Language & Accessibility",
        f"{GJ_ACCESSIBILITY} accessibility": f"{GJ_LANG}{GJ_ACCESSIBILITY} Language & Accessibility",
        # design
        f"{GJ_DESIGN} design": f"{GJ_DESIGN}{GJ_ANIMATION} Design",
        f"{GJ_ANIMATION} animation": f"{GJ_DESIGN}{GJ_ANIMATION} Design",
        # logs
        f"{GJ_LOGS_ADD} logs-add": f"{GJ_LOGS_ADD}{GJ_LOGS_RM} Logs",
        f"{GJ_LOGS_RM} logs-rm": f"{GJ_LOGS_ADD}{GJ_LOGS_RM} Logs",
        # people
        f"{GJ_PEOPLE} people": f"{GJ_PEOPLE} People",
        # database
        f"{GJ_DB} db": f"{GJ_DB} Database",
        # ignore
        f"{GJ_IGNORE} ignore": f"{GJ_IGNORE} Ignore",
        # snapshots
        f"{GJ_SNAP} snap": f"{GJ_SNAP} Snapshots",
        # experiments
        f"{GJ_EXPERIMENT} experiment": f"{GJ_EXPERIMENT} Experiments",
        # SEO
        f"{GJ_SEO} seo": f"{GJ_SEO} SEO",
        # infra
        f"{GJ_INFRA} infra": f"{GJ_INFRA} Infrastructure",
        # devxp
        f"{GJ_DEVXP} devxp": f"{GJ_DEVXP} Developer Experience",
        # money
        f"{GJ_MONEY} money": f"{GJ_MONEY} Sponsoring",
        # threading
        f"{GJ_THREADING} threading": f"{GJ_THREADING} Threading",
        # validation
        f"{GJ_VALIDATION} validation": f"{GJ_VALIDATION} Validation",
        # revert
        f"{GJ_REVERT} revert": f"{GJ_REVERT} Reversions",
        # deploy
        f"{GJ_DEPLOY} deploy": f"{GJ_DEPLOY} Deployments",
        # linting
        f"{GJ_FIX_LINT} fix-lint": f"{GJ_FIX_LINT} Linting",
        # resource & assets
        f"{GJ_RESOURCE} resource": f"{GJ_RESOURCE}{GJ_ASSET} Resources & Assets",
        f"{GJ_ASSET} asset": f"{GJ_RESOURCE}{GJ_ASSET} Resources & Assets",
        # others
        f"{GJ_SECRET} secret": f"{GJ_SECRET}{GJ_WIP}{GJ_ANALYTICS}{GJ_TYPO}{GJ_POOP}{GJ_EXTERNAL}{GJ_BEER}{GJ_TEXT}{GJ_EGG}{GJ_SEED}{GJ_FLAG}{GJ_CATCH}{GJ_HEALTH} Others",
        f"{GJ_WIP} wip": f"{GJ_SECRET}{GJ_WIP}{GJ_ANALYTICS}{GJ_TYPO}{GJ_POOP}{GJ_EXTERNAL}{GJ_BEER}{GJ_TEXT}{GJ_EGG}{GJ_SEED}{GJ_FLAG}{GJ_CATCH}{GJ_HEALTH} Others",
        f"{GJ_ANALYTICS} analytics": f"{GJ_SECRET}{GJ_WIP}{GJ_ANALYTICS}{GJ_TYPO}{GJ_POOP}{GJ_EXTERNAL}{GJ_BEER}{GJ_TEXT}{GJ_EGG}{GJ_SEED}{GJ_FLAG}{GJ_CATCH}{GJ_HEALTH} Others",
        f"{GJ_TYPO} typo": f"{GJ_SECRET}{GJ_WIP}{GJ_ANALYTICS}{GJ_TYPO}{GJ_POOP}{GJ_EXTERNAL}{GJ_BEER}{GJ_TEXT}{GJ_EGG}{GJ_SEED}{GJ_FLAG}{GJ_CATCH}{GJ_HEALTH} Others",
        f"{GJ_POOP} poop": f"{GJ_SECRET}{GJ_WIP}{GJ_ANALYTICS}{GJ_TYPO}{GJ_POOP}{GJ_EXTERNAL}{GJ_BEER}{GJ_TEXT}{GJ_EGG}{GJ_SEED}{GJ_FLAG}{GJ_CATCH}{GJ_HEALTH} Others",
        f"{GJ_EXTERNAL} external": f"{GJ_SECRET}{GJ_WIP}{GJ_ANALYTICS}{GJ_TYPO}{GJ_POOP}{GJ_EXTERNAL}{GJ_BEER}{GJ_TEXT}{GJ_EGG}{GJ_SEED}{GJ_FLAG}{GJ_CATCH}{GJ_HEALTH} Others",
        f"{GJ_BEER} beer": f"{GJ_SECRET}{GJ_WIP}{GJ_ANALYTICS}{GJ_TYPO}{GJ_POOP}{GJ_EXTERNAL}{GJ_BEER}{GJ_TEXT}{GJ_EGG}{GJ_SEED}{GJ_FLAG}{GJ_CATCH}{GJ_HEALTH} Others",
        f"{GJ_TEXT} text": f"{GJ_SECRET}{GJ_WIP}{GJ_ANALYTICS}{GJ_TYPO}{GJ_POOP}{GJ_EXTERNAL}{GJ_BEER}{GJ_TEXT}{GJ_EGG}{GJ_SEED}{GJ_FLAG}{GJ_CATCH}{GJ_HEALTH} Others",
        f"{GJ_EGG} egg": f"{GJ_SECRET}{GJ_WIP}{GJ_ANALYTICS}{GJ_TYPO}{GJ_POOP}{GJ_EXTERNAL}{GJ_BEER}{GJ_TEXT}{GJ_EGG}{GJ_SEED}{GJ_FLAG}{GJ_CATCH}{GJ_HEALTH} Others",
        f"{GJ_SEED} egg": f"{GJ_SECRET}{GJ_WIP}{GJ_ANALYTICS}{GJ_TYPO}{GJ_POOP}{GJ_EXTERNAL}{GJ_BEER}{GJ_TEXT}{GJ_EGG}{GJ_SEED}{GJ_FLAG}{GJ_CATCH}{GJ_HEALTH} Others",
        f"{GJ_FLAG} egg": f"{GJ_SECRET}{GJ_WIP}{GJ_ANALYTICS}{GJ_TYPO}{GJ_POOP}{GJ_EXTERNAL}{GJ_BEER}{GJ_TEXT}{GJ_EGG}{GJ_SEED}{GJ_FLAG}{GJ_CATCH}{GJ_HEALTH} Others",
        f"{GJ_CATCH} egg": f"{GJ_SECRET}{GJ_WIP}{GJ_ANALYTICS}{GJ_TYPO}{GJ_POOP}{GJ_EXTERNAL}{GJ_BEER}{GJ_TEXT}{GJ_EGG}{GJ_SEED}{GJ_FLAG}{GJ_CATCH}{GJ_HEALTH} Others",
        f"{GJ_HEALTH} health": f"{GJ_SECRET}{GJ_WIP}{GJ_ANALYTICS}{GJ_TYPO}{GJ_POOP}{GJ_EXTERNAL}{GJ_BEER}{GJ_TEXT}{GJ_EGG}{GJ_SEED}{GJ_FLAG}{GJ_CATCH}{GJ_HEALTH} Others",
        # None: init, bump, merge
    }
    # order sections in changelog. all other sections are ordered alphabetically
    change_type_order = [
        f"{GJ_BOOM} Boom",
        f"{GJ_FEAT} Features",
        f"{GJ_FIX}{GJ_HOTFIX} Fixes",
        f"{GJ_SECURITY} Security",
        f"{GJ_REFACTOR} Refactorings",
        f"{GJ_PERF} Performance",
    ]

    def questions(self) -> List[Dict[str, Any]]:
        """Return the questions to ask the user."""
        return [
            {
                "type": "list",
                "name": "prefix",
                "message": "Select the type of change you are committing",
                "choices": [
                    {
                        "value": moji.value,
                        "name": moji.name,
                    }
                    for moji in utils.get_gitmojis()
                ],
            },
            {
                "type": "input",
                "name": "scope",
                "message": (
                    "What is the scope of this change? (class or file name): "
                    "(press [enter] to skip)\n"
                ),
                "filter": parse_scope,
            },
            {
                "type": "input",
                "name": "subject",
                "filter": parse_subject,
                "message": (
                    "Write a short and imperative summary of the code changes: "
                    "(lower case and no period)\n"
                ),
            },
            {
                "type": "input",
                "name": "time",
                "message": "Time spent (i.e. 3h 15m) (press [enter] to skip):\n",
                "filter": lambda x: "⏰ " + x.strip() if x else "",
            },
            {
                "type": "input",
                "name": "body",
                "message": (
                    "Provide additional contextual information about the code changes: "
                    "(press [enter] to skip)\n"
                ),
                "filter": multiple_line_breaker,
            },
            {
                "type": "confirm",
                "message": "Is this a BREAKING CHANGE? Correlates with MAJOR in SemVer",
                "name": "is_breaking_change",
                "default": False,
            },
            {
                "type": "input",
                "name": "footer",
                "message": (
                    "Footer. Information about Breaking Changes and reference "
                    "issues that this commit closes: (press [enter] to skip)\n"
                ),
            },
        ]

    def message(self, answers: Dict[str, Any]) -> str:
        """Generate a commit message from the answers."""
        prefix = answers["prefix"]
        scope = answers["scope"]
        subject = answers["subject"]
        body = answers["body"]
        footer = answers["footer"]
        is_breaking_change = answers["is_breaking_change"]
        time = answers["time"]

        if scope:
            scope = f"({scope})"
        if body:
            body = f"\n\n{body}"
        if is_breaking_change and footer and not footer.startswith("BREAKING CHANGE"):
            footer = f"BREAKING CHANGE: {footer}"
        if footer:
            footer = f"\n\n{footer}"
        if time:
            time = f" >>> {time}"

        prefix_scope = f"{prefix}{scope}"
        if is_breaking_change:
            prefix_scope = f"{prefix_scope}!"

        message = f"{prefix_scope}: {subject}{time}{body}{footer}"

        return message

    def example(self) -> str:
        """Return an example commit message."""
        return (
            f"{GJ_FIX} fix: correct minor typos in code\n"
            "\n"
            "see the issue for details on the typos fixed\n"
            "\n"
            "closes issue #12"
        )

    def schema(self) -> str:
        """Return the commit message schema."""
        return (
            "<gitmoji><type>(<scope>): <subject>\n"
            "<BLANK LINE>\n"
            "<body>\n"
            "<BLANK LINE>\n"
            "(BREAKING CHANGE: )<footer>"
        )

    # pattern to validate commits
    def schema_pattern(self) -> str:
        """Return the schema validation pattern."""
        return utils.get_pattern()

    def info(self) -> str:
        """Return information about the commit message style."""
        dir_path = Path(__file__).parent
        filepath = dir_path.joinpath("conventional_gitmojis_info.txt")
        with open(filepath, "r") as f:
            content = f.read()
        return content

    def process_commit(self, commit: str) -> str:
        """Process a commit."""
        pat = self.schema_pattern()
        m = re.match(pat, commit)
        if m is None:
            return ""
        return m.group(3).strip()
