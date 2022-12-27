#!/usr/bin/env bash

set -e
set -x

pytest --cov src --cov-report xml tests
