# Test Suite Documentation

## Overview

This project includes a comprehensive test suite with 50+ test cases covering:
- Database initialization and operations
- User model functionality
- Registration and login flows
- Form validation
- CSRF protection
- Session management
- Endpoint functionality

## Running Tests

### Quick Start

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
bash run_tests.sh

# Run tests with coverage report
bash run_tests.sh --coverage
```

### Using pytest Directly

```bash
# Run all tests with verbose output
pytest test_app.py -v

# Run specific test class
pytest test_app.py::TestUserModel -v

# Run specific test
pytest test_app.py::TestUserModel::test_user_creation -v

# Run tests with output printed
pytest test_app.py -v -s

# Run with coverage
pytest test_app.py --cov=. --cov-report=html

# Run tests matching a keyword
pytest test_app.py -k "registration" -v

# Run and stop on first failure
pytest test_app.py -x -v
```

## Test Structure

### TestAppSetup
Tests for Flask app initialization and configuration.

**Tests:**
- `test_app_exists` - Verifies Flask app is created
- `test_app_testing_mode` - Verifies app can be configured for testing
- `test_secret_key_configured` - Checks SECRET_KEY is set
- `test_database_configured` - Verifies DATABASE config exists

### TestDatabase
Tests for database initialization and constraints.

**Tests:**
- `test_database_initializes` - Verifies users table is created
- `test_users_table_has_columns` - Checks all required columns exist
- `test_username_unique_constraint` - Verifies username uniqueness is enforced
- `test_email_unique_constraint` - Verifies email uniqueness is enforced

### TestUserModel
Tests for User model functionality.

**Tests:**
- `test_user_creation` - Creating a new user
- `test_get_user_by_username` - Retrieving user by username
- `test_get_by_id` - Retrieving user by ID
- `test_password_hashing` - Password is properly hashed
- `test_password_verification_correct` - Correct password verification
- `test_password_verification_incorrect` - Incorrect password rejected

### TestRegistrationEndpoint
Tests for /register endpoint.

**Tests:**
- `test_register_get_returns_form` - GET returns registration form
- `test_register_success` - Successful registration
- `test_register_duplicate_username` - Duplicate username rejected
- `test_register_duplicate_email` - Duplicate email rejected
- `test_register_invalid_email` - Invalid email format rejected
- `test_register_password_too_short` - Short passwords rejected
- `test_register_missing_username` - Missing username validation
- `test_register_missing_email` - Missing email validation
- `test_register_username_too_short` - Too short username rejected

### TestLoginEndpoint
Tests for /login endpoint.

**Tests:**
- `test_login_get_returns_form` - GET returns login form
- `test_login_success` - Successful login
- `test_login_wrong_password` - Wrong password rejected
- `test_login_nonexistent_user` - Nonexistent user rejected
- `test_login_missing_username` - Missing username validation
- `test_login_missing_password` - Missing password validation

### TestDashboardEndpoint
Tests for dashboard access control.

**Tests:**
- `test_dashboard_requires_login` - Unauthenticated users redirected
- `test_dashboard_accessible_after_login` - Authenticated users can access

### TestLogoutEndpoint
Tests for logout functionality.

**Tests:**
- `test_logout_requires_login` - Logout requires authentication
- `test_logout_success` - Successful logout redirects to login

### TestIndexRoute
Tests for home page redirect logic.

**Tests:**
- `test_index_redirects_unauthenticated_to_login` - Guests redirected to login
- `test_index_redirects_authenticated_to_dashboard` - Users redirected to dashboard

### TestAPIEndpoints
Tests for API endpoints (verifying they don't exist).

**Tests:**
- `test_api_register_not_implemented` - /api/register returns 404
- `test_api_login_not_implemented` - /api/login returns 404

### TestCSRFProtection
Tests for CSRF token presence in forms.

**Tests:**
- `test_csrf_token_in_register_form` - Register form has CSRF token
- `test_csrf_token_in_login_form` - Login form has CSRF token

### TestEndpointNames
Tests for corrected endpoint names.

**Tests:**
- `test_register_endpoint_exists` - /register endpoint works
- `test_login_endpoint_exists` - /login endpoint works
- `test_signup_not_found` - /signup endpoint doesn't exist
- `test_signin_not_found` - /signin endpoint doesn't exist
- `test_profile_not_found` - /profile endpoint doesn't exist

### TestPasswordValidation
Tests for password validation rules.

**Tests:**
- `test_password_minimum_length_is_6` - Minimum length enforced
- `test_password_exactly_6_characters_accepted` - 6 char passwords accepted

### TestEmailValidation
Tests for email validation rules.

**Tests:**
- `test_email_is_required` - Email is mandatory
- `test_email_format_validation` - Email format validated

## Test Fixtures

### client
Provides a Flask test client with a temporary SQLite database.
- Creates isolated test database for each test
- Cleans up after test completes
- Configured with TESTING=True

### runner
Provides a Flask CLI test runner for command-line testing.

## Expected Test Results

All 50+ tests should pass with no failures:

```
test_app.py::TestAppSetup::test_app_exists PASSED
test_app.py::TestAppSetup::test_app_testing_mode PASSED
test_app.py::TestAppSetup::test_secret_key_configured PASSED
test_app.py::TestAppSetup::test_database_configured PASSED
test_app.py::TestDatabase::test_database_initializes PASSED
test_app.py::TestDatabase::test_users_table_has_columns PASSED
test_app.py::TestDatabase::test_username_unique_constraint PASSED
test_app.py::TestDatabase::test_email_unique_constraint PASSED
... (more tests)

