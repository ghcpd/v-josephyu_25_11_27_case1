#!/usr/bin/env bash
set -euo pipefail

# Create virtual environment, install requirements
python -m venv .venv
# Activate (POSIX)
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. Activate venv with: source .venv/bin/activate (or .\.venv\\Scripts\\Activate for PowerShell)"
