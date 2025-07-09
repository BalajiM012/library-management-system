from flask import Blueprint, jsonify, render_template
from src.app_factory import db
from src.models import BorrowRecord, Book
from sqlalchemy import func

demand_forecast_bp = Blueprint('demand_forecast', __name__, url_prefix='/demand_forecast', template_folder='templates')

from flask import current_app

@demand_forecast_bp.route('/forecast', methods=['GET'])
def forecast():
    # Simple demand forecasting: count borrow records per book
    with current_app.app_context():
        borrow_counts = db.session.query(
            BorrowRecord.book_id,
            func.count(BorrowRecord.id).label('borrow_count')
        ).group_by(BorrowRecord.book_id).order_by(func.count(BorrowRecord.id).desc()).all()

        books = []
        for book_id, count in borrow_counts:
            book = Book.query.get(book_id)
            if book:
                books.append({
                    'title': book.title,
                    'author': book.author,
                    'borrow_count': count
                })

        forecast_data = {
            'books': books,
            'message': 'Demand forecast based on borrow history'
        }
        return jsonify(forecast_data)

@demand_forecast_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('demand_forecast.html')
