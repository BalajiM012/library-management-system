from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app_factory import db
from src.models import BorrowRecord, Book, User

from flask import Flask
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app_factory import db
from src.models import BorrowRecord, Book, User

def create_sample_borrow_records(app: Flask):
    with app.app_context():
        # Create sample users if not exist
        users = User.query.limit(5).all()
        if len(users) < 5:
            for i in range(5 - len(users)):
                user = User(fullname=f"User{i+1}", email=f"user{i+1}@example.com", username=f"user{i+1}", password="password")
                db.session.add(user)
            db.session.commit()
            users = User.query.limit(5).all()

        # Create sample books if not exist
        books = Book.query.limit(5).all()
        if len(books) < 5:
            for i in range(5 - len(books)):
                book = Book(title=f"Book Title {i+1}", author=f"Author {i+1}", isbn=f"ISBN{i+1}", copies=5)
                db.session.add(book)
            db.session.commit()
            books = Book.query.limit(5).all()

        # Create 30 borrow records with fines
        for i in range(30):
            user = users[i % len(users)]
            book = books[i % len(books)]
            # Set custom borrow_date before July 2025
            borrow_date = datetime(2025, 6, 1) - timedelta(days=i)
            due_date = borrow_date + timedelta(days=14)
            return_date = due_date + timedelta(days=i % 5)  # Some returned late
            days_overdue = (return_date - due_date).days if return_date > due_date else 0
            fine = days_overdue * 1.0

            borrow_record = BorrowRecord(
                user_id=user.id,
                book_id=book.id,
                borrow_date=borrow_date,
                due_date=due_date,
                return_date=return_date,
                fine=fine
            )
            db.session.add(borrow_record)

        db.session.commit()
        print("Created 30 sample borrow records with fines.")

if __name__ == "__main__":
    from src.app_factory import create_app
    app = create_app()
    create_sample_borrow_records(app)
