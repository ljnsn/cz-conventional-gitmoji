from pathlib import Path
from unittest import mock

import pytest

from gitmojify import mojify
from shared.gitmojis import *


def test_grouped_gitmojis() -> None:
    """Verify gitmojis are grouped correctly."""
    grouped_gitmojis = mojify.grouped_gitmojis()
    assert isinstance(grouped_gitmojis, dict)
    assert len(grouped_gitmojis) == 73


@pytest.mark.parametrize(
    ["message_in", "message_out"],
    [
        ("feat: some new feature", f"{GJ_FEAT} feat: some new feature"),
        ("docs(readme): add a section", f"{GJ_DOCS} docs(readme): add a section"),
        (
            "refactor(FooClass)!: rename foo.bar -> foo.baz\n\nBREAKING CHANGE: this breaks stuff",
            f"{GJ_REFACTOR} refactor(FooClass)!: rename foo.bar -> foo.baz\n\nBREAKING CHANGE: this breaks stuff",
        ),
        (
            "test(foo-tests): add some tests for foo\n\nAdd new tests for foo.bar and foo.baz.",
            f"{GJ_TEST} test(foo-tests): add some tests for foo\n\nAdd new tests for foo.bar and foo.baz.",
        ),
    ],
)
def test_gitmojify(message_in: str, message_out: str) -> None:
    """Verify the correct icon is prepended to the message."""
    assert mojify.gitmojify(message_in) == message_out


@pytest.fixture(name="message")
def fixture_message() -> str:
    """Return a commit message."""
    return "feat: some new feature"


def test_run_file(tmp_path: Path, message: str) -> None:
    """Verify the commit message is modified."""
    filepath = tmp_path / "commit-msg"
    filepath.write_text(message)
    with mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=mock.MagicMock(commit_msg_file=filepath.as_posix(), message=None),
    ):
        mojify.run()
    assert filepath.read_text(encoding="utf-8") == f"{GJ_FEAT} feat: some new feature"


def test_run_message(message: str, capsys) -> None:
    """Verify the commit message is modified."""
    with mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=mock.MagicMock(commit_msg_file=None, message=message),
    ):
        mojify.run()
    captured = capsys.readouterr()
    assert captured.out == f"{GJ_FEAT} feat: some new feature"
