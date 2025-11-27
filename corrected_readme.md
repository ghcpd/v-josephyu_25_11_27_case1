# Flask User Management Tutorial (Corrected)

This README contains corrected, working instructions for running the sample Flask user management app in this repository.

## Requirements
- Python 3.10+ (3.13 works)
- Git (optional)

## Setup (Linux / macOS)
```bash
# Create a Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Setup (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running the app
The app is a simple Flask application. It does not parse `--host`/`--port` args passed via CLI to `python app.py`.

Option A — Run with Python (default development server):
```bash
python app.py
# The app will run on http://127.0.0.1:5000 by default
```

Option B — Use Flask CLI (explicit host/port):
```bash
export FLASK_APP=app
flask run --host=0.0.0.0 --port=8080
```
(Windows PowerShell equivalent: `setx FLASK_APP app; flask run --host=0.0.0.0 --port=8080` or use `set` for session only.)

## Configuration
- The application reads `app.config['SECRET_KEY']` for CSRF protection and session signing. To use an environment variable, set the `SECRET_KEY` env var before starting the app:

```bash
export SECRET_KEY='replace-this-with-a-random-secret'
# or on Windows PowerShell:
$env:SECRET_KEY='replace-this-with-a-random-secret'
```

## Endpoints (correct)
- GET `/register` — registration form
  - Fields: `username` (required), `email` (required), `password` (required)
  - No `confirm_password` field is provided, contrary to some older documentation.
- GET `/login` — login form
  - Fields: `username` (required), `password` (required)
- GET `/dashboard` — protected user dashboard (login required)
- GET `/logout` — logout endpoint

Notes:
- There are no `/signup`, `/signin`, `/profile` endpoints; use `/register`, `/login`, and `/dashboard` respectively.
- There are no `/api/register` or `/api/login` endpoints in this sample app.

## Validation details (important)
- `username`: min 3 chars, max 32
- `email`: required and validated by `email_validator` package
- `password`: min 6 chars, max 128

## Database
- The app stores data in SQLite by default: `app.db` in the repository root. The README previously suggested `data/database.sqlite3` — that path does not exist.

## Sessions
- The app uses Flask default session handling and Flask-Login user sessions; Redis session backend is not enabled in this repository.

## Running tests
- A small test suite is included under `tests/`. To run the tests locally:

Bash (Linux/macOS):
```bash
./run_tests.sh
```

PowerShell (Windows):
```powershell
.\run_tests.ps1
```

## Examples: Register & Login (using the test client)
- Register a user by completing the `/register` form. The application uses CSRF protection, so manual POSTs should either include CSRF token or use Flask test client with `WTF_CSRF_ENABLED=False`.

## Notes for contributors
- If you'd like to add API endpoints, you can create `/api/register` and `/api/login` to accept JSON payloads and return JSON responses.
- To use Redis for sessions, integrate Flask-Session or another session backend and configure `SESSION_TYPE='redis'` and `SESSION_REDIS`.

## Helpful scripts
- `setup.sh` — Linux/macOS setup
- `setup.ps1` — Windows PowerShell setup
- `run_tests.sh` / `run_tests.ps1` — run pytest test suites

Thank you — run the app and tests using the correct platform-specific instructions above. If you'd like, I can add a Flask factory pattern for easier testing and configuration management.
