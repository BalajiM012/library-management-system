from flask import Blueprint, jsonify, request, session
from src.models import Book, BorrowRecord, User
from src.app_factory import db
from datetime import datetime

student_bp = Blueprint('student', __name__, url_prefix='/api/student')

@student_bp.route('/get_books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_list = []
    for book in books:
        books_list.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'copies': book.copies
        })
    return jsonify(books_list)

@student_bp.route('/submit_book', methods=['POST'])
def submit_book():
    data = request.json
    borrow_id = data.get('borrow_id')
    borrow_record = BorrowRecord.query.filter_by(id=borrow_id).first()
    if not borrow_record:
        return jsonify({'error': 'Borrow record not found'}), 404
    if borrow_record.return_date:
        return jsonify({'error': 'Book already returned'}), 400
    borrow_record.return_date = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Book returned successfully'})

@student_bp.route('/borrowed_books_history', methods=['GET'])
def borrowed_books_history():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    records = BorrowRecord.query.filter_by(user_id=user_id).all()
    history = []
    for r in records:
        history.append({
            'id': r.id,
            'book': {
                'title': r.book.title,
                'author': r.book.author,
                'isbn': r.book.isbn
            },
            'borrow_date': r.borrow_date.isoformat() if r.borrow_date else None,
            'due_date': r.due_date.isoformat() if r.due_date else None,
            'return_date': r.return_date.isoformat() if r.return_date else None,
            'fine': r.fine
        })
    return jsonify(history)

@student_bp.route('/fine_calculator', methods=['GET'])
def fine_calculator():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    records = BorrowRecord.query.filter_by(user_id=user_id).all()
    total_fine = sum(r.fine for r in records if r.fine)
    return jsonify({'total_fine': total_fine})

@student_bp.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'fullname': user.fullname,
        'username': user.username,
        'email': user.email,
        'role': user.role
    })
