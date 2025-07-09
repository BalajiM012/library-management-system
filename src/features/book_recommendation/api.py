from flask import Blueprint, jsonify, session, render_template
from src.app_factory import db
from src.models import Book, BorrowRecord
from sqlalchemy.sql import func
from collections import Counter

book_recommendation_bp = Blueprint('book_recommendation', __name__, url_prefix='/api/book_recommendation', template_folder='templates')

def get_user_borrowed_books(user_id):
    borrowed = BorrowRecord.query.filter_by(user_id=user_id).all()
    return [b.book_id for b in borrowed]

def get_books_by_author(author, exclude_ids=None):
    query = Book.query.filter(Book.author == author)
    if exclude_ids:
        query = query.filter(~Book.id.in_(exclude_ids))
    return query.all()

def collaborative_filtering_recommendations(user_id, top_n=5):
    # Find other users who borrowed the same books
    user_books = set(get_user_borrowed_books(user_id))
    if not user_books:
        return []
    other_borrows = BorrowRecord.query.filter(BorrowRecord.book_id.in_(user_books), BorrowRecord.user_id != user_id).all()
    user_similarity = Counter()
    for borrow in other_borrows:
        user_similarity[borrow.user_id] += 1
    # Get top similar users
    similar_users = [user for user, count in user_similarity.most_common()]
    recommended_books = set()
    for similar_user in similar_users:
        books = get_user_borrowed_books(similar_user)
        for book_id in books:
            if book_id not in user_books:
                recommended_books.add(book_id)
            if len(recommended_books) >= top_n:
                break
        if len(recommended_books) >= top_n:
            break
    return Book.query.filter(Book.id.in_(recommended_books)).all()

def content_based_recommendations(user_id, top_n=5):
    user_books = get_user_borrowed_books(user_id)
    if not user_books:
        return []
    # Get authors of books user borrowed
    authors = db.session.query(Book.author).filter(Book.id.in_(user_books)).distinct().all()
    authors = [a[0] for a in authors]
    recommended_books = []
    for author in authors:
        books = get_books_by_author(author, exclude_ids=user_books)
        recommended_books.extend(books)
        if len(recommended_books) >= top_n:
            break
    return recommended_books[:top_n]

def hybrid_recommendations(user_id, top_n=5):
    content_recs = content_based_recommendations(user_id, top_n)
    collaborative_recs = collaborative_filtering_recommendations(user_id, top_n)
    combined = {book.id: book for book in content_recs}
    for book in collaborative_recs:
        combined[book.id] = book
    return list(combined.values())[:top_n]

@book_recommendation_bp.route('/collaborative', methods=['GET'])
def collaborative_filtering():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'recommendations': []})
    books = collaborative_filtering_recommendations(user_id)
    recommendations = [{"title": b.title, "author": b.author} for b in books]
    return jsonify({'recommendations': recommendations})

@book_recommendation_bp.route('/content_based', methods=['GET'])
def content_based_filtering():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'recommendations': []})
    books = content_based_recommendations(user_id)
    recommendations = [{"title": b.title, "author": b.author} for b in books]
    return jsonify({'recommendations': recommendations})

@book_recommendation_bp.route('/hybrid', methods=['GET'])
def hybrid_filtering():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'recommendations': []})
    books = hybrid_recommendations(user_id)
    recommendations = [{"title": b.title, "author": b.author} for b in books]
    return jsonify({'recommendations': recommendations})

@book_recommendation_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('recommendation.html')
