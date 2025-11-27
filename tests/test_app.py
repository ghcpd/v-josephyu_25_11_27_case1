import os
import tempfile
import pytest
from app import app
from models import get_connection

@pytest.fixture
def client(tmp_path, monkeypatch):
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    # Create a new temporary database for each test
    db_file = tmp_path / 'test.db'
    app.config['DATABASE'] = str(db_file)

    # Ensure database is initialized
    from models import init_db
    init_db(app)

    with app.test_client() as client:
        yield client


def test_index_redirects_to_login(client):
    resp = client.get('/')
    assert resp.status_code == 302
    assert '/login' in resp.headers.get('Location')


def test_get_login_page(client):
    resp = client.get('/login')
    assert resp.status_code == 200
    assert b'User Login' in resp.data


def test_register_and_dashboard_access(client):
    # Register a new user
    resp = client.post('/register', data={
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 's3cret1'  # password length >= 6
    }, follow_redirects=True)
    # After register, should be redirected to dashboard
    assert b'Welcome' in resp.data
    assert b'alice' in resp.data

    # Logout then try to login using credentials
    client.get('/logout', follow_redirects=True)
    resp2 = client.post('/login', data={
        'username': 'alice',
        'password': 's3cret1'
    }, follow_redirects=True)
    assert b'Welcome' in resp2.data
    assert b'alice' in resp2.data


def test_register_requires_unique_username_or_email(client):
    # First register
    client.post('/register', data={
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'hunter2'
    }, follow_redirects=True)
    # Try to register with same username
    resp = client.post('/register', data={
        'username': 'bob',
        'email': 'bob2@example.com',
        'password': 'hunter2'
    }, follow_redirects=True)
    assert b'Username is already taken' in resp.data

    # Try to register with same email
    resp2 = client.post('/register', data={
        'username': 'bobby',
        'email': 'bob@example.com',
        'password': 'hunter2'
    }, follow_redirects=True)
    assert b'Email is already registered' in resp2.data
