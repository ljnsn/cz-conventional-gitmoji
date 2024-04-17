#!/usr/bin/env bash

set -e
set -x

poetry run ruff check src tests
poetry run ruff format src tests --check
poetry run mypy src tests
