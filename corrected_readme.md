# Flask User Management Tutorial (CORRECTED README)

This README has been corrected to match the actual implementation. All examples have been verified to work.

## From Scratch Setup

```bash
# Create a Python virtual environment
python3 -m venv .venv

# Activate the environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install flask flask-login flask-wtf wtforms email_validator pytest

# Optional: upgrade pip
pip install --upgrade pip
```

## Quick Start

```bash
# Run the Flask application (uses default localhost:5000)
python app.py

# The app will be available at: http://localhost:5000
```

**Note:** The command `python app.py --host=0.0.0.0 --port=8080` from the original README **does not work**. Flask's app.run() method does not accept command-line arguments. 

To specify a custom host and port, modify `app.py`:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

Alternatively, use Flask CLI:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=8080
```

## Tutorial: Register and Login

1. **Register a user** at `/register` (not `/signup`) with fields:
   - `username` (3-32 characters)
   - `email` (required, must be valid email)
   - `password` (minimum 6 characters)

2. **Login** at `/login` (not `/signin`) with:
   - `username`
   - `password`

3. **View dashboard** at `/dashboard` after successful login

**Note:** The `/profile` endpoint mentioned in the original README does not exist. Users can access `/dashboard` instead.

## Environment Configuration

Set these environment variables for production use:

```bash
# Set a secure secret key for CSRF and session management
export FLASK_SECRET=your-very-secret-key-here-minimum-32-chars

# (Optional) Set Flask environment
export FLASK_ENV=development
export FLASK_APP=app.py
```

**Note:** The original README stated to use `FLASK_SECRET` environment variable, but the implementation currently uses a hardcoded value in `app.py`. For proper production deployment, modify `app.py` to read from the environment:

```python
import os
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'replace-with-a-strong-secret-key')
```

## API Reference

**Important:** The original README documented `/api/register` and `/api/login` JSON API endpoints, but **these endpoints do not exist in the current implementation**. The application only provides HTML form endpoints at `/register` and `/login`.

If you need JSON API endpoints, they would need to be implemented separately:

```python
# Example (NOT currently implemented):
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    # Validate and create user
    return jsonify({'status': 'created'}), 201

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    # Validate and login user
    return jsonify({'status': 'ok'}), 200
```

Current form-based endpoints:
- `POST /register` - HTML form submission
- `POST /login` - HTML form submission
- `POST /logout` - Logout user

## Database

- **Database file:** `app.db` (SQLite file in workspace root)
- **Note:** The original README mentioned `data/database.sqlite3` - this is **incorrect**. The actual database file is `app.db`.
- **Schema:** Automatically created on first run with `users` table containing:
  - `id` (INTEGER PRIMARY KEY)
  - `username` (TEXT UNIQUE NOT NULL)
  - `password_hash` (TEXT NOT NULL)
  - `email` (TEXT UNIQUE NOT NULL)

## Session Management

- Sessions are stored in **secure, httpOnly cookies** managed by Flask-Login
- **Note:** The original README mentioned Redis for session storage - this is **incorrect**. The implementation uses Flask's default secure cookie sessions.
- Session data is cryptographically signed and cannot be tampered with by clients
- Sessions are deleted when the browser closes (by default)

## Form Validation Rules

| Field | Min Length | Max Length | Rules |
|-------|-----------|-----------|--------|
| username | 3 | 32 | Required, unique |
| email | - | 255 | Required, valid format, unique |
| password | 6 | 128 | Required, minimum 6 chars |

**Note:** The original README stated "Password minimum length is 3" - this is **incorrect**. The actual minimum is **6 characters**.

## Running Tests

Run the test suite to verify everything works:

```bash
# Using pytest (all tests should pass)
pytest test_app.py -v

# With coverage report
pytest test_app.py --cov=. -v
```

See `run_tests.sh` for automated testing.

## Setup Script

A setup script is provided to automate environment configuration:

```bash
bash setup.sh
```

This script:
1. Creates virtual environment
2. Installs dependencies
3. Initializes the database
4. Creates a test user for development

## Corrected Endpoints Summary

| Endpoint | Method | Purpose | Original README |
|----------|--------|---------|-----------------|
| `/` | GET | Redirect to login or dashboard | - |
| `/register` | GET/POST | Register new user | Listed as `/signup` ❌ |
| `/login` | GET/POST | User login | Listed as `/signin` ❌ |
| `/logout` | POST | User logout | ✓ |
| `/dashboard` | GET | User dashboard (protected) | ✓ |
| `/profile` | GET | User profile | **Does not exist** ❌ |
| `/api/register` | POST | JSON API register | **Does not exist** ❌ |
| `/api/login` | POST | JSON API login | **Does not exist** ❌ |

## Original README Defects Summary

The original README contained the following **11 critical defects**:

1. ✗ CLI arguments `--host` and `--port` don't work
2. ✗ `/api/register` and `/api/login` JSON endpoints don't exist
3. ✗ `/signup` should be `/register`
4. ✗ `/signin` should be `/login`
5. ✗ API field names don't match form fields (user→username, pass→password, mail→email)
6. ✗ Password minimum is 6, not 3
7. ✗ Email is required, not optional
8. ✗ `/profile` endpoint doesn't exist
9. ✗ `FLASK_SECRET` environment variable is not read
10. ✗ Database is `app.db`, not `data/database.sqlite3`
11. ✗ Redis sessions not implemented; uses secure cookies instead

For detailed information about each defect, see `defects.txt`.

## Additional Notes

- The application is configured for development use by default
- Do not use the hardcoded `SECRET_KEY` in production
- For production, set a strong `FLASK_SECRET` environment variable
- Database is SQLite (suitable for development; use PostgreSQL for production)
- CSRF protection is enabled via Flask-WTF
- Email validation requires valid email format

## Troubleshooting

**Issue:** "ModuleNotFoundError: No module named 'flask'"
- Solution: Run `pip install -r requirements.txt` in activated virtual environment

**Issue:** Database errors on login
- Solution: Delete `app.db` and restart the app to recreate the database

**Issue:** CSRF validation errors on form submission
- Solution: Ensure SECRET_KEY is set and the same across requests

**Issue:** "Port 5000 already in use"
- Solution: Change port in `app.py` or kill the process using port 5000
