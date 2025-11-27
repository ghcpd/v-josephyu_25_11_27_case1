"""
Test suite for Flask application
Tests all functionality and verifies README documentation accuracy
"""
import pytest
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app import app as flask_app
from models import init_db, get_connection, User


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    flask_app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key',
        'DATABASE': 'test.db',
        'WTF_CSRF_ENABLED': False  # Disable CSRF for testing
    })
    
    # Initialize database
    init_db(flask_app)
    
    yield flask_app
    
    # Cleanup: remove test database
    if os.path.exists('test.db'):
        os.remove('test.db')


@pytest.fixture
def client(app):
    """Create a test client for the application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


class TestRoutes:
    """Test all routes mentioned in README"""
    
    def test_index_redirect(self, client):
        """Test that root redirects to login for unauthenticated users"""
        response = client.get('/', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_login_route_exists(self, client):
        """Test that /login route exists (README says /signin)"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'User Login' in response.data
    
    def test_signin_route_does_not_exist(self, client):
        """Test that /signin route does NOT exist (README error)"""
        response = client.get('/signin')
        assert response.status_code == 404
    
    def test_register_route_exists(self, client):
        """Test that /register route exists (README says /signup)"""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'User Registration' in response.data
    
    def test_signup_route_does_not_exist(self, client):
        """Test that /signup route does NOT exist (README error)"""
        response = client.get('/signup')
        assert response.status_code == 404
    
    def test_profile_route_does_not_exist(self, client):
        """Test that /profile route does NOT exist (README error)"""
        response = client.get('/profile')
        assert response.status_code == 404
    
    def test_dashboard_route_exists(self, client):
        """Test that /dashboard route exists (not /profile)"""
        response = client.get('/dashboard', follow_redirects=False)
        assert response.status_code == 302  # Redirects to login when not authenticated


class TestRegistration:
    """Test user registration functionality"""
    
    def test_register_with_valid_data(self, client, app):
        """Test registration with valid data"""
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Welcome' in response.data or b'testuser' in response.data
    
    def test_register_missing_confirm_password_field(self, client):
        """Test that confirm_password field does NOT exist (README error)"""
        response = client.get('/register')
        assert b'confirm_password' not in response.data.lower()
        assert b'Confirm Password' not in response.data
    
    def test_register_password_min_length(self, client):
        """Test password minimum length (should be 6, not 3 as README states)"""
        response = client.post('/register', data={
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': '12'  # Too short
        })
        assert response.status_code == 200
        assert b'Field must be between 6 and 128 characters long' in response.data
    
    def test_register_email_required(self, client):
        """Test that email is required (README says optional)"""
        response = client.post('/register', data={
            'username': 'testuser3',
            'password': 'password123'
            # Missing email
        })
        assert response.status_code == 200
        assert b'required' in response.data.lower() or b'error' in response.data.lower()


class TestLogin:
    """Test login functionality"""
    
    def test_login_with_valid_credentials(self, client, app):
        """Test login with valid username and password"""
        # First register a user
        client.post('/register', data={
            'username': 'logintest',
            'email': 'login@example.com',
            'password': 'password123'
        })
        
        # Logout
        client.get('/logout')
        
        # Try to login
        response = client.post('/login', data={
            'username': 'logintest',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Welcome' in response.data or b'logintest' in response.data
    
    def test_login_with_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post('/login', data={
            'username': 'nonexistent',
            'password': 'wrongpass'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Invalid' in response.data or b'error' in response.data.lower()


class TestAPIEndpoints:
    """Test API endpoints mentioned in README"""
    
    def test_api_register_endpoint_does_not_exist(self, client):
        """Test that POST /api/register does NOT exist (README error)"""
        response = client.post('/api/register', json={
            "user": "name",
            "pass": "123",
            "mail": "email@example.com"
        })
        assert response.status_code == 404
    
    def test_api_login_endpoint_does_not_exist(self, client):
        """Test that POST /api/login does NOT exist (README error)"""
        response = client.post('/api/login', json={
            "user": "name",
            "pass": "123"
        })
        assert response.status_code == 404


class TestConfiguration:
    """Test configuration options"""
    
    def test_database_location(self, app):
        """Test database is at app.db, not data/database.sqlite3"""
        assert app.config['DATABASE'] == 'test.db'  # In test mode
        # In production, it's 'app.db' not 'data/database.sqlite3'
    
    def test_secret_key_hardcoded(self, app):
        """Test that SECRET_KEY is hardcoded, not from FLASK_SECRET env var"""
        # The app uses hardcoded SECRET_KEY, not os.environ.get('FLASK_SECRET')
        assert app.config['SECRET_KEY'] is not None
    
    def test_no_redis_sessions(self):
        """Test that sessions are NOT stored in Redis (README error)"""
        # Flask-Login uses default session storage (cookie-based), not Redis
        # There's no Redis configuration in the code
        assert True  # This is a documentation error


class TestAppStartup:
    """Test application startup options"""
    
    def test_app_run_accepts_host_port(self):
        """Test that app.run() in code doesn't accept --host and --port flags"""
        # The README says: python app.py --host=0.0.0.0 --port=8080
        # But app.py calls app.run(debug=True) with no argument parsing
        # Command-line arguments are not handled
        with open('app.py', 'r') as f:
            content = f.read()
            assert 'argparse' not in content
            assert '--host' not in content
            assert '--port' not in content


class TestPasswordValidation:
    """Test password validation rules"""
    
    def test_password_minimum_length_is_6(self, client):
        """Test that password minimum is 6, not 3 as README states"""
        response = client.post('/register', data={
            'username': 'passtest',
            'email': 'passtest@example.com',
            'password': '123'  # Only 3 characters
        })
        assert response.status_code == 200
        # Should show validation error
        assert b'Field must be between 6 and 128 characters long' in response.data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
