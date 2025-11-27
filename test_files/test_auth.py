import pytest

from models import init_db


@pytest.fixture
def app(tmp_path):
    from app import app as flask_app
    flask_app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        DATABASE=str(tmp_path / 'app.db'),
        SECRET_KEY='test-secret',
    )
    init_db(flask_app)
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, username='alice', password='secret123', email='alice@example.com'):
    return client.post(
        '/register',
        data={'username': username, 'password': password, 'email': email},
        follow_redirects=False,
    )


def login(client, username='alice', password='secret123'):
    return client.post(
        '/login',
        data={'username': username, 'password': password},
        follow_redirects=False,
    )


def test_register_and_dashboard_access(client):
    resp = register(client)
    assert resp.status_code in (302, 303)
    dash = client.get('/dashboard')
    assert dash.status_code == 200
    assert b'alice' in dash.data


def test_register_duplicate_username(client):
    first = register(client)
    assert first.status_code in (302, 303)
    second = register(client)
    assert second.status_code == 200
    assert b'Username is already taken' in second.data


def test_login_success(client):
    register(client)
    client.get('/logout')
    resp = login(client)
    assert resp.status_code in (302, 303)
    dash = client.get('/dashboard')
    assert dash.status_code == 200
    assert b'alice' in dash.data


def test_login_invalid_password(client):
    register(client)
    resp = login(client, password='wrongpass')
    assert resp.status_code == 200
    assert b'Invalid username or password' in resp.data


def test_validation_missing_email(client):
    resp = register(client, email='')
    assert resp.status_code == 200
    assert b'This field is required' in resp.data


def test_validation_short_password(client):
    resp = register(client, password='123')
    assert resp.status_code == 200
    assert b'Field must be between 6 and 128 characters long' in resp.data


def test_alias_routes(client):
    # GET aliases should render forms
    assert client.get('/signup').status_code == 200
    assert client.get('/signin').status_code == 200
    # Login to access /profile alias
    register(client)
    profile = client.get('/profile')
    assert profile.status_code == 200


def test_api_register_and_login(client):
    r = client.post('/api/register', json={'user': 'bob', 'pass': 'secret123', 'mail': 'bob@example.com'})
    assert r.status_code == 201
    l = client.post('/api/login', json={'user': 'bob', 'pass': 'secret123'})
    assert l.status_code == 200


def test_api_register_duplicate(client):
    client.post('/api/register', json={'user': 'cara', 'pass': 'secret123', 'mail': 'cara@example.com'})
    dup = client.post('/api/register', json={'user': 'cara', 'pass': 'secret123', 'mail': 'cara@example.com'})
    assert dup.status_code == 409


def test_api_login_invalid(client):
    client.post('/api/register', json={'user': 'dan', 'pass': 'secret123', 'mail': 'dan@example.com'})
    bad = client.post('/api/login', json={'user': 'dan', 'pass': 'wrong'})
    assert bad.status_code == 401


def test_api_missing_fields(client):
    resp = client.post('/api/login', json={})
    assert resp.status_code == 400
