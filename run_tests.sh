#!/usr/bin/env bash
set -e

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi

# Run the test suite
pytest -q

