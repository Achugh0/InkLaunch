"""Review routes."""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session, current_app
from app.models import Review, Book, User
from app import mongo
from bson import ObjectId

bp = Blueprint('reviews', __name__, url_prefix='/reviews')


@bp.route('/', methods=['GET'])
def list_reviews():
    """List reviews (for moderation)."""
    user_role = session.get('user_role')
    
    if user_role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    status = request.args.get('status', 'pending')
    
    reviews = list(mongo.db.reviews.find({'status': status}).sort('created_at', -1))
    
    # Enrich with book and reviewer info
    for review in reviews:
        book = Book.find_by_id(str(review['book_id']))
        reviewer = User.find_by_id(str(review['reviewer_id']))
        review['book'] = book
        review['reviewer'] = reviewer
    
    return render_template('reviews/list.html', reviews=reviews, status=status)


@bp.route('/create', methods=['POST'])
def create_review():
    """Create a review."""
    user_id = session.get('user_id')
    
    if not user_id:
        if request.is_json:
            return jsonify({'error': 'Authentication required'}), 401
        flash('Please log in to write a review', 'error')
        return redirect(url_for('auth.login'))
    
    data = request.get_json() if request.is_json else request.form
    
    book_id = data.get('book_id')
    rating = data.get('rating', type=int)
    review_text = data.get('review_text', '').strip()
    
    # Validation
    if not book_id or not rating or not review_text:
        if request.is_json:
            return jsonify({'error': 'Book ID, rating, and review text are required'}), 400
        flash('All fields are required', 'error')
        return redirect(url_for('books.get_book', book_id=book_id))
    
    if rating < 1 or rating > 5:
        if request.is_json:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        flash('Rating must be between 1 and 5', 'error')
        return redirect(url_for('books.get_book', book_id=book_id))
    
    if len(review_text) < current_app.config['REVIEW_MIN_LENGTH']:
        if request.is_json:
            return jsonify({'error': f'Review must be at least {current_app.config["REVIEW_MIN_LENGTH"]} characters'}), 400
        flash(f'Review must be at least {current_app.config["REVIEW_MIN_LENGTH"]} characters', 'error')
        return redirect(url_for('books.get_book', book_id=book_id))
    
    # Check if book exists
    book = Book.find_by_id(book_id)
    if not book:
        if request.is_json:
            return jsonify({'error': 'Book not found'}), 404
        flash('Book not found', 'error')
        return redirect(url_for('books.list_books'))
    
    # Check if user is trying to review their own book
    if str(book['user_id']) == user_id:
        if request.is_json:
            return jsonify({'error': 'Cannot review your own book'}), 400
        flash('You cannot review your own book', 'error')
        return redirect(url_for('books.get_book', book_id=book_id))
    
    # Create review
    review_id = Review.create(book_id, user_id, rating, review_text)
    
    if request.is_json:
        return jsonify({
            'message': 'Review submitted successfully. It will be visible after admin approval.',
            'review_id': str(review_id)
        }), 201
    
    flash('Review submitted successfully! It will be visible after admin approval.', 'success')
    return redirect(url_for('books.get_book', book_id=book_id))


@bp.route('/<review_id>/approve', methods=['POST'])
def approve_review(review_id):
    """Approve a review (admin only)."""
    user_role = session.get('user_role')
    
    if user_role != 'admin':
        if request.is_json:
            return jsonify({'error': 'Admin access required'}), 403
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    review = Review.find_by_id(review_id)
    if not review:
        if request.is_json:
            return jsonify({'error': 'Review not found'}), 404
        flash('Review not found', 'error')
        return redirect(url_for('reviews.list_reviews'))
    
    Review.update_status(review_id, 'approved')
    
    if request.is_json:
        return jsonify({'message': 'Review approved successfully'}), 200
    
    flash('Review approved successfully', 'success')
    return redirect(url_for('reviews.list_reviews'))


@bp.route('/<review_id>/reject', methods=['POST'])
def reject_review(review_id):
    """Reject a review (admin only)."""
    user_role = session.get('user_role')
    
    if user_role != 'admin':
        if request.is_json:
            return jsonify({'error': 'Admin access required'}), 403
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    review = Review.find_by_id(review_id)
    if not review:
        if request.is_json:
            return jsonify({'error': 'Review not found'}), 404
        flash('Review not found', 'error')
        return redirect(url_for('reviews.list_reviews'))
    
    Review.update_status(review_id, 'rejected')
    
    if request.is_json:
        return jsonify({'message': 'Review rejected successfully'}), 200
    
    flash('Review rejected', 'success')
    return redirect(url_for('reviews.list_reviews'))


@bp.route('/<review_id>/delete', methods=['POST'])
def delete_review(review_id):
    """Delete a review."""
    user_id = session.get('user_id')
    user_role = session.get('user_role')
    
    if not user_id:
        if request.is_json:
            return jsonify({'error': 'Authentication required'}), 401
        return redirect(url_for('auth.login'))
    
    review = Review.find_by_id(review_id)
    if not review:
        if request.is_json:
            return jsonify({'error': 'Review not found'}), 404
        flash('Review not found', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Check permissions
    if str(review['reviewer_id']) != user_id and user_role != 'admin':
        if request.is_json:
            return jsonify({'error': 'Permission denied'}), 403
        flash('Permission denied', 'error')
        return redirect(url_for('main.dashboard'))
    
    Review.delete(review_id)
    
    if request.is_json:
        return jsonify({'message': 'Review deleted successfully'}), 200
    
    flash('Review deleted successfully', 'success')
    return redirect(url_for('main.dashboard'))
