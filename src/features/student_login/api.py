from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

student_login_bp = Blueprint('student_login', __name__, url_prefix='/api/student_login')

def is_scrypt_hash(pw_hash):
    # Simple check if hash starts with scrypt prefix
    return pw_hash.startswith('scrypt:')

@student_login_bp.route('/signup', methods=['POST'])
def signup():
    from src.app_factory import db
    from src.models import User
    data = request.json
    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({'error': 'User already exists'}), 400
    user = User(
        fullname=data['fullname'],
        email=data['email'],
        username=data['username'],
        password=generate_password_hash(data['password'], method='pbkdf2:sha256'),
        role='student'
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Signup successful'})

@student_login_bp.route('/login', methods=['POST'])
def login():
    from src.app_factory import db
    from src.models import User
    from flask import session
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user:
        print(f"DEBUG: User password hash: {user.password}")  # Debug print
        if is_scrypt_hash(user.password):
            # Verify scrypt hash manually (requires scrypt support)
            # For now, reject login and ask for password reset or rehash
            return jsonify({'error': 'Password uses unsupported hash. Please reset your password.'}), 401
        else:
            if check_password_hash(user.password, data['password']):
                access_token = create_access_token(identity={'id': user.id, 'role': user.role})
                # Set session for compatibility with app.py
                session['user_id'] = user.id
                session['role'] = user.role
                # Rehash password with pbkdf2:sha256 if needed
                if not user.password.startswith('pbkdf2:sha256'):
                    user.password = generate_password_hash(data['password'], method='pbkdf2:sha256')
                    db.session.commit()
                return jsonify({'message': 'Login successful', 'access_token': access_token, 'role': user.role})
    return jsonify({'error': 'Invalid credentials'}), 401

from flask_jwt_extended import get_jwt_identity

@student_login_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # JWT tokens are stateless; client should delete token on logout
    # But we can validate the token subject here to avoid errors
    identity = get_jwt_identity()
    if not identity or not isinstance(identity, dict):
        return jsonify({'msg': 'Subject must be a dict'}), 422
    return jsonify({'message': 'Logged out'})

@student_login_bp.route('/logout', methods=['GET'])
@jwt_required()
def logout_get():
    identity = get_jwt_identity()
    if not identity or not isinstance(identity, dict):
        return jsonify({'msg': 'Subject must be a dict'}), 422
    return jsonify({'message': 'Logged out'})

@student_login_bp.route('/reset_password', methods=['POST'])
def reset_password():
    from src.app_factory import db
    from src.models import User
    data = request.json
    username = data.get('username')
    new_password = data.get('new_password')
    if not username or not new_password:
        return jsonify({'error': 'Username and new_password are required'}), 400
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    from werkzeug.security import generate_password_hash
    user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
    db.session.commit()
    return jsonify({'message': 'Password reset successful'})

@student_login_bp.route('/debug_password_hash/<username>', methods=['GET'])
def debug_password_hash(username):
    from src.models import User
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'username': username, 'password_hash': user.password})

@student_login_bp.route('/force_reset_password/<username>', methods=['POST'])
def force_reset_password(username):
    from src.app_factory import db
    from src.models import User
    from werkzeug.security import generate_password_hash
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    new_password = "TestPass123"
    user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
    db.session.commit()
    return jsonify({'message': f'Password for {username} reset to {new_password}'})
