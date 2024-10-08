#!/usr/bin/env bash

set -e
set -x

uv run ruff check src tests
uv run ruff format src tests --diff
uv run mypy src tests
