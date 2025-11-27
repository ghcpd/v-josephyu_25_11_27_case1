import os
import tempfile
import pytest
from app import app
from models import init_db, get_connection

@pytest.fixture
def client(tmp_path):
    db_file = tmp_path / "test_app.db"
    app.config['DATABASE'] = str(db_file)
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['TESTING'] = True
    # init DB
    init_db(app)
    with app.test_client() as client:
        yield client


def test_register_and_login_flow(client):
    # Register
    rv = client.post('/register', data={'username': 'alice', 'email': 'alice@example.com', 'password': 'secret123'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'You are logged in' in rv.data

    # Logout
    rv = client.get('/logout', follow_redirects=True)
    assert rv.status_code == 200
    # Login with same credentials
    rv = client.post('/login', data={'username': 'alice', 'password': 'secret123'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'You are logged in' in rv.data


def test_wrong_endpoints_return_404(client):
    # README mentions /signup and /signin, but app uses /register and /login
    assert client.get('/signup').status_code == 404
    assert client.get('/signin').status_code == 404


def test_api_endpoints_absent(client):
    assert client.post('/api/register', json={'user': 'a', 'pass': '1', 'mail': 'a@example.com'}).status_code in (404, 405)
    assert client.post('/api/login', json={'user': 'a', 'pass': '1'}).status_code in (404, 405)


def test_register_requires_email_and_password_length(client):
    # Missing email should cause form to fail and not log in
    rv = client.post('/register', data={'username': 'bob', 'email': '', 'password': 'pwd'}, follow_redirects=True)
    assert (b'This field is required' in rv.data) or (b'Enter a valid email address' in rv.data)
    # Password shorter than 6 should fail validation
    rv = client.post('/register', data={'username': 'bob2', 'email': 'bob2@example.com', 'password': '123'}, follow_redirects=True)
    assert b'Field must be between 6 and 128 characters long.' in rv.data
