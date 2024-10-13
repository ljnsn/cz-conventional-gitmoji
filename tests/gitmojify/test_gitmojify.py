from pathlib import Path
from unittest import mock

import attrs
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
        return_value=mock.MagicMock(
            config=None,
            commit_msg_file=filepath.as_posix(),
            message=None,
        ),
    ):
        mojify.run()
    assert filepath.read_text(encoding="utf-8") == f"{GJ_FEAT} {message}"


def test_run_message(message: str, capsys: pytest.CaptureFixture[str]) -> None:
    """Verify the commit message is modified."""
    with mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=mock.MagicMock(config=None, commit_msg_file=None, message=message),
    ):
        mojify.run()
    captured = capsys.readouterr()
    assert captured.out == f"{GJ_FEAT} {message}"


@pytest.mark.parametrize(
    ["message", "allowed_prefixes", "convert_prefixes", "expected"],
    [
        ("feat: some feature", None, None, f"{GJ_FEAT} feat: some feature"),
        ("custom: some feature", ["custom"], None, "custom: some feature"),
        ("CUSTOM: some feature", ["CUSTOM"], None, "CUSTOM: some feature"),
        ("feat: some feature", ["custom"], None, f"{GJ_FEAT} feat: some feature"),
        ("Merge some branch", ["Merge"], None, "Merge some branch"),
        ("Merge some branch", None, ["Merge"], f"{GJ_MERGE} merge: some branch"),
    ],
)
def test_gitmojify_allowed_prefixes(
    message: str, allowed_prefixes: list, convert_prefixes: list, expected: str
) -> None:
    """Test gitmojify function with allowed_prefixes and convert_prefixes."""
    assert mojify.gitmojify(message, allowed_prefixes, convert_prefixes) == expected


@pytest.mark.parametrize(
    ["message", "convert_prefixes", "expected"],
    [
        ("Merge some branch", ["Merge"], f"{GJ_MERGE} merge: some branch"),
        ("MERGE: some feature", ["MERGE"], f"{GJ_MERGE} merge: some feature"),
        ("feat: some feature", None, f"{GJ_FEAT} feat: some feature"),
    ],
)
def test_gitmojify_convert(message: str, convert_prefixes: list, expected: str) -> None:
    """Test gitmojify function with convert_prefixes option."""
    assert mojify.gitmojify(message, convert_prefixes=convert_prefixes) == expected


def test_get_settings() -> None:
    """Test get_settings function."""
    orig_settings = mojify.get_settings()
    mock_args = mock.MagicMock(config="path/to/config")
    with mock.patch("commitizen.config.read_cfg") as mock_read_cfg:
        mock_read_cfg.return_value.settings = attrs.asdict(
            attrs.evolve(
                orig_settings,
                allowed_prefixes=["custom3", "custom4"],
                convert_prefixes=["Merge", "Revert"],
            )
        )
        settings = mojify.get_settings(mock_args.config)
        assert settings.allowed_prefixes == ["custom3", "custom4"]
        assert settings.convert_prefixes == ["Merge", "Revert"]


def test_run_with_allowed_prefixes(tmp_path: Path):
    """Test run function with allowed_prefixes."""
    filepath = tmp_path / "commit-msg"
    filepath.write_text("custom: some feature")

    with mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=mock.MagicMock(
            commit_msg_file=filepath.as_posix(),
            message=None,
            config=None,
            allowed_prefixes=["custom"],
            convert_prefixes=None,
        ),
    ):
        mojify.run()

    assert filepath.read_text(encoding="utf-8") == "custom: some feature"


def test_run_with_convert_prefixes(tmp_path: Path):
    """Test run function with convert_prefixes option."""
    filepath = tmp_path / "commit-msg"
    filepath.write_text("Merge some feature")

    with mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=mock.MagicMock(
            commit_msg_file=filepath.as_posix(),
            message=None,
            config=None,
            allowed_prefixes=None,
            convert_prefixes=["Merge"],
        ),
    ):
        mojify.run()

    assert filepath.read_text(encoding="utf-8") == f"{GJ_MERGE} merge: some feature"


