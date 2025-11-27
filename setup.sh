#!/usr/bin/env bash
set -e
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Virtual environment created and dependencies installed. Activate with: source .venv/bin/activate (bash)"