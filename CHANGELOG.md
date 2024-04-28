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
