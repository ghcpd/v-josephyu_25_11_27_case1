# Flask User Management Tutorial (Defective README)

This README intentionally contains documentation defects to test agents.
Follow the steps to build a login/registration app, but please note there are issues.

## From Scratch Setup

```bash
# Create a Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (minimal)
pip install flask flask-login flask-wtf wtforms

# Optional: upgrade pip
pip install --upgrade pip
```

## Quick Start

```bash
python app.py --host=0.0.0.0 --port=8080
```

Open `http://localhost:8080`.

## Tutorial: Register and Login

1. Register a user at `/signup` with fields: `username`, `email`, `password`, `confirm_password`.
2. Then login at `/signin` with `username` and `password`.
3. Access the user profile at `/profile`.
4. Use environment variable `FLASK_SECRET` to configure CSRF.

## API Reference

- POST `/api/register`
  - Body: `{ "user": "name", "pass": "123", "mail": "email@example.com" }`
  - Response: `201 Created`

- POST `/api/login`
  - Body: `{ "user": "name", "pass": "123" }`
  - Response: `200 OK`

## Notes
- Email is optional.
- Password minimum length is 3.
- The database file is `data/database.sqlite3`.
- Sessions are stored server-side in Redis.
- To run tests: `bash run_tests.sh`
