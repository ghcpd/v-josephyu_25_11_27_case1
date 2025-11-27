# Flask User Management Example — Corrected ✅

This document fixes the defects in the original README and provides working setup, run, and test instructions for the Flask app.

## Prerequisites
- Python 3.9+ (tested with 3.13)
- Git (optional)

## Environment Setup (.venv)

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux (Bash)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Quick Start

```powershell
# From project root with .venv activated
python app.py --host=0.0.0.0 --port=8080
```

- Default without args: `python app.py` → http://127.0.0.1:5000
- Alternative: `FLASK_APP=app.py flask run -h 0.0.0.0 -p 8080`

## Configuration
- **Secret Key / CSRF**: set `FLASK_SECRET` to override the default secret.
- **Database**: SQLite at `app.db` (config key `DATABASE`).
- **Sessions**: default Flask signed cookies (no Redis).

## Web Routes
- `GET/POST /register` (alias: `/signup`)
  - Fields: `username` (3-32 chars), `email` (required), `password` (6-128 chars)
- `GET/POST /login` (alias: `/signin`)
  - Fields: `username`, `password`
- `GET /dashboard` (alias: `/profile`) — requires login
- `GET /logout`

## JSON API
- `POST /api/register`
  - Body (any of the key variants):
    ```json
    {
      "username"|"user": "alice",
      "password"|"pass": "secret123",
      "email"|"mail": "alice@example.com"
    }
    ```
  - Responses: `201 Created` on success; `409` on duplicate user/email; `400` on validation errors.

- `POST /api/login`
  - Body:
    ```json
    { "username"|"user": "alice", "password"|"pass": "secret123" }
    ```
  - Responses: `200 OK` on success; `401` on invalid creds; `400` on missing fields.

Example (PowerShell):
```powershell
$body = @{ user = 'alice'; pass = 'secret123'; mail = 'alice@example.com' } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8080/api/register -Method Post -Body $body -ContentType 'application/json'
```

Example (curl):
```bash
curl -X POST http://localhost:8080/api/login \
  -H 'Content-Type: application/json' \
  -d '{"user": "alice", "pass": "secret123"}'
```

## Testing
- Run all tests (Bash): `bash run_tests.sh`
- Windows PowerShell: `./.venv/Scripts/python -m pytest test_files`
- Tests live in `test_files/` and cover:
  - Registration & login flows (forms & JSON API)
  - Validation rules (password length, required email)
  - Alias routes (`/signup`, `/signin`, `/profile`)

## Notes
- Email is **required** (DB enforces `NOT NULL` & unique).
- Password minimum length is **6**.
- The provided `setup.sh` automates environment creation on Bash-based systems.

## Directory Structure
```
app.py            # Flask app entrypoint
auth.py           # Auth blueprint (forms + JSON API)
models.py         # SQLite models/helpers
templates/        # Jinja2 templates
requirements.txt  # Pinned dependencies
run_tests.sh      # Convenience test script
setup.sh          # Bash setup script
defects.txt       # Discovered documentation defects
corrected_readme.md
```
