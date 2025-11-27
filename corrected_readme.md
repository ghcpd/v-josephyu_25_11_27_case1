# Flask User Management — Corrected README

✅ This README aligns with the project implementation and provides working commands for both Windows (PowerShell) and Unix (Bash) shells. It also corrects endpoint names, DB location, CSRF setup, and clarifies what features are and aren't implemented.

## Quick Start (Windows - PowerShell)

```powershell
# Create and activate venv
python -m venv .venv
& .venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the app (use default host/port)
python app.py
# App will run on http://127.0.0.1:5000 by default
```

## Quick Start (Unix / macOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

## Running on a different host/port

The project `app.py` currently runs using `app.run(debug=True)` and does not parse command-line flags. Use `FLASK_RUN_HOST` and `FLASK_RUN_PORT` with `flask run` if you need to control host/port, or run as shown with python and modify code to read env vars.

Example (Unix):
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=8080
```

Example (PowerShell):
```powershell
$env:FLASK_APP = 'app.py'
$env:FLASK_ENV = 'development'
flask run --host=0.0.0.0 --port=8080
```

## Web Routes (as implemented)
- GET `/` -> redirects to `/login` (or `/dashboard` if authenticated)
- GET/POST `/login` -> login form, requires `username` and `password` fields
- GET/POST `/register` -> registration form, requires `username`, `email` (required), `password` (>= 6 characters)
- GET `/dashboard` -> user dashboard (login required)
- GET `/logout` -> logout user

Notes:
- The app does not implement `/signup` or `/signin` — the endpoints are `/register` and `/login`.
- The app does not implement a `/profile` endpoint out-of-the-box.
- There are no `/api/register` or `/api/login` JSON endpoints implemented.

## Configuration
- SECRET KEY: app uses `app.config['SECRET_KEY']` set in `app.py` unless you override it via FLASK_SECRET in your environment (not implemented, see notes below).
- Database file: the app uses SQLite file `app.db` at the workspace root by default. You can change this by setting `app.config['DATABASE']` or modifying `app.py`.
- CSRF: Flask-WTF is enabled by default; for testing the test suite disables CSRF.
- Sessions: cookies-based sessions are used (Flask default). Redis is not used.

## Running tests

```bash
# Activate virtual env, then run
pytest -q
```

## Notes and recommendations
- If you need to run on a different port from `python app.py`, use the `FLASK_APP` + `flask run` approach (see example above).
- If you want to expose host/port via CLI args when running `python app.py`, modify `app.py` to parse `--host` and `--port` or use environment variables.
- To allow using `FLASK_SECRET` environment variable as SECRET_KEY, change `app.py` to read `os.environ.get('FLASK_SECRET', default)` and use that value.

