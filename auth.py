from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from models import get_connection, User

auth_bp = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=32)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=32)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField('Register')

"""
Note: user_loader is registered in app.py to avoid circular imports.
"""

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        conn = get_connection(current_app)
        user = User.get_by_username(conn, form.username.data)
        if user and user.verify_password(form.password.data):
            login_user(user)
            conn.close()
            return redirect(url_for('dashboard'))
        conn.close()
        flash('Invalid username or password')
    return render_template('login.html', form=form)


# Alias to satisfy documentation references
@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    return login()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        conn = get_connection(current_app)
        existing = User.get_by_username(conn, form.username.data)
        if existing:
            flash('Username is already taken')
            conn.close()
            return render_template('register.html', form=form)
        # Check email uniqueness
        cur = conn.cursor()
        cur.execute('SELECT id FROM users WHERE email = ?', (form.email.data,))
        if cur.fetchone():
            flash('Email is already registered')
            conn.close()
            return render_template('register.html', form=form)
        user = User.create(conn, form.username.data, form.password.data, form.email.data)
        login_user(user)
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)


# Alias to satisfy documentation references
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    return register()

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# JSON API endpoints
def _extract_creds(data: dict):
    # Accept both doc-specified keys and canonical keys
    username = data.get('username') or data.get('user')
    password = data.get('password') or data.get('pass')
    email = data.get('email') or data.get('mail')
    return username, password, email


@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json(force=True, silent=True) or {}
    username, password, email = _extract_creds(data)

    # Basic validation mirroring WTForms rules
    errors = {}
    if not username or not (3 <= len(username) <= 32):
        errors['user'] = 'Username required (3-32 chars).'
    if not password or not (6 <= len(password) <= 128):
        errors['pass'] = 'Password required (6-128 chars).'
    if not email:
        errors['mail'] = 'Email required.'
    if errors:
        return jsonify({'status': 'error', 'errors': errors}), 400

    conn = get_connection(current_app)
    try:
        existing = User.get_by_username(conn, username)
        if existing:
            return jsonify({'status': 'error', 'errors': {'user': 'Username already exists'}}), 409
        cur = conn.cursor()
        cur.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cur.fetchone():
            return jsonify({'status': 'error', 'errors': {'mail': 'Email already exists'}}), 409
        user = User.create(conn, username, password, email)
        return jsonify({'status': 'ok', 'id': user.id, 'user': user.username}), 201
    finally:
        conn.close()


@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json(force=True, silent=True) or {}
    username, password, _ = _extract_creds(data)
    if not username or not password:
        return jsonify({'status': 'error', 'errors': {'user': 'Username and password required'}}), 400

    conn = get_connection(current_app)
    try:
        user = User.get_by_username(conn, username)
        if user and user.verify_password(password):
            login_user(user)
            return jsonify({'status': 'ok', 'user': user.username}), 200
        return jsonify({'status': 'error', 'errors': {'auth': 'Invalid credentials'}}), 401
    finally:
        conn.close()
