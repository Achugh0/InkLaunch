"""Book routes."""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Book, User, Review
from app.services.s3_service import s3_service
from werkzeug.utils import secure_filename
from bson import ObjectId
import os
from datetime import datetime

bp = Blueprint('books', __name__, url_prefix='/books')


def allowed_file(filename):
    """Check if file extension is allowed."""
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'jpg', 'jpeg', 'png', 'gif'})
    return ext in allowed


@bp.route('/', methods=['GET'])
def list_books():
    """List and search all books."""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ITEMS_PER_PAGE']
    query = request.args.get('q', '').strip()
    genre = request.args.get('genre', '')
    status = request.args.get('status', 'active')
    sort_by = request.args.get('sort', 'recent')
    
    # Build filters
    filters = {}
    if status:
        filters['status'] = status
    if genre:
        filters['genre'] = genre
    
    # Set sort order
    sort_mapping = {
        'recent': [('created_at', -1)],
        'title': [('title', 1)],
        'views': [('views_count', -1)],
        'wins': [('competition_wins', -1)]
    }
    sort_order = sort_mapping.get(sort_by, [('created_at', -1)])
    
    skip = (page - 1) * per_page
    books = Book.search(query=query, filters=filters, skip=skip, limit=per_page, sort=sort_order)
    total = Book.count_search(query=query, filters=filters)
    
    # Enrich with author info and ratings
    for book in books:
        author = User.find_by_id(str(book['user_id']))
        book['author'] = author
        book['rating_info'] = Review.get_average_rating(str(book['_id']))
    
    total_pages = (total + per_page - 1) // per_page
    
    # Get available genres for filter
    from app import mongo
    all_genres = mongo.db[Book.collection].distinct('genre')
    
    if request.is_json:
        return jsonify({
            'books': [{
                'id': str(b['_id']),
                'title': b['title'],
                'author': b['author']['full_name'] if b['author'] else 'Unknown',
                'author_id': str(b['user_id']),
                'genre': b.get('genre'),
                'cover_image_url': b.get('cover_image_url'),
                'rating': b['rating_info']['average'],
                'review_count': b['rating_info']['count']
            } for b in books],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages
        }), 200
    
    return render_template('books/list.html', 
                         books=books, 
                         page=page, 
                         total=total, 
                         per_page=per_page,
                         total_pages=total_pages,
                         query=query,
                         genre=genre,
                         status=status,
                         sort_by=sort_by,
                         all_genres=all_genres)


@bp.route('/<book_id>', methods=['GET'])
def get_book(book_id):
    """Get book details."""
    book = Book.find_by_id(book_id)
    
    if not book:
        if request.is_json:
            return jsonify({'error': 'Book not found'}), 404
        flash('Book not found', 'error')
        return redirect(url_for('books.list_books'))
    
    # Increment views
    Book.increment_views(book_id)
    
    # Get author info
    author = User.find_by_id(str(book['user_id']))
    book['author'] = author
    
    # Get reviews
    reviews = Review.find_by_book(book_id)
    for review in reviews:
        reviewer = User.find_by_id(str(review['reviewer_id']))
        review['reviewer'] = reviewer
    
    # Get rating info
    rating_info = Review.get_average_rating(book_id)
    
    if request.is_json:
        return jsonify({
            'id': str(book['_id']),
            'title': book['title'],
            'subtitle': book.get('subtitle'),
            'description': book.get('description'),
            'author': {
                'id': str(author['_id']),
                'name': author['full_name'],
                'bio': author.get('bio')
            } if author else None,
            'genre': book.get('genre'),
            'isbn': book.get('isbn'),
            'cover_image_url': book.get('cover_image_url'),
            'amazon_link': book.get('amazon_link'),
            'goodreads_link': book.get('goodreads_link'),
            'rating': rating_info,
            'reviews': len(reviews)
        }), 200
    
    return render_template('books/detail.html', book=book, reviews=reviews, rating_info=rating_info)


