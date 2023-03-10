from typing import Any

import pytest
from commitizen import defaults
from commitizen.config import BaseConfig

from cz_gitmoji.main import CommitizenGitmojiCz
from shared.gitmojis import *


@pytest.fixture()
def config():
    _config = BaseConfig()
    _config.settings.update({"name": defaults.name})
    return _config


@pytest.fixture()
def cz_gitmoji(config: BaseConfig) -> CommitizenGitmojiCz:
    return CommitizenGitmojiCz(config)


@pytest.fixture(
    params=[
        # anwsers, expected
        (
            {
                "prefix": f"{GJ_DOCS} docs",
                "scope": "models",
                "subject": "person was undocumented",
                "body": "When no plant of the field was yet in the image of God he created them; male and female he created them.",
                "is_breaking_change": False,
                "time": "1h 15m",
                "footer": "",
            },
            f"{GJ_DOCS} docs(models): person was undocumented >>> 1h 15m\n\nWhen no plant of the field was yet in the image of God he created them; male and female he created them.",
        ),
        (
            {
                "prefix": f"{GJ_REFACTOR} refactor",
                "scope": "dto",
                "subject": "bla bla",
                "body": "The woman said to him, Where are you?",
                "is_breaking_change": True,
                "time": "",
                "footer": "BREAKING CHANGE: this breaks stuff",
            },
            f"{GJ_REFACTOR} refactor(dto)!: bla bla\n\nThe woman said to him, Where are you?\n\nBREAKING CHANGE: this breaks stuff",
        ),
        (
            {
                "prefix": f"{GJ_TEST} test",
                "scope": "controllers",
                "subject": "xpto",
                "body": "So out of the heavens and the earth and the woman, and between your offspring and hers; he will strike his heel.",
                "is_breaking_change": True,
                "time": "30m",
                "footer": "",
            },
            f"{GJ_TEST} test(controllers)!: xpto >>> 30m\n\nSo out of the heavens and the earth and the woman, and between your offspring and hers; he will strike his heel.",
        ),
        (
            {
                "prefix": f"{GJ_BUILD} build",
                "scope": "docker",
                "subject": "xpto",
                "body": "He drove out the man; and at the east of the garden at the time of the evening breeze, and the man and put him in the garden of Eden, to till the ground the LORD God walking in the image of God he created them; male and female he created them.",
                "is_breaking_change": False,
                "time": "",
                "footer": "Ref: #1111, #1112, #1113",
            },
            f"{GJ_BUILD} build(docker): xpto\n\nHe drove out the man; and at the east of the garden at the time of the evening breeze, and the man and put him in the garden of Eden, to till the ground the LORD God walking in the image of God he created them; male and female he created them.\n\nRef: #1111, #1112, #1113",
        ),
    ]
)
def messages(request: Any):
    return request.param
