import pytest
from app import app, init_db

@pytest.fixture
def client(tmp_path):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    test_db = tmp_path / "test_app.db"
    app.config['DATABASE'] = str(test_db)
    init_db(app)
    with app.test_client() as client:
        yield client


def test_short_password_fails(client):
    # Password length enforced to be >= 6
    resp = client.post('/register', data={
        'username': 'shorty',
        'email': 'shorty@example.com',
        'password': '123',
        'submit': True,
    }, follow_redirects=True)
    # Registration should not succeed with a too-short password; ensure we did not get to the dashboard
    assert b'Hello, <strong>' not in resp.data


def test_email_required(client):
    # Email field is required (DataRequired and Email validators are present)
    resp = client.post('/register', data={
        'username': 'noemail',
        'email': '',
        'password': 'password123',
        'submit': True,
    }, follow_redirects=True)
    assert b'This field is required.' in resp.data