========================== 50+ passed in X.XXs ==========================
```

## Coverage Goals

The test suite aims for >80% code coverage:

- **Models**: 95%+ coverage of User model
- **Auth routes**: 90%+ coverage of login/register/logout
- **Database**: 100% coverage of init_db and get_connection
- **Validation**: 90%+ coverage of form validators

Run with coverage:
```bash
pytest test_app.py --cov=. --cov-report=html --cov-report=term-missing
```

## Continuous Integration

For CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pytest test_app.py -v --cov=. --cov-report=xml
```

## Troubleshooting Tests

### Tests fail with "ModuleNotFoundError"
```bash
# Make sure you're in the project root and virtual environment is activated
source .venv/bin/activate
cd /path/to/project
```

### Tests fail with database errors
```bash
# Tests create temporary databases, but if you have permission issues:
# Delete any stale app.db files
rm -f app.db
# Re-run tests
pytest test_app.py -v
```

### Tests hang or timeout
```bash
# Use timeout flag
pytest test_app.py -v --timeout=10
```

### Need to see print output
```bash
# Use -s flag
pytest test_app.py -v -s
```

## Test Development

To add new tests:

1. Create test function starting with `test_`
2. Use appropriate fixture (e.g., `client`)
3. Follow naming convention: `test_[feature]_[behavior]`
4. Add docstring describing test purpose
5. Use assertions to verify behavior

Example:
```python
def test_new_feature(client):
    """Test description of what this tests"""
    response = client.get('/endpoint')
    assert response.status_code == 200
    assert b'expected_content' in response.data
```

## Performance

Test suite execution times:
- Quick run (no coverage): ~5-10 seconds
- Full run with coverage: ~10-15 seconds
- Parallel execution: pytest-xdist can speed up

```bash
# Run tests in parallel (requires pytest-xdist)
pip install pytest-xdist
pytest test_app.py -v -n auto
```

## Maintenance

### Updating tests after code changes
1. Run full test suite: `pytest test_app.py -v`
2. Check coverage: `pytest test_app.py --cov`
3. Update failing tests or implementation
4. Verify all tests pass

### Adding test dependencies
Add to requirements.txt:
```
pytest>=9.0.0
pytest-cov>=4.0.0
```

Then reinstall:
```bash
pip install -r requirements.txt
```

## See Also

- `test_app.py` - Full test suite
- `pytest.ini` - Pytest configuration
- `run_tests.sh` - Automated test runner
- `corrected_readme.md` - Application documentation
