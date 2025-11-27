#!/usr/bin/env bash
set -euo pipefail

# Activate venv
if [ -f .venv/bin/activate ]; then
  # POSIX
  source .venv/bin/activate
else
  echo "Virtualenv not found. Create it with: python -m venv .venv && source .venv/bin/activate"
  exit 1
fi

# Run pytest
pytest -q

echo "All tests passed"
