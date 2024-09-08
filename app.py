import os
import secrets
from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response, g
import jwt
from datetime import datetime, timedelta
from functools import wraps
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use environment variable for secret key, generate a random one if not set
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or secrets.token_hex(16)

# Mock user database with roles
users = {
    "user1": {"password": os.getenv('USER1_PASSWORD') or 'password1', "role": "standard"},
    "user2": {"password": os.getenv('USER2_PASSWORD') or secrets.token_urlsafe(10), "role": "standard"},
    "admin": {"password": os.getenv('ADMIN_PASSWORD') or secrets.token_urlsafe(10), "role": "admin"}
}

def get_user_info():
    token = request.cookies.get('jwt')
    if token:
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload['user'], payload['role']
        except:
            return None, None
    return None, None

@app.before_request
def before_request():
    g.user, g.role = get_user_info()

@app.context_processor
def inject_user():
    return dict(user=g.user, role=g.role)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not g.user:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.role != 'admin':
            logger.error("Unauthorized access attempt to admin page")
            return jsonify({"message": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated


@app.route('/')
@token_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = "This is the world where anything goes, as long as it's user and exp."
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username]['password'] == password:
            try:
                token = jwt.encode({
                    'user': username,
                    'role': users[username]['role'],
                    'exp': datetime.now() + timedelta(hours=1)
                }, app.config['SECRET_KEY'], algorithm='HS256')
                response = make_response(redirect(url_for('home')))
                response.set_cookie('jwt', token, httponly=True, secure=True, samesite='Strict')
                return response
            except Exception as e:
                logger.error(f"Error creating JWT: {str(e)}")
                return render_template('login.html', error='An error occurred during login', message=message)
        else:
            logger.warning(f"Failed login attempt for user: {username}")
            return render_template('login.html', error='Invalid credentials', message=message)
    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('jwt')
    return response

@app.route('/admin')
@token_required
@admin_required
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)