from flask import Blueprint, request, jsonify, abort
from src.app_factory import db
from src.models import User

manage_users_bp = Blueprint('manage_users', __name__, url_prefix='/manage_users')

@manage_users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
    return jsonify(users_data)

@manage_users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email
    }
    return jsonify(user_data)

@manage_users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not 'fullname' in data or not 'username' in data or not 'email' in data or not 'password' in data:
        abort(400, description="Missing required fields")
    if User.query.filter_by(username=data['username']).first():
        abort(400, description="Username already exists")
    new_user = User(
        fullname=data['fullname'],
        username=data['username'],
        email=data['email'],
        password=data['password']  # Note: In production, hash the password!
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created', 'user_id': new_user.id}), 201

@manage_users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")
    data = request.get_json()
    if not data:
        abort(400, description="No data provided")
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    if 'password' in data:
        user.password = data['password']  # Note: In production, hash the password!
    db.session.commit()
    return jsonify({'message': 'User updated'})

@manage_users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})
