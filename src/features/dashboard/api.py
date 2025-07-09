from flask import Blueprint, jsonify, session, render_template

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

from src.models import BorrowRecord
from flask import jsonify

@dashboard_bp.route('/admin', methods=['GET'])
def admin_dashboard():
    # Fetch fines and due date fine tracking data for dashboard
    records = BorrowRecord.query.all()
    fines_data = []
    for record in records:
        fines_data.append({
            'borrow_id': record.id,
            'user_id': record.user_id,
            'book_id': record.book_id,
            'fine': record.fine,
            'due_date': record.due_date.isoformat() if record.due_date else None,
            'return_date': record.return_date.isoformat() if record.return_date else None
        })
    return jsonify({'message': 'Admin dashboard data', 'fines': fines_data})

@dashboard_bp.route('/student', methods=['GET'])
def student_dashboard():
    # Return student dashboard data
    return jsonify({'message': 'Student dashboard data'})

@dashboard_bp.route('/admin/dashboard', methods=['GET'])
def admin_dashboard_page():
    return render_template('dashboard.html')
