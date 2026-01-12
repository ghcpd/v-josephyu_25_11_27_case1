# Flask User Management Tutorial (Corrected)

This is the corrected version of the README with accurate documentation.
All examples have been verified against the actual implementation.

## From Scratch Setup

```bash
# Create a Python virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install flask flask-login flask-wtf wtforms email_validator

# Optional: upgrade pip
pip install --upgrade pip
```

## Quick Start

```bash
# Simply run the application
python app.py
```

The application will start on `http://127.0.0.1:5000` by default.

**Alternative Start Options:**

```bash
# Using Flask CLI with custom host and port
set FLASK_APP=app.py  # Windows
# or: export FLASK_APP=app.py  # Linux/Mac
flask run --host=0.0.0.0 --port=8080
```

## Tutorial: Register and Login

### 1. Register a New User

Navigate to `/register` (not `/signup`) with the following fields:
- `username` - Required, 3-32 characters
- `email` - Required (not optional), must be a valid email format
- `password` - Required, minimum 6 characters (not 3)

**Note:** There is no `confirm_password` field in the registration form.

**Example:**
1. Go to: `http://localhost:5000/register`
2. Fill in:
   - Username: `johndoe`
   - Email: `john@example.com`
   - Password: `password123` (min 6 chars)
3. Click "Register"
4. You will be automatically logged in and redirected to the dashboard

### 2. Login

Navigate to `/login` (not `/signin`) with:
- `username` - Your registered username
- `password` - Your password

**Example:**
1. Go to: `http://localhost:5000/login`
2. Enter your username and password
3. Click "Login"
4. You will be redirected to the dashboard

### 3. Access Dashboard

After logging in, access your user dashboard at `/dashboard` (not `/profile`):
- URL: `http://localhost:5000/dashboard`
- Displays: Welcome message with username
- Action: Logout button

### 4. Logout

Click the "Log Out" button on the dashboard or navigate to `/logout`

## Configuration

### Secret Key

The application uses a hardcoded SECRET_KEY for session management:
```python
app.config['SECRET_KEY'] = 'replace-with-a-strong-secret-key'
```

**To use an environment variable (requires code modification):**
```python
import os
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'default-secret-key')
```

Then set the environment variable:
```bash
# Windows
set FLASK_SECRET=your-secret-key-here

# Linux/Mac
export FLASK_SECRET=your-secret-key-here
```

### Database

- **Location:** `app.db` in the root directory (not `data/database.sqlite3`)
- **Type:** SQLite3
- **Schema:** Single `users` table with columns: id, username, password_hash, email

### Session Storage

Sessions are stored using Flask's default cookie-based session management with Flask-Login.
**Note:** Redis is NOT used for session storage.

## Application Routes

### Web Routes (HTML Forms)

| Route | Methods | Description | Authentication Required |
|-------|---------|-------------|------------------------|
| `/` | GET | Redirects to `/login` or `/dashboard` | No |
| `/login` | GET, POST | User login form | No |
| `/register` | GET, POST | User registration form | No |
| `/logout` | GET | Logout current user | Yes |
| `/dashboard` | GET | User dashboard/profile | Yes |

### API Routes

**Note:** This application does NOT implement JSON API endpoints.
There are no `/api/register` or `/api/login` routes.
All interactions are through HTML forms.

## Validation Rules

### Username
- **Required:** Yes
- **Minimum length:** 3 characters
- **Maximum length:** 32 characters
- **Unique:** Yes

### Email
- **Required:** Yes (not optional)
- **Format:** Must be valid email format
- **Maximum length:** 255 characters
- **Unique:** Yes

### Password
- **Required:** Yes
- **Minimum length:** 6 characters (not 3)
- **Maximum length:** 128 characters
- **Hashing:** Uses Werkzeug's generate_password_hash (PBKDF2)

## Testing

Run the test suite with pytest:

```bash
# Run all tests
pytest test_app.py -v

# Or use the provided script
bash run_tests.sh
```

## Project Structure

```
.
├── app.py                 # Main application file
├── auth.py               # Authentication blueprint (login, register, logout)
├── models.py             # Database models (User class, DB functions)
├── requirements.txt      # Python dependencies
├── app.db               # SQLite database (created on first run)
├── templates/
│   ├── base.html        # Base template with Bootstrap
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   └── dashboard.html   # User dashboard
└── test_app.py          # Test suite
```

## Dependencies

```
Flask==3.0.0
Flask-Login==0.6.3
Flask-WTF==1.2.1
WTForms==3.1.2
Werkzeug==3.0.1
email_validator==2.2.0
pytest  # For testing
```

## Common Issues and Solutions

### Issue: "email_validator is not installed"
**Solution:** Install email_validator:
```bash
pip install email_validator
```

### Issue: "404 Not Found" when accessing /signup or /signin
**Solution:** Use correct routes: `/register` for registration and `/login` for login

### Issue: "404 Not Found" when accessing /profile
**Solution:** Use `/dashboard` instead of `/profile`

### Issue: Password validation fails with 3 characters
**Solution:** Passwords must be at least 6 characters long

### Issue: Registration fails without email
**Solution:** Email is required, not optional

## Security Notes

1. **Change the SECRET_KEY** before deploying to production
2. **Use HTTPS** in production to protect passwords and session cookies
3. **Consider rate limiting** for login and registration endpoints
4. **Add password confirmation** field for better UX (currently not implemented)
5. **Implement password strength requirements** beyond minimum length
6. **Add email verification** to prevent fake registrations

## Development vs Production

### Development (Current Setup)
- Debug mode enabled
- SQLite database
- Hardcoded secret key
- No HTTPS

### Production Recommendations
- Set `debug=False`
- Use PostgreSQL or MySQL
- Use environment variables for secrets
- Enable HTTPS
- Add proper logging
- Implement rate limiting
- Add CSRF protection (Flask-WTF provides this)
- Use gunicorn or similar WSGI server

## Example Usage

### Complete Workflow

```bash
# 1. Setup
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Start application
python app.py

# 3. Open browser to http://localhost:5000

# 4. Register new user
#    Navigate to /register
#    Fill in: username, email, password
#    Submit

# 5. You're automatically logged in and see dashboard

# 6. Logout
#    Click "Log Out" button

# 7. Login again
#    Navigate to /login
#    Enter username and password
#    Submit

# 8. Access dashboard
#    Already at /dashboard after login
```

## Contributing

When contributing, please:
1. Keep documentation synchronized with code
2. Update tests when adding features
3. Follow existing code style
4. Test all changes locally before submitting

## License

This is a tutorial project for educational purposes.
