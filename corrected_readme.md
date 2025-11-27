# Flask User Management Tutorial - Corrected

This repository runs a small Flask app for user registration and login.

## Quick Setup (POSIX and Windows)

POSIX (macOS/Linux):

```bash
# Create virtualenv
python -m venv .venv
# Activate
source .venv/bin/activate
# Install deps
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
# Activate
.\.venv\Scripts\Activate
pip install -r requirements.txt
```

⚠️ Note: The README in this repo previously described `python3` and `source .venv/bin/activate` which are POSIX-specific. The above shows both options.

## Running the App

This app uses the `app.py` script. There are two recommended ways to start the app:

1) Using flask CLI (recommended):

POSIX:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
python -m flask run --host=0.0.0.0 --port=8080
```

PowerShell:
```powershell
$env:FLASK_APP='app.py'
$env:FLASK_ENV='development'
python -m flask run --host=0.0.0.0 --port=8080
```

2) Using the script directly (defaults to 127.0.0.1:5000):

```bash
python app.py
# The app uses app.run(debug=True) and ignores --host/--port flags.
```

Open http://127.0.0.1:5000 or http://localhost:8080 depending on how you started the server.

## App Behavior & Routes

- Home redirects to login if not authenticated: `/` -> `/login`
- Login page: `GET /login` (template `templates/login.html`)
- Registration page: `GET /register` (template `templates/register.html`)
- Dashboard: `GET /dashboard` (requires login)
- Logout: `GET /logout`

API endpoints mentioned in the original README (`/api/register`, `/api/login`) do not exist. The actual routes use the blueprint `auth` with `/register` and `/login`.

**Form constraints**:
- `username` length: 3-32
- `password` minimum length: 6 (NOT 3 as stated in older README)
- `email` is required by the implementation (not optional)

## Database

- The app uses an SQLite database file: `app.db` in the workspace root by default.
- You can override the database path by setting `app.config['DATABASE']` (or via code in a config).

The README previously listed `data/database.sqlite3` as the database — this is incorrect by default.

## Session Store & CSRF

- Sessions are implemented using flask-login and default cookie-based sessions. The app does not configure Redis for server-side sessions.
- The app sets `app.config['SECRET_KEY']` in `app.py`. To use an environment variable, update `app.py` to read `os.environ['FLASK_SECRET']` or similar.

## Tests

Run tests with:

```bash
bash run_tests.sh
```

This repository includes `tests/test_app.py` with basic coverage for login, registration, and unique email/username checks.

## Notes and Recommendations

- To enable external binding on a dev server, either use `flask run` with host option (see above) or replace `app.run(debug=True)` with `app.run(host='0.0.0.0', port=8080, debug=True)`.
- If you expect server-side sessions (Redis), change Flask session interface or integrate Flask-Session with a Redis backend.
- If you want the app to read `FLASK_SECRET`, change `app.config['SECRET_KEY']` to read from environment variables.

---

End of corrected README
