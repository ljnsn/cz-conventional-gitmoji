#!/usr/bin/env bash

set -e
set -x

ruff src tests
black src tests --check
isort src tests --check-only