@bp.route('/create', methods=['GET', 'POST'])
def create_book():
    """Create a new book."""
    user_id = session.get('user_id')
    
    if not user_id:
        if request.is_json:
            return jsonify({'error': 'Authentication required'}), 401
        flash('Please log in to create a book', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'GET':
        genres = ['Fiction', 'Non-Fiction', 'IT & Technology', 'Corporate Satire', 
                  'Psychological Fiction', 'Mystery', 'Romance', 'Science Fiction', 
                  'Fantasy', 'Biography', 'Self-Help', 'Business']
        return render_template('books/create.html', genres=genres)
    
    # Handle file upload or URL
    cover_image_url = ''
    
    # Check if user provided a URL instead
    if 'cover_image_url' in request.form and request.form['cover_image_url'].strip():
        cover_image_url = request.form['cover_image_url'].strip()
    # Otherwise check for file upload
    elif 'cover_image' in request.files:
        file = request.files['cover_image']
        if file and file.filename and allowed_file(file.filename):
            try:
                # Try S3 upload first
                if s3_service.is_s3_configured():
                    cover_image_url = s3_service.upload_file(file, folder='book-covers')
                    if not cover_image_url:
                        raise Exception("S3 upload returned None")
                else:
                    # Fallback to local storage (for development)
                    filename = secure_filename(file.filename)
                    filename = f"{datetime.utcnow().timestamp()}_{filename}"
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
                    file.save(filepath)
                    cover_image_url = f"/uploads/{filename}"
            except Exception as e:
                # Log error but continue - cover image is optional
                current_app.logger.error(f"Failed to save cover image: {str(e)}")
                flash(f'Warning: Cover image upload failed: {str(e)}', 'warning')
    
    data = request.form if not request.is_json else request.get_json()
    
    # Validation
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    genre = data.get('genre', '').strip()
    
    if not title or not description or not genre:
        if request.is_json:
            return jsonify({'error': 'Title, description, and genre are required'}), 400
        flash('Title, description, and genre are required', 'error')
        return redirect(url_for('books.create_book'))
    
    if len(description) < 100:
        if request.is_json:
            return jsonify({'error': 'Description must be at least 100 characters'}), 400
        flash('Description must be at least 100 characters', 'error')
        return redirect(url_for('books.create_book'))
    
    # Create book
    book_data = {
        'title': title,
        'subtitle': data.get('subtitle', '').strip(),
        'description': description,
        'genre': genre,
        'isbn': data.get('isbn', '').strip(),
        'language': data.get('language', 'English'),
        'page_count': int(data.get('page_count', 0)) if data.get('page_count') else 0,
        'price': float(data.get('price', 0)) if data.get('price') else 0.0,
        'amazon_link': data.get('amazon_link', '').strip(),
        'goodreads_link': data.get('goodreads_link', '').strip(),
        'cover_image_url': cover_image_url,
        'publication_date': datetime.utcnow(),
        'status': 'active'
    }
    
    book_id = Book.create(user_id, book_data)
    
    if request.is_json:
        return jsonify({
            'message': 'Book created successfully',
            'book_id': str(book_id)
        }), 201
    
    flash('Book created successfully!', 'success')
    return redirect(url_for('books.get_book', book_id=str(book_id)))


@bp.route('/<book_id>/edit', methods=['GET', 'POST'])
def edit_book(book_id):
    """Edit a book."""
    user_id = session.get('user_id')
    user_role = session.get('user_role')
    
    if not user_id:
        if request.is_json:
            return jsonify({'error': 'Authentication required'}), 401
        flash('Please log in', 'error')
        return redirect(url_for('auth.login'))
    
    book = Book.find_by_id(book_id)
    
    if not book:
        if request.is_json:
            return jsonify({'error': 'Book not found'}), 404
        flash('Book not found', 'error')
        return redirect(url_for('books.list_books'))
    
    # Check permissions
    if str(book['user_id']) != user_id and user_role != 'admin':
        if request.is_json:
            return jsonify({'error': 'Permission denied'}), 403
        flash('Permission denied', 'error')
        return redirect(url_for('books.get_book', book_id=book_id))
    
    if request.method == 'GET':
        genres = ['Fiction', 'Non-Fiction', 'IT & Technology', 'Corporate Satire', 
                  'Psychological Fiction', 'Mystery', 'Romance', 'Science Fiction', 
                  'Fantasy', 'Biography', 'Self-Help', 'Business']
        return render_template('books/edit.html', book=book, genres=genres)
    
    # Handle updates
    data = request.form if not request.is_json else request.get_json()
    
    update_data = {}
    if 'title' in data:
        update_data['title'] = data['title'].strip()
    if 'subtitle' in data:
        update_data['subtitle'] = data['subtitle'].strip()
    if 'description' in data:
        update_data['description'] = data['description'].strip()
    if 'genre' in data:
        update_data['genre'] = data['genre'].strip()
    if 'isbn' in data:
        update_data['isbn'] = data['isbn'].strip()
    if 'page_count' in data:
        update_data['page_count'] = int(data['page_count']) if data['page_count'] else 0
    if 'price' in data:
        update_data['price'] = float(data['price']) if data['price'] else 0.0
    if 'amazon_link' in data:
        update_data['amazon_link'] = data['amazon_link'].strip()
    if 'goodreads_link' in data:
        update_data['goodreads_link'] = data['goodreads_link'].strip()
    
    # Handle new cover image (URL or file upload)
    if 'cover_image_url' in request.form and request.form['cover_image_url'].strip():
        # User provided a URL
        update_data['cover_image_url'] = request.form['cover_image_url'].strip()
    elif 'cover_image' in request.files:
        file = request.files['cover_image']
        if file and file.filename and allowed_file(file.filename):
            try:
                # Try S3 upload first
                if s3_service.is_s3_configured():
                    cover_image_url = s3_service.upload_file(file, folder='book-covers')
                    if cover_image_url:
                        update_data['cover_image_url'] = cover_image_url
                        # Optionally delete old image from S3 if it exists
                        old_url = book.get('cover_image_url')
                        if old_url and 's3.amazonaws.com' in old_url:
                            s3_service.delete_file(old_url)
                else:
                    # Fallback to local storage (for development)
                    filename = secure_filename(file.filename)
                    filename = f"{datetime.utcnow().timestamp()}_{filename}"
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    update_data['cover_image_url'] = f"/uploads/{filename}"
            except Exception as e:
                current_app.logger.error(f"Failed to save cover image: {str(e)}")
    
    Book.update(book_id, update_data)
    
    if request.is_json:
        return jsonify({'message': 'Book updated successfully'}), 200
    
    flash('Book updated successfully!', 'success')
    return redirect(url_for('books.get_book', book_id=book_id))


@bp.route('/<book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Delete a book."""
    user_id = session.get('user_id')
    user_role = session.get('user_role')
    
    if not user_id:
        if request.is_json:
            return jsonify({'error': 'Authentication required'}), 401
        flash('Please log in', 'error')
        return redirect(url_for('auth.login'))
    
    book = Book.find_by_id(book_id)
    
    if not book:
        if request.is_json:
            return jsonify({'error': 'Book not found'}), 404
        flash('Book not found', 'error')
        return redirect(url_for('books.list_books'))
    
    # Check permissions
    if str(book['user_id']) != user_id and user_role != 'admin':
        if request.is_json:
            return jsonify({'error': 'Permission denied'}), 403
        flash('Permission denied', 'error')
        return redirect(url_for('books.get_book', book_id=book_id))
    
    Book.delete(book_id)
    
    if request.is_json:
        return jsonify({'message': 'Book deleted successfully'}), 200
    
    flash('Book deleted successfully', 'success')
    return redirect(url_for('main.dashboard'))
