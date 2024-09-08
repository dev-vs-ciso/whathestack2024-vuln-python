import os
import secrets
from flask import Flask, request, jsonify, render_template, redirect, url_for, g
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from functools import wraps
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization"]}})


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
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
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

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         if not g.user:
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        logger.info(f"Incoming request to {request.path}")
        
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            logger.info(f"Authorization header: {auth_header}")
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                logger.error("Bearer token malformed")
                return jsonify({"message": "Bearer token malformed"}), 401
        
        if not token:
            logger.error("Token is missing")
            return redirect(url_for('login'))
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
            current_role = data['role']
            logger.info(f"Token decoded successfully for user: {current_user}")
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            logger.error("Invalid token")
            return jsonify({"message": "Invalid token"}), 401
        
        return f(current_user, current_role, *args, **kwargs)
    
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
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username]['password'] == password:
            try:
                token = jwt.encode({
                    'user': username,
                    'role': users[username]['role'],
                    'exp': datetime.utcnow() + timedelta(hours=1)
                }, app.config['SECRET_KEY'], algorithm='HS256')
                return jsonify({"success": True, "token": token}), 200
            except Exception as e:
                logger.error(f"Error creating JWT: {str(e)}")
                return jsonify({"success": False, "error": "An error occurred during login"}), 500
        else:
            logger.warning(f"Failed login attempt for user: {username}")
            return jsonify({"success": False, "error": "Invalid credentials"}), 401
    return render_template('login_session_storage.html')


@app.route('/logout')
def logout():
    # Client-side logout (clearing localStorage) will be handled in JavaScript
    return jsonify({"message": "Logout successful"}), 200

@app.route('/admin')
@token_required
@admin_required
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)