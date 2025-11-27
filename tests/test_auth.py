import os
import tempfile
import pytest
from app import app, init_db
from models import get_connection

@pytest.fixture
def client(tmp_path):
    # Configure app for testing
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # disable CSRF for form posting
    test_db = tmp_path / "test_app.db"
    app.config['DATABASE'] = str(test_db)

    # Initialize database
    init_db(app)

    with app.test_client() as client:
        yield client


def test_register_and_login_flow(client):
    # Register a new user with form POST
    resp = client.post('/register', data={
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'password123',
        'submit': True,
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Hello, <strong>alice</strong>!' in resp.data

    # Logout
    resp = client.get('/logout', follow_redirects=True)
    assert resp.status_code == 200
    assert b'User Login' in resp.data

    # Login with registered user
    resp = client.post('/login', data={
        'username': 'alice',
        'password': 'password123',
        'submit': True,
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Hello, <strong>alice</strong>!' in resp.data


def test_register_duplicate_username(client):
    # Register user
    resp = client.post('/register', data={
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'pass1word',
        'submit': True,
    }, follow_redirects=True)
    assert resp.status_code == 200

    # Attempt to register with same username
    resp = client.post('/register', data={
        'username': 'bob',
        'email': 'another@example.com',
        'password': 'pass1word',
        'submit': True,
    }, follow_redirects=True)
    assert b'Username is already taken' in resp.data


def test_register_duplicate_email(client):
    # Register user
    resp = client.post('/register', data={
        'username': 'charlie',
        'email': 'charlie@example.com',
        'password': 'pass1word',
        'submit': True,
    }, follow_redirects=True)
    assert resp.status_code == 200

    # Attempt to register with same email
    resp = client.post('/register', data={
        'username': 'charlie2',
        'email': 'charlie@example.com',
        'password': 'pass1word',
        'submit': True,
    }, follow_redirects=True)
    assert b'Email is already registered' in resp.data


def test_api_endpoints_absent(client):
    # Verify README claimed /api/register and /api/login exist; they should not.
    resp = client.post('/api/register', json={"user":"x","pass":"a","mail":"a@b.com"})
    assert resp.status_code == 404

    resp = client.post('/api/login', json={"user":"x","pass":"a"})
    assert resp.status_code == 404

