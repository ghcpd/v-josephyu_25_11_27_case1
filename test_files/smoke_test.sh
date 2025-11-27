#!/usr/bin/env bash
set -euo pipefail

# Usage: Run the Flask app first in another shell (e.g., python -m flask run)
# Example: export FLASK_APP=app.py; python -m flask run

BASE_URL=${BASE_URL:-http://127.0.0.1:5000}

# Register a user
curl -s -X POST "$BASE_URL/register" -d "username=smoke&email=smoke@example.com&password=s3cret1" -c cookiejar.txt -L -v

# Login (should redirect to dashboard)
curl -s -X POST "$BASE_URL/login" -d "username=smoke&password=s3cret1" -b cookiejar.txt -c cookiejar.txt -L -v

# Get dashboard
curl -s "$BASE_URL/dashboard" -b cookiejar.txt -L -v

# Clean up
rm -f cookiejar.txt

echo "Smoke tests finished"
