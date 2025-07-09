from flask import Blueprint, jsonify
from src.models import BorrowRecord  # Assuming this model exists and has fine info

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/admin', methods=['GET'])
def get_fines():
    # Query borrow records with fine info
    records = BorrowRecord.query.all()
    fines = []
    for r in records:
        fines.append({
            'borrow_id': r.id,
            'user_id': r.user_id,
            'book_id': r.book_id,
            'due_date': r.due_date.isoformat() if r.due_date else None,
            'return_date': r.return_date.isoformat() if r.return_date else None,
            'fine': r.fine
        })
    return jsonify({'fines': fines})