def test_run_with_options(tmp_path: Path):
    """Test run function with allowed_prefixes and convert_prefixes options."""
    filepath = tmp_path / "commit-msg"
    filepath.write_text("custom: some feature")

    with mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=mock.MagicMock(
            commit_msg_file=filepath.as_posix(),
            message=None,
            config="path/to/config",
            allowed_prefixes=None,
            convert_prefixes=None,
        ),
    ), mock.patch(
        "gitmojify.mojify.get_settings",
        return_value=mock.MagicMock(
            allowed_prefixes=["custom"],
            convert_prefixes=["Merge"],
            encoding="utf-8",
        ),
    ):
        mojify.run()
        assert filepath.read_text(encoding="utf-8") == "custom: some feature"

    filepath.write_text("Merge some branch")
    with mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=mock.MagicMock(
            commit_msg_file=filepath.as_posix(),
            message=None,
            config="path/to/config",
            allowed_prefixes=None,
            convert_prefixes=None,
        ),
    ), mock.patch(
        "gitmojify.mojify.get_settings",
        return_value=mock.MagicMock(
            allowed_prefixes=None,
            convert_prefixes=["Merge"],
            encoding="utf-8",
        ),
    ):
        mojify.run()
        assert filepath.read_text(encoding="utf-8") == f"{GJ_MERGE} merge: some branch"


def test_gitmojify_with_convert_prefixes():
    """Test gitmojify with convert_prefixes."""
    message = "feat: add new feature"
    result = mojify.gitmojify(message, convert_prefixes=["feat"])
    assert result.startswith("✨")


SUMMARY = "branch 'main' into branch 'dev'"
DESCRIPTION = "This is a description."


@pytest.mark.parametrize(
    ["message_in", "message_out", "should_raise"],
    [
        (f"Merge {SUMMARY}", f"{GJ_MERGE} merge: {SUMMARY}", False),
        (f"Merge: {SUMMARY}", f"{GJ_MERGE} merge: {SUMMARY}", False),
        (f"merge {SUMMARY}", ..., True),
        (f"merge: {SUMMARY}", f"{GJ_MERGE} merge: {SUMMARY}", False),
        (
            f"Merge {SUMMARY}\n\n{DESCRIPTION}",
            f"{GJ_MERGE} merge: {SUMMARY}\n\n{DESCRIPTION}",
            False,
        ),
        ("Merge", ..., True),
        ("Merge: ", ..., True),
        ("merge: ", ..., True),
        # TODO: expected is f"{GJ_MERGE} merge: \n\n{DESCRIPTION}" and should_raise is True
        (f"Merge \n\n{DESCRIPTION}", f"{GJ_MERGE} merge: {DESCRIPTION}", False),
    ],
)
def test_gitmojify_with_convert_prefixes_merge(
    message_in: str, message_out: str, should_raise: bool
):
    """Test gitmojify with convert_prefixes and the Merge prefix."""
    if not should_raise:
        result = mojify.gitmojify(message_in, convert_prefixes=["Merge"])
        assert result == message_out
    else:
        with pytest.raises(ValueError) as exc_info:
            mojify.gitmojify(message_in, convert_prefixes=["Merge"])
        assert str(exc_info.value) == "invalid commit message"


def test_gitmojify_with_allowed_prefixes():
    """Test gitmojify with allowed_prefixes."""
    message = "custom: special commit"
    result = mojify.gitmojify(message, allowed_prefixes=["custom"])
    assert result == message


def test_gitmojify_invalid_message():
    """Test gitmojify with an invalid message."""
    message = "invalid commit message"
    with pytest.raises(ValueError, match="invalid commit message"):
        mojify.gitmojify(message)


def test_gitmojify_with_existing_gitmoji():
    """Test gitmojify with a message that already has a gitmoji."""
    message = "🐛 fix: resolve bug"
    result = mojify.gitmojify(message)
    assert result == message
