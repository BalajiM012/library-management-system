from flask import Blueprint, jsonify
from src.models import BorrowRecord  # Fee model not found, removed import and related code

history_bp = Blueprint('history', __name__, url_prefix='/api/history')

@history_bp.route('/borrow', methods=['GET'])
def get_borrow_history():
    records = BorrowRecord.query.all()
    history = []
    for r in records:
        history.append({
            'serial_number': r.id,
            'book_id': r.book_id,
            'book_title': r.book.title if r.book else '',
            'borrow_date': r.borrow_date.isoformat() if r.borrow_date else None,
            'return_date': r.return_date.isoformat() if r.return_date else None,
        })
    return jsonify(history)

@history_bp.route('/fees', methods=['GET'])
def get_fees():
    # Fee model not found, returning empty fees data
    return jsonify({'total_fees': 0, 'details': []})
