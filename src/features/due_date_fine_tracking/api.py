from flask import Blueprint, render_template, jsonify, request
from datetime import datetime

due_date_fine_tracking_bp = Blueprint('due_date_fine_tracking', __name__, url_prefix='/due_date_fine_tracking')

@due_date_fine_tracking_bp.route('/')
def dashboard():
    return render_template('due_date_fine_tracking.html')

@due_date_fine_tracking_bp.route('/api/borrow_records', methods=['GET'])
def get_borrow_records():
    from app import BorrowRecord
    records = BorrowRecord.query.all()
    result = []
    for r in records:
        result.append({
            'id': r.id,
            'user_id': r.user_id,
            'book_id': r.book_id,
            'borrow_date': r.borrow_date.isoformat(),
            'due_date': r.due_date.isoformat(),
            'return_date': r.return_date.isoformat() if r.return_date else None,
            'fine': r.fine
        })
    return jsonify(result)

@due_date_fine_tracking_bp.route('/api/return_book/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    from app import db, Book, BorrowRecord
    record = BorrowRecord.query.get_or_404(borrow_id)
    if record.return_date:
        return jsonify({'message': 'Book already returned'}), 400
    record.return_date = datetime.utcnow()
    if record.return_date > record.due_date:
        days_overdue = (record.return_date - record.due_date).days
        record.fine = days_overdue * 1.0
    else:
        record.fine = 0.0
    book = Book.query.get(record.book_id)
    book.copies += 1
    db.session.commit()
    return jsonify({'message': 'Book returned successfully', 'fine': record.fine})
