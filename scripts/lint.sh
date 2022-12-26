#!/usr/bin/env bash

set -e
set -x

flake8 src tests
black src tests --check
isort src tests --check-only
