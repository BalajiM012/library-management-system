from flask import Blueprint, jsonify
from datetime import datetime

automated_fine_calculation_bp = Blueprint('automated_fine_calculation', __name__, url_prefix='/api/automated_fine_calculation')

def calculate_fines_logic():
    from src.app_factory import db
    from src.models import BorrowRecord
    records = BorrowRecord.query.filter(BorrowRecord.return_date == None).all()
    for record in records:
        due_date = record.due_date
        now = datetime.utcnow()
        if now > due_date:
            days_overdue = (now - due_date).days
            record.fine = days_overdue * 1.0
        else:
            record.fine = 0.0
    db.session.commit()

@automated_fine_calculation_bp.route('/calculate_fines', methods=['POST'])
def calculate_fines():
    calculate_fines_logic()
    return jsonify({'message': 'Fines calculated and updated successfully'})

@automated_fine_calculation_bp.route('/fines', methods=['GET'])
def get_fines():
    from src.models import BorrowRecord
    records = BorrowRecord.query.all()
    fines_list = []
    for record in records:
        fines_list.append({
            'borrow_id': record.id,
            'user_id': record.user_id,
            'book_id': record.book_id,
            'fine': record.fine,
            'due_date': record.due_date.isoformat() if record.due_date else None,
            'return_date': record.return_date.isoformat() if record.return_date else None
        })
    return jsonify(fines_list)
