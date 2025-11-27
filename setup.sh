#!/usr/bin/env bash
set -e

# Create and activate virtual environment in .venv
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. Activate the virtualenv with: source .venv/bin/activate (or on Windows: .venv\Scripts\Activate.ps1)"

