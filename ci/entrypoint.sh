#!/usr/bin/env bash

set -xeuo pipefail

/bin/bash -l -c "tox -- --cov --cov-report=html --cov-report=xml tests"
