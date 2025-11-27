# Flask User Login and Registration (Corrected README)

This document provides working instructions for the existing implementation in this repository.

## Prerequisites
- Python 3.11+ (works with 3.13 in `.venv`)
- Recommended: virtual environment

## Setup (Windows PowerShell)

```powershell
# Go to project directory
cd "D:\mins_project\model_test\Documentation & knowledge\1126_case8\sample_task_2"

# Create and activate venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Run

```powershell
# Start the Flask app (debug on; binds to 127.0.0.1:5000)
python app.py
```

Open `http://127.0.0.1:5000/`.

## Configuration
- Secret key: set `app.config['SECRET_KEY']` in `app.py` (required for sessions/CSRF).
- Database: SQLite file `app.db` at project root (auto-created on first run).

## Routes
- `GET /login` — Login page
- `POST /login` — Process login
- `GET /register` — Registration page
- `POST /register` — Create a new user (username, email, password)
- `GET /logout` — Logout
- `GET /dashboard` — Authenticated landing page

## Field Requirements
- `username`: 3–32 characters
- `email`: valid email format; unique
- `password`: 6–128 characters; stored hashed via Werkzeug

## Example Walkthrough
1. Visit `/register`, create a user with a valid email.
2. You’ll be redirected to `/dashboard` after registration.
3. Logout at `/logout`.
4. Login again at `/login`.

## Testing Notes
- There is no `/api/*` JSON API in the current implementation.
- There is no Redis session store; sessions use secure cookies via Flask.
- Do not pass `--host`/`--port` CLI flags to `app.py`; the script ignores them.
