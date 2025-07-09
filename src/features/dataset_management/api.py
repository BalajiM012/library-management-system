from flask import Blueprint, request, jsonify

dataset_management_bp = Blueprint('dataset_management', __name__, url_prefix='/api/dataset_management')

@dataset_management_bp.route('/add_book', methods=['POST'])
def add_book_dataset():
    from app import db, Book
    data = request.json
    book = Book(title=data['title'], author=data['author'], isbn=data['isbn'], copies=data['copies'])
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book dataset added'})

@dataset_management_bp.route('/add_user', methods=['POST'])
def add_user_dataset():
    from app import db, User
    data = request.json
    user = User(fullname=data['fullname'], email=data['email'], username=data['username'], password=data['password'], role=data.get('role', 'student'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User dataset added'})
