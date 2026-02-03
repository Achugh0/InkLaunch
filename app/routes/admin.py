"""Admin routes."""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from app.models import User, Book, Review, CompetitionPeriod, Nomination
from app import mongo, bcrypt
from bson import ObjectId
from datetime import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')


def require_admin():
    """Check if user is admin."""
    user_id = session.get('user_id')
    user_role = session.get('user_role')
    
    if not user_id or user_role != 'admin':
        return False
    return True


@bp.route('/dashboard')
def dashboard():
    """Admin dashboard."""
    if not require_admin():
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    # Get statistics
    total_users = mongo.db.users.count_documents({})
    total_books = mongo.db.books.count_documents({})
    total_reviews = mongo.db.reviews.count_documents({})
    pending_reviews = mongo.db.reviews.count_documents({'status': 'pending'})
    
    stats = {
        'total_users': total_users,
        'total_books': total_books,
        'total_reviews': total_reviews,
        'pending_reviews': pending_reviews
    }
    
    if request.is_json:
        return jsonify(stats), 200
    
    return render_template('admin/dashboard.html', stats=stats)


@bp.route('/users')
def list_users():
    """List all users."""
    if not require_admin():
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    users = list(mongo.db.users.find().sort('created_at', -1))
    
    return render_template('admin/users.html', users=users)


@bp.route('/reviews/pending')
def pending_reviews():
    """List pending reviews."""
    if not require_admin():
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    reviews = list(mongo.db.reviews.find({'status': 'pending'}).sort('created_at', -1))
    
    # Enrich with book and reviewer info
    for review in reviews:
        book = Book.find_by_id(str(review['book_id']))
        reviewer = User.find_by_id(str(review['reviewer_id']))
        review['book'] = book
        review['reviewer'] = reviewer
    
    return render_template('admin/pending_reviews.html', reviews=reviews)


