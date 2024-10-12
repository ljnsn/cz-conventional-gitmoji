from typing import Any, Dict, Optional, Tuple

import pytest
from commitizen.cz.exceptions import AnswerRequiredError

from cz_gitmoji.main import CommitizenGitmojiCz, parse_scope, parse_subject
from shared.spec import mojis


@pytest.mark.parametrize(
    ["scope", "expected"],
    [
        ("main", "main"),
        ("BaseConfig", "BaseConfig"),
        ("a scope", "a-scope"),
        ("", ""),
    ],
)
def test_parse_scope(scope: str, expected: str) -> None:
    """Verify scope is parsed properly."""
    assert parse_scope(scope) == expected


@pytest.mark.parametrize(
    ["text", "expected"],
    [
        ("a subject", "a subject"),
        ("subject", "subject"),
        ("subject ", "subject"),
        ("This is a subject.", "This is a subject"),
    ],
)
def test_parse_subject(text: str, expected: str) -> None:
    """Verify subject is parsed properly."""
    assert parse_subject(text) == expected


@pytest.mark.parametrize("text", ["", None])
def test_missing_subject(text: Optional[str]) -> None:
    """Verify that an empty subject raises an error."""
    with pytest.raises(AnswerRequiredError, match="Subject is required."):
        parse_subject(text)  # type: ignore[arg-type]


def test_questions(cz_gitmoji: CommitizenGitmojiCz) -> None:
    """Verify questions are as expected."""
    questions = cz_gitmoji.questions()
    assert isinstance(questions, list)
    assert isinstance(questions[0], dict)
    assert len(questions[0]["choices"]) == len(mojis)


def test_message(
    cz_gitmoji: CommitizenGitmojiCz,
    messages: Tuple[Dict[str, Any], str],
) -> None:
    """Verify the correct commit messages are created from answers."""
    answers, expected = messages
    message = cz_gitmoji.message(answers)
    assert message == expected


def test_example(cz_gitmoji: CommitizenGitmojiCz) -> None:
    """Verify the example commit message."""
    example = cz_gitmoji.example()
    assert "🐛 fix: correct minor typos in code" in example
    assert "closes issue #12" in example


def test_schema(cz_gitmoji: CommitizenGitmojiCz) -> None:
    """Verify the commit message schema."""
    schema = cz_gitmoji.schema()
    assert "<gitmoji><type>(<scope>): <subject>" in schema
    assert "(BREAKING CHANGE: )<footer>" in schema


def test_schema_pattern(cz_gitmoji: CommitizenGitmojiCz) -> None:
    """Verify the schema validation pattern."""
    pattern = cz_gitmoji.schema_pattern()
    assert isinstance(pattern, str)
    assert len(pattern) > 0


def test_info(cz_gitmoji: CommitizenGitmojiCz) -> None:
    """Verify the info content."""
    info = cz_gitmoji.info()
    assert isinstance(info, str)
    assert len(info) > 0


def test_process_commit(cz_gitmoji: CommitizenGitmojiCz) -> None:
    """Verify commit processing."""
    valid_commit = "🐛 fix(core): resolve null pointer exception"
    processed = cz_gitmoji.process_commit(valid_commit)
    assert processed == "resolve null pointer exception"

    invalid_commit = "This is not a valid commit message"
    processed = cz_gitmoji.process_commit(invalid_commit)
    assert processed == ""
