from flask import Blueprint, request, jsonify, session

user_login_bp = Blueprint('user_login', __name__, url_prefix='/user')

@user_login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # TODO: Implement authentication logic, replace with proper password check
    if username == "admin" and password == "password":
        session['user'] = {'username': 'admin'}
        return jsonify({"message": "Login successful", "user": {"username": "admin"}})
    else:
        return jsonify({"error": "Invalid credentials"}), 401
