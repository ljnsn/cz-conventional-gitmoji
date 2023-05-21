from typing import Any, Dict, Optional, Tuple

import pytest
from commitizen.cz.exceptions import AnswerRequiredError

from cz_gitmoji.main import CommitizenGitmojiCz, parse_scope, parse_subject


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
    assert len(questions[0]["choices"]) == 73


def test_message(
    cz_gitmoji: CommitizenGitmojiCz,
    messages: Tuple[Dict[str, Any], str],
) -> None:
    """Verify the correct commit messages are created from answers."""
    answers, expected = messages
    message = cz_gitmoji.message(answers)
    assert message == expected
