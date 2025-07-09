from flask import Blueprint, jsonify, request
from src.models import BorrowRecord  # Assuming this model exists and has fine info
from datetime import datetime

due_date_fine_tracking_bp = Blueprint('due_date_fine_tracking', __name__, url_prefix='/due_date_fine_tracking/api')

@due_date_fine_tracking_bp.route('/borrow_records', methods=['GET'])
def get_borrow_records():
    records = BorrowRecord.query.all()
    result = []
    for r in records:
        result.append({
            'id': r.id,
            'user_id': r.user_id,
            'book_id': r.book_id,
            'borrow_date': r.borrow_date.isoformat() if r.borrow_date else None,
            'due_date': r.due_date.isoformat() if r.due_date else None,
            'return_date': r.return_date.isoformat() if r.return_date else None,
            'fine': r.fine
        })
    return jsonify(result)

@due_date_fine_tracking_bp.route('/return_book/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    record = BorrowRecord.query.get_or_404(borrow_id)
    if record.return_date:
        return jsonify({'message': 'Book already returned', 'fine': record.fine})
    record.return_date = datetime.utcnow()
    # Calculate fine if returned late
    if record.due_date and record.return_date > record.due_date:
        delta = (record.return_date - record.due_date).days
        record.fine = delta * 1  # Assuming $1 fine per day late
    else:
        record.fine = 0
    from src.app_factory import db
    db.session.commit()
    return jsonify({'message': 'Book returned successfully', 'fine': record.fine})
