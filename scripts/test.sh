#!/usr/bin/env bash

set -e
set -x

poetry run pytest --cov src --cov-report xml tests
