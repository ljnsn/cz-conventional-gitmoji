#!/usr/bin/env bash

set -e
set -x

uv run pytest --cov src --cov-report xml tests
