# cz-conventional-gitmoji

A [commitizen](https://github.com/commitizen-tools/commitizen) plugin that combines [gitmoji](https://gitmoji.dev/) and conventional.

## Installation

```shell
poetry add cz-conventional-gitmoji
```

or with pip:

```shell
pip install cz-conventional-gitmoji
```

## Usage

```shell
cz --name cz_gitmoji commit
```

## Features

- [x] Enable gitmoji conventional commit messages via `cz commit`.
- [ ] Add `--simple-emojis` option to use only the emojis relating to `cz_conventional_commits` types.
- [ ] Add `--simple-types` option to use only the types used by `cz_conventional_commits`.
- [ ] Add `--conventional` option to put the emoji in the commit message, making it compatible with `cz_conventional_commits`.
- [x] Add hook to automatically prepend the appropriate gitmoji for the commit's type.

## Inspiration

- [`commitizen-emoji`](https://github.com/marcelomaia/commitizen-emoji)
