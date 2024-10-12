## v0.5.3 (2024-10-12)

### 🐛🚑️ Fixes

- **mojify**: get encoding from settings

### ✅🤡🧪 Tests

- **gitmojify**: add encoding and more tests

### 🧹 chore

- use permalink

## v0.5.2 (2024-10-12)

### 🐛🚑️ Fixes

- newlines issue (#208)

## v0.5.1 (2024-10-11)

### 🐛🚑️ Fixes

- **shared**: keep only config fields needed

### 🔧🔨📦️ Configuration, Scripts, Packages

- **commitizen**: use annotated tags

### 🧹 chore

- lock update

## v0.5.0 (2024-10-11)

### ✨ Features

- support `allowed_prefixes` and add `convert_prefixes` (#224)

### 📝💡 Documentation

- **readme**: add type mapping

### 🔧🔨📦️ Configuration, Scripts, Packages

- update lock
- **pre-commit**: drop pygrep hooks

### 🧹 chore

- copier update

## v0.4.5 (2024-10-08)

### 🐛🚑️ Fixes

- **shared**: reduce duplication

### ⏪️ Reversions

- "🐛 fix(cz-gitmoji): move back dunder var"

### 📌➕⬇️ ➖⬆️  Dependencies

- bump all

## v0.4.4 (2024-10-08)

### 🐛🚑️ Fixes

- **cz-gitmoji**: move back dunder var

## v0.4.3 (2024-10-08)

### 🐛🚑️ Fixes

- **hatch**: build

### 💚👷 CI & Build

- make sure git uses lf
- set default shell to bash

### 🔧🔨📦️ Configuration, Scripts, Packages

- **lint**: use --diff instead of --check

## v0.4.2 (2024-10-08)

### 🐛🚑️ Fixes

- don't set token username

## v0.4.1 (2024-10-08)

### 🐛🚑️ Fixes

- pass pypi creds to uv

## v0.4.0 (2024-10-08)

### 🐛🚑️ Fixes

- drop support for python3.7

### 🎨🏗️ Style & Architecture

- add docstrings
- add docstring and fix magic

### 💚👷 CI & Build

- update pipeline for uv

### 📝💡 Documentation

- add note about commitizen hook extra dep

### 🔧🔨📦️ Configuration, Scripts, Packages

- **commitizen**: set major version zero to true
- **ruff**: set target to 3.8
- update scripts for uv

### 🧑‍💻 Developer Experience

- switch to uv

## v0.3.3 (2024-08-08)

### 🐛🚑️ Fixes

- **mojify**: set git message read encoding

### 🔧🔨📦️ Configuration, Scripts, Packages

- **pre-commit**: fix ruff check command

## v0.3.2 (2024-05-21)

### 🐛🚑️ Fixes

- **cz-gitmoji**: add bump map for major version zero

## v0.3.1 (2024-04-28)

### 🐛🚑️ Fixes

- bump pattern breaking recognition

### 💚👷 CI & Build

- use ruff for formatting

### 📌➕⬇️ ➖⬆️  Dependencies

- black

### 📝💡 Documentation

- **readme**: remove poetry specific mention

### 🔧🔨📦️ Configuration, Scripts, Packages

- remove black config and add ruff target version
- loosen dependency constraints
- remove upper bound on ruff

## v0.3.0 (2024-04-17)

### ✨ Features

- add chore type

### build

- **deps**: bump codecov/codecov-action from 3 to 4

### ✅🤡🧪 Tests

- **gitmojify**: check against moji list
- **cz-gitmoji**: check number of choices is the same as number of mojis

### 💚👷 CI & Build

- add job name
- **dependabot**: use different token for dependabot
- run script directly
- bump pre commit hooks

### 📝💡 Documentation

- **readme**: add note about install pre-commit hooks

### 🔧🔨📦️ Configuration, Scripts, Packages

- **ruff**: adapt to 0.2.0

### 🩹 fix-simple

- **cz-gitmoji**: remove unnecessary early return

## v0.2.4 (2024-01-30)

### 🐛🚑️ Fixes

- py312 support

### 💚👷 CI & Build

- re-enable 3.12 in CI

## v0.2.3 (2024-01-24)

### 🐛🚑️ Fixes

- typo

## v0.2.2 (2024-01-24)

### 🐛🚑️ Fixes

- bump

### 💚👷 CI & Build

- set python version to use in deploy to 3.11

## v0.2.1 (2024-01-24)

### 🐛🚑️ Fixes

- **gitmojify**: force encoding to utf8

### build

- **deps**: bump actions/setup-python from 4 to 5
- **deps**: bump actions/checkout from 3 to 4

### ✅🤡🧪 Tests

- **gitmojify**: use message in assertion
- **gitmojfy**: use correct encoding in test
- **gitmojify**: add tests for running gitmojify

### 🏷️ Types

- add type annotation for capsys
- add py.typed markers

### 💚👷 CI & Build

- add windows to test matrix

### 📌➕⬇️ ➖⬆️  Dependencies

- mypy

### 🔧🔨📦️ Configuration, Scripts, Packages

- run mypy on lint
- **mypy**: ignore missing imports

### 🚨 Linting

- ignore invalid arg in test

## v0.2.0 (2023-05-21)

### ✨ Features

- move to new plugin format

### 🐛🚑️ Fixes

- fix plugin name

### 💚👷 CI & Build

- **ruff**: use extend-fixable

### 📌➕⬇️ ➖⬆️  Dependencies

- bump commitizen

## v0.1.3 (2023-05-02)

### build

- **deps**: bump actions/checkout from 2 to 3
- **deps**: bump actions/setup-python from 1 to 4
- **deps**: bump commitizen from 2.38.0 to 2.39.1

### 💚👷 CI & Build

- **actions**: remove mac for now
- add python 3.11 to matrix
- use ruff in pre-commit
- remove run on pull request
- remove windows from matrix
- create poetry venv
- **dependabot**: fix dependabot commit message
- **publish**: fix commit message condition

### 📌➕⬇️ ➖⬆️  Dependencies

- attrs to latest
- remove isort
- bump ruff
- bump commitizen

### 🔧🔨📦️ Configuration, Scripts, Packages

- **ruff**: extend-ignore to ignore
- add more ruff config
- remove isort config
- remove isort from lint
- **poetry**: update poetry lock
- use poetry to run tools

### 🙈 Ignore

- add .idea

## v0.1.2 (2022-12-27)

### 🐛🚑️ Fixes

- **changelog**: order sections in changelog

### 💚👷 CI & Build

- **publish**: fix script path

### 🔧🔨📦️ Configuration, Scripts, Packages

- **commitizen**: fix tag format and bump message

## 0.1.1 (2022-12-27)

### 🐛🚑️ Fixes

- **cz_gitmoji**: fix ignore pattern in change map
