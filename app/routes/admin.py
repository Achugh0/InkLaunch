"""Admin routes."""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash, send_file, abort
from app.models import User, Book, Review, CompetitionPeriod, Nomination
from app.models_audit import AuditLog
from app.security import require_admin as require_admin_decorator, validate_object_id
from app import mongo, bcrypt
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
import csv
import io
from werkzeug.utils import secure_filename

bp = Blueprint('admin', __name__, url_prefix='/admin')


def require_admin():
    """Check if user is admin."""
    user_id = session.get('user_id')
    user_role = session.get('user_role')
    
    if not user_id or user_role != 'admin':
        flash('Admin access required', 'error')
        abort(403)
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
    
    if not validate_object_id(user_id):
        flash('Invalid user ID', 'error')
        return redirect(url_for('admin.list_users'))
    
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
    
    if not validate_object_id(user_id):
        if request.is_json:
            return jsonify({'error': 'Invalid user ID'}), 400
        flash('Invalid user ID', 'error')
        return redirect(url_for('admin.list_users'))
    
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
    
    if not validate_object_id(user_id):
        if request.is_json:
            return jsonify({'error': 'Invalid user ID'}), 400
        flash('Invalid user ID', 'error')
        return redirect(url_for('admin.list_users'))
    
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
    
    if not validate_object_id(book_id):
        if request.is_json:
            return jsonify({'error': 'Invalid book ID'}), 400
        flash('Invalid book ID', 'error')
        return redirect(url_for('admin.list_books'))
    
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


@bp.route('/users/bulk-import', methods=['GET', 'POST'])
def bulk_import_users():
    """Bulk import users from CSV."""
    if not require_admin():
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # Check if file was uploaded
        if 'csv_file' not in request.files:
            flash('No file uploaded', 'error')
            return redirect(request.url)
        
        file = request.files['csv_file']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if not file.filename.endswith('.csv'):
            flash('Please upload a CSV file', 'error')
            return redirect(request.url)
        
        try:
            # Read CSV file
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.DictReader(stream)
            
            success_count = 0
            error_count = 0
            errors = []
            
            for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 to account for header
                try:
                    # Validate required fields
                    required_fields = ['user_id', 'email', 'Full_name', 'password']
                    missing_fields = [field for field in required_fields if not row.get(field)]
                    
                    if missing_fields:
                        errors.append(f"Row {row_num}: Missing required fields: {', '.join(missing_fields)}")
                        error_count += 1
                        continue
                    
                    # Check if user already exists
                    existing_user = User.find_by_username(row['user_id'])
                    if existing_user:
                        errors.append(f"Row {row_num}: Username '{row['user_id']}' already exists")
                        error_count += 1
                        continue
                    
                    existing_email = User.find_by_email(row['email'])
                    if existing_email:
                        errors.append(f"Row {row_num}: Email '{row['email']}' already exists")
                        error_count += 1
                        continue
                    
                    # Create user
                    user_data = {
                        'username': row['user_id'],
                        'email': row['email'],
                        'full_name': row['Full_name'],
                        'password_hash': bcrypt.generate_password_hash(row['password']).decode('utf-8'),
                        'role': row.get('role', 'user').lower(),
                        'status': row.get('status', 'active').lower(),
                        'bio': row.get('BIO', ''),
                        'created_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow(),
                        'profile_image': None,
                        'social_links': {},
                        'preferences': {},
                        'badges': []
                    }
                    
                    mongo.db.users.insert_one(user_data)
                    success_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
                    error_count += 1
            
            # Show results
            if success_count > 0:
                flash(f'Successfully imported {success_count} users', 'success')
            
            if error_count > 0:
                flash(f'Failed to import {error_count} users', 'warning')
                for error in errors[:10]:  # Show first 10 errors
                    flash(error, 'error')
                if len(errors) > 10:
                    flash(f'... and {len(errors) - 10} more errors', 'error')
            
            return redirect(url_for('admin.list_users'))
            
        except Exception as e:
            flash(f'Error processing CSV file: {str(e)}', 'error')
            return redirect(request.url)
    
    # GET request - show upload form
    return render_template('admin/bulk_import_users.html')


@bp.route('/users/download-sample-csv')
def download_sample_csv():
    """Download sample CSV file for bulk import."""
    if not require_admin():
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    try:
        # Path to sample CSV file
        import os
        sample_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'sample_users.csv')
        
        return send_file(
            sample_file,
            mimetype='text/csv',
            as_attachment=True,
            download_name='sample_users.csv'
        )
    except Exception as e:
        flash(f'Error downloading sample file: {str(e)}', 'error')
        return redirect(url_for('admin.list_users'))