@bp.route('/users/<user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit a user."""
    if not require_admin():
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    user = User.find_by_id(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin.list_users'))
    
    if request.method == 'POST':
        update_data = {
            'full_name': request.form.get('full_name'),
            'email': request.form.get('email').lower(),
            'role': request.form.get('role'),
            'is_active': request.form.get('is_active') == 'true',
            'bio': request.form.get('bio', ''),
            'updated_at': datetime.utcnow()
        }
        
        User.update(user_id, update_data)
        flash('User updated successfully', 'success')
        return redirect(url_for('admin.list_users'))
    
    return render_template('admin/edit_user.html', user=user)


@bp.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user."""
    if not require_admin():
        if request.is_json:
            return jsonify({'error': 'Admin access required'}), 403
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    # Don't allow deleting yourself
    if user_id == session.get('user_id'):
        if request.is_json:
            return jsonify({'error': 'Cannot delete your own account'}), 400
        flash('Cannot delete your own account', 'error')
        return redirect(url_for('admin.list_users'))
    
    user = User.find_by_id(user_id)
    if not user:
        if request.is_json:
            return jsonify({'error': 'User not found'}), 404
        flash('User not found', 'error')
        return redirect(url_for('admin.list_users'))
    
    # Delete user's books
    mongo.db.books.delete_many({'user_id': ObjectId(user_id)})
    
    # Delete user's reviews
    mongo.db.reviews.delete_many({'reviewer_id': ObjectId(user_id)})
    
    # Delete the user
    mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    
    if request.is_json:
        return jsonify({'message': 'User deleted successfully'}), 200
    
    flash('User deleted successfully', 'success')
    return redirect(url_for('admin.list_users'))


@bp.route('/users/<user_id>/reset-password', methods=['POST'])
def reset_user_password(user_id):
    """Reset a user's password."""
    if not require_admin():
        if request.is_json:
            return jsonify({'error': 'Admin access required'}), 403
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    user = User.find_by_id(user_id)
    if not user:
        if request.is_json:
            return jsonify({'error': 'User not found'}), 404
        flash('User not found', 'error')
        return redirect(url_for('admin.list_users'))
    
    data = request.get_json() if request.is_json else request.form
    new_password = data.get('new_password')
    
    if not new_password or len(new_password) < 8:
        if request.is_json:
            return jsonify({'error': 'Password must be at least 8 characters'}), 400
        flash('Password must be at least 8 characters', 'error')
        return redirect(url_for('admin.list_users'))
    
    password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    User.update(user_id, {'password_hash': password_hash})
    
    if request.is_json:
        return jsonify({'message': 'Password reset successfully'}), 200
    
    flash('Password reset successfully', 'success')
    return redirect(url_for('admin.list_users'))


@bp.route('/users/create', methods=['GET', 'POST'])
def create_user():
    """Create a new user."""
    if not require_admin():
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        role = request.form.get('role', 'user')
        
        # Check if user exists
        if User.find_by_email(email):
            flash('User with this email already exists', 'error')
            return render_template('admin/create_user.html')
        
        # Create user
        User.create(email, password, full_name, role=role)
        flash('User created successfully', 'success')
        return redirect(url_for('admin.list_users'))
    
    return render_template('admin/create_user.html')


@bp.route('/books')
def list_books():
    """List all books with management options."""
    if not require_admin():
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    books = list(mongo.db.books.find().sort('created_at', -1))
    
    # Enrich with author info
    for book in books:
        author = User.find_by_id(str(book['user_id']))
        book['author'] = author
    
    return render_template('admin/books.html', books=books)


@bp.route('/books/<book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Delete a book."""
    if not require_admin():
        if request.is_json:
            return jsonify({'error': 'Admin access required'}), 403
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    book = Book.find_by_id(book_id)
    if not book:
        if request.is_json:
            return jsonify({'error': 'Book not found'}), 404
        flash('Book not found', 'error')
        return redirect(url_for('admin.list_books'))
    
    # Delete book's reviews
    mongo.db.reviews.delete_many({'book_id': ObjectId(book_id)})
    
    # Delete the book
    mongo.db.books.delete_one({'_id': ObjectId(book_id)})
    
    if request.is_json:
        return jsonify({'message': 'Book deleted successfully'}), 200
    
    flash('Book deleted successfully', 'success')
    return redirect(url_for('admin.list_books'))


@bp.route('/system/stats')
def system_stats():
    """System statistics and maintenance."""
    if not require_admin():
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    # Database stats
    db_stats = mongo.db.command('dbStats')
    
    # Collection stats
    collections_stats = {
        'users': mongo.db.users.count_documents({}),
        'books': mongo.db.books.count_documents({}),
        'reviews': mongo.db.reviews.count_documents({}),
        'competitions': mongo.db.competition_periods.count_documents({}),
        'nominations': mongo.db.nominations.count_documents({})
    }
    
    # Recent activity
    recent_users = list(mongo.db.users.find().sort('created_at', -1).limit(5))
    recent_books = list(mongo.db.books.find().sort('created_at', -1).limit(5))
    recent_reviews = list(mongo.db.reviews.find().sort('created_at', -1).limit(5))
    
    # Enrich recent books with author info
    for book in recent_books:
        author = User.find_by_id(str(book['user_id']))
        book['author'] = author
    
    # Enrich recent reviews with reviewer and book info
    for review in recent_reviews:
        reviewer = User.find_by_id(str(review['reviewer_id']))
        book = Book.find_by_id(str(review['book_id']))
        review['reviewer'] = reviewer
        review['book'] = book
    
    stats = {
        'db_size': db_stats.get('dataSize', 0) / (1024 * 1024),  # Convert to MB
        'collections': collections_stats,
        'recent_users': recent_users,
        'recent_books': recent_books,
        'recent_reviews': recent_reviews
    }
    
    return render_template('admin/system_stats.html', stats=stats)

