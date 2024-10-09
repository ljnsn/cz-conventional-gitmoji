from pathlib import Path
from unittest import mock

import pytest

from gitmojify import mojify
from shared.gitmojis import *
from shared.spec import mojis


def test_grouped_gitmojis() -> None:
    """Verify gitmojis are grouped correctly."""
    grouped_gitmojis = mojify._grouped_gitmojis()
    assert isinstance(grouped_gitmojis, dict)
    assert len(grouped_gitmojis) == len(mojis)


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
    assert filepath.read_text(encoding="utf-8") == f"{GJ_FEAT} {message}"


def test_run_message(message: str, capsys: pytest.CaptureFixture[str]) -> None:
    """Verify the commit message is modified."""
    with mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=mock.MagicMock(commit_msg_file=None, message=message),
    ):
        mojify.run()
    captured = capsys.readouterr()
    assert captured.out == f"{GJ_FEAT} {message}"


@pytest.mark.parametrize(
    ["message", "allowed_prefixes", "expected"],
    [
        ("feat: some feature", None, f"{GJ_FEAT} feat: some feature"),
        ("custom: some feature", ["custom"], "custom: some feature"),
        ("CUSTOM: some feature", ["CUSTOM"], "CUSTOM: some feature"),
        ("feat: some feature", ["custom"], f"{GJ_FEAT} feat: some feature"),
        ("Merge some branch", ["Merge"], "Merge some branch"),
    ],
)
def test_gitmojify_allowed_prefixes(
    message: str, allowed_prefixes: list, expected: str
) -> None:
    """Test gitmojify function with allowed_prefixes."""
    assert mojify.gitmojify(message, allowed_prefixes) == expected


@pytest.mark.parametrize(
    ["message", "allowed_prefixes", "expected"],
    [
        ("Merge some branch", ["Merge"], f"{GJ_MERGE} merge: some branch"),
        ("MERGE: some feature", ["MERGE"], f"{GJ_MERGE} merge: some feature"),
        ("feat: some feature", None, f"{GJ_FEAT} feat: some feature"),
    ],
)
def test_gitmojify_convert(message: str, allowed_prefixes: list, expected: str) -> None:
    """Test gitmojify function with convert option."""
    assert mojify.gitmojify(message, allowed_prefixes, convert=True) == expected


def test_get_allowed_prefixes():
    """Test _get_allowed_prefixes function."""
    mock_args = mock.MagicMock(allowed_prefixes=["custom1", "custom2"], config=None)
    assert mojify._get_allowed_prefixes(mock_args) == ["custom1", "custom2"]

    mock_args = mock.MagicMock(allowed_prefixes=None, config="path/to/config")
    with mock.patch("commitizen.config.read_cfg") as mock_read_cfg:
        mock_read_cfg.return_value.settings = {
            "allowed_prefixes": ["custom3", "custom4"]
        }
        assert mojify._get_allowed_prefixes(mock_args) == ["custom3", "custom4"]

    mock_args = mock.MagicMock(allowed_prefixes=None, config="non_existent_config")
    assert mojify._get_allowed_prefixes(mock_args) == []


def test_run_with_allowed_prefixes(tmp_path: Path):
    """Test run function with allowed_prefixes."""
    filepath = tmp_path / "commit-msg"
    filepath.write_text("custom: some feature")

    with mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=mock.MagicMock(
            commit_msg_file=filepath.as_posix(),
            message=None,
            allowed_prefixes=["custom"],
            convert=False,
        ),
    ):
        mojify.run()

    assert filepath.read_text(encoding="utf-8") == "custom: some feature"


def test_run_with_convert(tmp_path: Path):
    """Test run function with convert option."""
    filepath = tmp_path / "commit-msg"
    filepath.write_text("Merge some feature")

    with mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=mock.MagicMock(
            commit_msg_file=filepath.as_posix(),
            message=None,
            allowed_prefixes=["Merge"],
            convert=True,
        ),
    ):
        mojify.run()

    assert filepath.read_text(encoding="utf-8") == f"{GJ_MERGE} merge: some feature"
