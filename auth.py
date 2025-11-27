from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
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

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
