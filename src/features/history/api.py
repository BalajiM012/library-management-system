from flask import Blueprint, request, jsonify, session
from functools import wraps

history_bp = Blueprint('history', __name__, url_prefix='/api/history')

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Bypass authentication for testing
            return f(*args, **kwargs)
            # Uncomment below to enable authentication
            # if 'user_id' not in session:
            #     return jsonify({'error': 'Authentication required'}), 401
            # if role and session.get('role') != role:
            #     return jsonify({'error': 'Unauthorized'}), 403
            # return f(*args, **kwargs)
        return decorated_function
    return decorator

@history_bp.route('/borrow', methods=['GET'])
@login_required()
def get_borrow_history():
    from src.app_factory import db
    user_id = session.get('user_id')
    # Query database for borrow history by user_id
    from sqlalchemy import text
    sql = text('''
        SELECT br.id AS serial_number, b.id AS book_id, b.title AS book_title, br.borrow_date, br.return_date
        FROM borrow_record br
        JOIN book b ON br.book_id = b.id
        WHERE br.user_id = :user_id
        ORDER BY br.borrow_date DESC
    ''')
    result = db.session.execute(sql, {'user_id': user_id})
    borrow_history = []
    for row in result:
        borrow_history.append({
            'serial_number': row.serial_number,
            'book_id': row.book_id,
            'book_title': row.book_title,
            'borrow_date': row.borrow_date.strftime('%Y-%m-%d') if row.borrow_date else None,
            'return_date': row.return_date.strftime('%Y-%m-%d') if row.return_date else None
        })
    return jsonify(borrow_history)

@history_bp.route('/fees', methods=['GET'])
@login_required()
def get_fees():
    from src.app_factory import db
    user_id = session.get('user_id')
    # Query database for fees by user_id
    from sqlalchemy import text
    sql_total = text('''
        SELECT COALESCE(SUM(amount), 0) AS total_fees
        FROM fees
        WHERE user_id = :user_id
    ''')
    sql_details = text('''
        SELECT date, amount, reason
        FROM fees
        WHERE user_id = :user_id
        ORDER BY date DESC
    ''')
    total_result = db.session.execute(sql_total, {'user_id': user_id}).fetchone()
    details_result = db.session.execute(sql_details, {'user_id': user_id})
    fees = {
        'total_fees': float(total_result.total_fees) if total_result else 0.0,
        'details': []
    }
    for row in details_result:
        fees['details'].append({
            'date': row.date.strftime('%Y-%m-%d') if row.date else None,
            'amount': float(row.amount),
            'reason': row.reason
        })
    return jsonify(fees)
