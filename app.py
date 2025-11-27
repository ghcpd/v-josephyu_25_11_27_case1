import os
import argparse
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from models import init_db, get_connection, User
from auth import auth_bp

app = Flask(__name__)
# Allow overriding secret key via environment variable for CSRF/session security
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'replace-with-a-strong-secret-key')
app.config['DATABASE'] = 'app.db'  # SQLite file at root of workspace

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)

# Initialize database (create tables if not exist)
init_db(app)

@login_manager.user_loader
def load_user(user_id):
    conn = get_connection(app)
    user = User.get_by_id(conn, int(user_id))
    conn.close()
    return user

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


@app.route('/profile')
@login_required
def profile():
    # Alias for dashboard to satisfy documentation references
    return render_template('dashboard.html', user=current_user)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask app.')
    parser.add_argument('--host', default=os.environ.get('FLASK_RUN_HOST', '127.0.0.1'))
    parser.add_argument('--port', type=int, default=int(os.environ.get('FLASK_RUN_PORT', 5000)))
    args = parser.parse_args()
    app.run(debug=True, host=args.host, port=args.port)
