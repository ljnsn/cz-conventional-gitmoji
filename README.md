# cz-conventional-gitmoji

A [commitizen](https://github.com/commitizen-tools/commitizen) plugin that combines [gitmoji](https://gitmoji.dev/) and [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/).

## Installation

```bash
poetry add cz-conventional-gitmoji
```

or with pip:

```bash
pip install cz-conventional-gitmoji
```

## Usage

This package can be used as a normal `commitizen` plugin, either by specifying the name on the command line

```bash
cz --name cz_gitmoji commit
```

or by setting it in your **pyproject.toml**

```toml
[tool.commitizen]
name = "cz_gitmoji"
```

This will make `commitizen` use the commit message parsing rules defined by this plugin, which are 100% compatible with [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/). As such, the gitmojis are completely optional and all commands will continue to validate commit messages in conventional format just fine. This is useful if you're transitioning an existing repo to `cz-conventional-gitmoji` or you work in a team in which some colleagues don't like gitmojis.

### gitmojify

Apart from the conventional-gitmoji rules, this package provides the `gitmojify` command which is also available as a pre-commit hook. The command reads a commit message either from cli or a commit message file and prepends the correct gitmoji based on the type. If the message already has a gitmoji, it is returned as is.

```bash
$ gitmojify -m "init: initial version"
🎉 init: initial version
```

To use it as a pre-commit hook, install this packages as well as `commitizen` and put the following into your **.pre-commit-config.yaml**

```yaml
repos:
  - repo: https://github.com/ljnsn/cz-conventional-gitmoji
    rev: 0.2.4
    hooks:
      - id: conventional-gitmoji
```

Make sure to install the relevant pre-commit hooks with

```bash
pre-commit install --install-hooks
```

Commit with a message in conventional format that contains a valid type mapped by conventional gitmoji and the gitmoji will automagically be added.

## Features

- [x] Enable conventional gitmoji commit messages via `cz commit`.
- [x] Add hook to automatically prepend the appropriate gitmoji for the commit's type.
- [ ] Add `--simple-emojis` option to use only the emojis relating to `cz_conventional_commits` types.
- [ ] Add `--simple-types` option to use only the types used by `cz_conventional_commits`.
- [ ] Add `--conventional` option to put the emoji in the commit message, making it compatible with `cz_conventional_commits`.

## Inspiration

- [`commitizen-emoji`](https://github.com/marcelomaia/commitizen-emoji)
