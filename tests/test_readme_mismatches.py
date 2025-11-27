import pytest
from app import app

@pytest.fixture
def client(tmp_path):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    db_file = tmp_path / 'test.db'
    app.config['DATABASE'] = str(db_file)
    from models import init_db
    init_db(app)
    with app.test_client() as client:
        yield client


def test_readme_routes_absent(client):
    # README mentions /signup and /signin which are absent
    r1 = client.get('/signup')
    r2 = client.get('/signin')
    assert r1.status_code == 404
    assert r2.status_code == 404


def test_api_routes_absent(client):
    r = client.get('/api/register')
    assert r.status_code == 404


def test_password_min_length_is_6(client):
    # Trying to register with short password should fail validation
    r = client.post('/register', data={
        'username': 'shortpass',
        'email': 'short@example.com',
        'password': '123'
    }, follow_redirects=True)
    assert b'Field must be between 6 and 128 characters long.' in r.data or b'Length' in r.data


def test_email_is_required(client):
    r = client.post('/register', data={
        'username': 'noemail',
        'email': '',
        'password': 's3cr3t1'
    }, follow_redirects=True)
    assert b'This field is required' in r.data or b'Invalid' in r.data
