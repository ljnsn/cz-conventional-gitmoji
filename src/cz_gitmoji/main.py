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
from shared.gitmojis import GitmojiEnum as GJ  # noqa: N814


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
    """Cz Gitmoji plugin."""

    # pattern to match messages for bumping
    # if none of these match, version will not be bumped (unless manually specified)
    bump_pattern = (
        rf"^((BREAKING[\-\ ]CHANGE"
        rf"|{GJ.BOOM}? ?boom"
        rf"|{GJ.FEAT}? ?feat"
        rf"|{GJ.FIX}? ?fix"
        rf"|{GJ.HOTFIX}? ?hotfix"
        rf"|{GJ.REFACTOR}? +refactor"
        rf"|{GJ.PERF}? ?perf)"
        r"(\(.+\))?"  # scope
        r"!?):"  # breaking
    )
    # map types to SemVer
    bump_map = OrderedDict(
        (
            (r"^.+!$", MAJOR),
            (r"^BREAKING[\-\ ]CHANGE", MAJOR),
            (rf"^{GJ.BOOM}? ?boom", MAJOR),
            (rf"^{GJ.FEAT}? ?feat", MINOR),
            (rf"^{GJ.FIX}? ?fix", PATCH),
            (rf"^{GJ.HOTFIX}? ?hotfix", PATCH),
            (rf"^{GJ.REFACTOR}? ?refactor", PATCH),
            (rf"^{GJ.PERF}? ?perf", PATCH),
        )
    )
    bump_map_major_version_zero = OrderedDict(
        (
            (r"^.+!$", MINOR),
            (r"^BREAKING[\-\ ]CHANGE", MINOR),
            (rf"^{GJ.BOOM}? ?boom", MINOR),
            (rf"^{GJ.FEAT}? ?feat", MINOR),
            (rf"^{GJ.FIX}? ?fix", PATCH),
            (rf"^{GJ.HOTFIX}? ?hotfix", PATCH),
            (rf"^{GJ.REFACTOR}? ?refactor", PATCH),
            (rf"^{GJ.PERF}? ?perf", PATCH),
        )
    )
    # parse information for generating the change log
    commit_parser = (
        rf"^(?P<change_type>{utils.get_type_group_pattern()}|BREAKING CHANGE)"
        r"(?:\((?P<scope>[^()\r\n]*)\)|\()?(?P<breaking>!)?:\s(?P<message>.*)?"
    )
    # exclude from changelog
    changelog_pattern = (
        rf"^(?!{GJ.INIT}? ?init)(?!{GJ.MERGE}? ?merge)(?!{GJ.BUMP}? ?bump).*"
    )
    # map types to changelog sections
    change_type_map = {
        # boom
        f"{GJ.BOOM} boom": f"{GJ.BOOM} Boom",
        # features
        f"{GJ.FEAT} feat": f"{GJ.FEAT} Features",
        # fixes
        f"{GJ.FIX} fix": f"{GJ.FIX}{GJ.HOTFIX} Fixes",
        f"{GJ.HOTFIX} hotfix": f"{GJ.FIX}{GJ.HOTFIX} Fixes",
        # security
        f"{GJ.SECURITY} security": f"{GJ.SECURITY} Security",
        # license
        f"{GJ.LICENSE} license": f"{GJ.LICENSE} License",
        # refactorings
        f"{GJ.REFACTOR} refactor": f"{GJ.REFACTOR} Refactorings",
        # style & architecture
        f"{GJ.STYLE} style": f"{GJ.STYLE}{GJ.ARCH} Style & Architecture",
        f"{GJ.ARCH} arch": f"{GJ.STYLE}{GJ.ARCH} Style & Architecture",
        # performance
        f"{GJ.PERF} perf": f"{GJ.PERF} Performance",
        # docs
        f"{GJ.DOCS} docs": f"{GJ.DOCS}{GJ.SOURCE_DOCS} Documentation",
        f"{GJ.SOURCE_DOCS} source-docs": f"{GJ.DOCS}{GJ.SOURCE_DOCS} Documentation",
        # tests
        f"{GJ.TEST} test": f"{GJ.TEST}{GJ.MOCK}{GJ.TEST_FAIL} Tests",
        f"{GJ.MOCK} mock": f"{GJ.TEST}{GJ.MOCK}{GJ.TEST_FAIL} Tests",
        f"{GJ.TEST_FAIL} test-fail": f"{GJ.TEST}{GJ.MOCK}{GJ.TEST_FAIL} Tests",
        # auth
        f"{GJ.AUTH} auth": f"{GJ.AUTH} Authentication",
        # ci & build
        f"{GJ.BUILD} build": f"{GJ.CI}{GJ.BUILD} CI & Build",
        f"{GJ.CI} ci": f"{GJ.CI}{GJ.BUILD} CI & Build",
        # ui & uix
        f"{GJ.UI} ui": f"{GJ.UI}{GJ.UX} UI & UIX",
        f"{GJ.UX} ux": f"{GJ.UI}{GJ.UX} UI & UIX",
        # configuration & scripts & packages
        f"{GJ.CONFIG} config": f"{GJ.CONFIG}{GJ.SCRIPT}{GJ.PACKAGE} Configuration, Scripts, Packages",
        f"{GJ.SCRIPT} script": f"{GJ.CONFIG}{GJ.SCRIPT}{GJ.PACKAGE} Configuration, Scripts, Packages",
        f"{GJ.PACKAGE} package": f"{GJ.CONFIG}{GJ.SCRIPT}{GJ.PACKAGE} Configuration, Scripts, Packages",
        # cleanup
        f"{GJ.DUMP} dump": f"{GJ.DUMP}{GJ.DEAD} Clean up",
        f"{GJ.DEAD} dead": f"{GJ.DUMP}{GJ.DEAD} Clean up",
        # dependencies
        f"{GJ.DEP_ADD} dep-add": f"{GJ.PIN}{GJ.DEP_ADD}{GJ.DEP_DROP}{GJ.DEP_RM}{GJ.DEP_BUMP} Dependencies",
        f"{GJ.DEP_RM} dep-rm": f"{GJ.PIN}{GJ.DEP_ADD}{GJ.DEP_DROP}{GJ.DEP_RM}{GJ.DEP_BUMP} Dependencies",
        f"{GJ.DEP_BUMP} dep-bump": f"{GJ.PIN}{GJ.DEP_ADD}{GJ.DEP_DROP}{GJ.DEP_RM}{GJ.DEP_BUMP} Dependencies",
        f"{GJ.DEP_DROP} dep-drop": f"{GJ.PIN}{GJ.DEP_ADD}{GJ.DEP_DROP}{GJ.DEP_RM}{GJ.DEP_BUMP} Dependencies",
        f"{GJ.PIN} pin": f"{GJ.PIN}{GJ.DEP_ADD}{GJ.DEP_DROP}{GJ.DEP_RM}{GJ.DEP_BUMP} Dependencies",
        # types
        f"{GJ.TYPES} types": f"{GJ.TYPES} Types",
        # language & accessibility
        f"{GJ.LANG} lang": f"{GJ.LANG}{GJ.ACCESSIBILITY} Language & Accessibility",
        f"{GJ.ACCESSIBILITY} accessibility": f"{GJ.LANG}{GJ.ACCESSIBILITY} Language & Accessibility",
        # design
        f"{GJ.DESIGN} design": f"{GJ.DESIGN}{GJ.ANIMATION} Design",
        f"{GJ.ANIMATION} animation": f"{GJ.DESIGN}{GJ.ANIMATION} Design",
        # logs
        f"{GJ.LOGS_ADD} logs-add": f"{GJ.LOGS_ADD}{GJ.LOGS_RM} Logs",
        f"{GJ.LOGS_RM} logs-rm": f"{GJ.LOGS_ADD}{GJ.LOGS_RM} Logs",
        # people
        f"{GJ.PEOPLE} people": f"{GJ.PEOPLE} People",
        # database
        f"{GJ.DB} db": f"{GJ.DB} Database",
        # ignore
        f"{GJ.IGNORE} ignore": f"{GJ.IGNORE} Ignore",
        # snapshots
        f"{GJ.SNAP} snap": f"{GJ.SNAP} Snapshots",
        # experiments
        f"{GJ.EXPERIMENT} experiment": f"{GJ.EXPERIMENT} Experiments",
        # SEO
        f"{GJ.SEO} seo": f"{GJ.SEO} SEO",
        # infra
        f"{GJ.INFRA} infra": f"{GJ.INFRA} Infrastructure",
        # devxp
        f"{GJ.DEVXP} devxp": f"{GJ.DEVXP} Developer Experience",
        # money
        f"{GJ.MONEY} money": f"{GJ.MONEY} Sponsoring",
        # threading
        f"{GJ.THREADING} threading": f"{GJ.THREADING} Threading",
        # validation
        f"{GJ.VALIDATION} validation": f"{GJ.VALIDATION} Validation",
        # revert
        f"{GJ.REVERT} revert": f"{GJ.REVERT} Reversions",
        # deploy
        f"{GJ.DEPLOY} deploy": f"{GJ.DEPLOY} Deployments",
        # linting
        f"{GJ.FIX_LINT} fix-lint": f"{GJ.FIX_LINT} Linting",
        # resource & assets
        f"{GJ.RESOURCE} resource": f"{GJ.RESOURCE}{GJ.ASSET} Resources & Assets",
        f"{GJ.ASSET} asset": f"{GJ.RESOURCE}{GJ.ASSET} Resources & Assets",
        # others
        f"{GJ.SECRET} secret": f"{GJ.SECRET}{GJ.WIP}{GJ.ANALYTICS}{GJ.TYPO}{GJ.POOP}{GJ.EXTERNAL}{GJ.BEER}{GJ.TEXT}{GJ.EGG}{GJ.SEED}{GJ.FLAG}{GJ.CATCH}{GJ.HEALTH} Others",
        f"{GJ.WIP} wip": f"{GJ.SECRET}{GJ.WIP}{GJ.ANALYTICS}{GJ.TYPO}{GJ.POOP}{GJ.EXTERNAL}{GJ.BEER}{GJ.TEXT}{GJ.EGG}{GJ.SEED}{GJ.FLAG}{GJ.CATCH}{GJ.HEALTH} Others",
        f"{GJ.ANALYTICS} analytics": f"{GJ.SECRET}{GJ.WIP}{GJ.ANALYTICS}{GJ.TYPO}{GJ.POOP}{GJ.EXTERNAL}{GJ.BEER}{GJ.TEXT}{GJ.EGG}{GJ.SEED}{GJ.FLAG}{GJ.CATCH}{GJ.HEALTH} Others",
        f"{GJ.TYPO} typo": f"{GJ.SECRET}{GJ.WIP}{GJ.ANALYTICS}{GJ.TYPO}{GJ.POOP}{GJ.EXTERNAL}{GJ.BEER}{GJ.TEXT}{GJ.EGG}{GJ.SEED}{GJ.FLAG}{GJ.CATCH}{GJ.HEALTH} Others",
        f"{GJ.POOP} poop": f"{GJ.SECRET}{GJ.WIP}{GJ.ANALYTICS}{GJ.TYPO}{GJ.POOP}{GJ.EXTERNAL}{GJ.BEER}{GJ.TEXT}{GJ.EGG}{GJ.SEED}{GJ.FLAG}{GJ.CATCH}{GJ.HEALTH} Others",
        f"{GJ.EXTERNAL} external": f"{GJ.SECRET}{GJ.WIP}{GJ.ANALYTICS}{GJ.TYPO}{GJ.POOP}{GJ.EXTERNAL}{GJ.BEER}{GJ.TEXT}{GJ.EGG}{GJ.SEED}{GJ.FLAG}{GJ.CATCH}{GJ.HEALTH} Others",
        f"{GJ.BEER} beer": f"{GJ.SECRET}{GJ.WIP}{GJ.ANALYTICS}{GJ.TYPO}{GJ.POOP}{GJ.EXTERNAL}{GJ.BEER}{GJ.TEXT}{GJ.EGG}{GJ.SEED}{GJ.FLAG}{GJ.CATCH}{GJ.HEALTH} Others",
        f"{GJ.TEXT} text": f"{GJ.SECRET}{GJ.WIP}{GJ.ANALYTICS}{GJ.TYPO}{GJ.POOP}{GJ.EXTERNAL}{GJ.BEER}{GJ.TEXT}{GJ.EGG}{GJ.SEED}{GJ.FLAG}{GJ.CATCH}{GJ.HEALTH} Others",
        f"{GJ.EGG} egg": f"{GJ.SECRET}{GJ.WIP}{GJ.ANALYTICS}{GJ.TYPO}{GJ.POOP}{GJ.EXTERNAL}{GJ.BEER}{GJ.TEXT}{GJ.EGG}{GJ.SEED}{GJ.FLAG}{GJ.CATCH}{GJ.HEALTH} Others",
        f"{GJ.SEED} egg": f"{GJ.SECRET}{GJ.WIP}{GJ.ANALYTICS}{GJ.TYPO}{GJ.POOP}{GJ.EXTERNAL}{GJ.BEER}{GJ.TEXT}{GJ.EGG}{GJ.SEED}{GJ.FLAG}{GJ.CATCH}{GJ.HEALTH} Others",
        f"{GJ.FLAG} egg": f"{GJ.SECRET}{GJ.WIP}{GJ.ANALYTICS}{GJ.TYPO}{GJ.POOP}{GJ.EXTERNAL}{GJ.BEER}{GJ.TEXT}{GJ.EGG}{GJ.SEED}{GJ.FLAG}{GJ.CATCH}{GJ.HEALTH} Others",
        f"{GJ.CATCH} egg": f"{GJ.SECRET}{GJ.WIP}{GJ.ANALYTICS}{GJ.TYPO}{GJ.POOP}{GJ.EXTERNAL}{GJ.BEER}{GJ.TEXT}{GJ.EGG}{GJ.SEED}{GJ.FLAG}{GJ.CATCH}{GJ.HEALTH} Others",
        f"{GJ.HEALTH} health": f"{GJ.SECRET}{GJ.WIP}{GJ.ANALYTICS}{GJ.TYPO}{GJ.POOP}{GJ.EXTERNAL}{GJ.BEER}{GJ.TEXT}{GJ.EGG}{GJ.SEED}{GJ.FLAG}{GJ.CATCH}{GJ.HEALTH} Others",
        # None: init, bump, merge
    }
    # order sections in changelog. all other sections are ordered alphabetically
    change_type_order = [
        f"{GJ.BOOM} Boom",
        f"{GJ.FEAT} Features",
        f"{GJ.FIX}{GJ.HOTFIX} Fixes",
        f"{GJ.SECURITY} Security",
        f"{GJ.REFACTOR} Refactorings",
        f"{GJ.PERF} Performance",
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
            f"{GJ.FIX} fix: correct minor typos in code\n"
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
        # TODO: improve the info file
        filepath = dir_path.joinpath("conventional_gitmojis_info.txt")
        with filepath.open(encoding="utf-8") as f:
            content = f.read()
        return content

    def process_commit(self, commit: str) -> str:
        """Process a commit."""
        pat = self.schema_pattern()
        m = re.match(pat, commit)
        if m is None:
            return ""
        return m.group("subject").strip()
