from flask import Blueprint, request, jsonify

book_management_bp = Blueprint('book_management', __name__, url_prefix='/api/book_management')

@book_management_bp.route('/books', methods=['GET'])
def get_books():
    from src.models import Book
    books = Book.query.all()
    return jsonify([{'id': b.id, 'title': b.title, 'author': b.author, 'isbn': b.isbn, 'copies': b.copies} for b in books])

@book_management_bp.route('/books', methods=['POST'])
def add_book():
    from src.app_factory import db
    from src.models import Book
    data = request.json
    book = Book(title=data['title'], author=data['author'], isbn=data['isbn'], copies=data['copies'])
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book added'})

@book_management_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    from src.app_factory import db
    from src.models import Book
    data = request.json
    book = Book.query.get_or_404(book_id)
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.isbn = data.get('isbn', book.isbn)
    book.copies = data.get('copies', book.copies)
    db.session.commit()
    return jsonify({'message': 'Book updated'})

@book_management_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    from src.app_factory import db
    from src.models import Book
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'})
