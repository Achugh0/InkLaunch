"""User routes."""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from app.models import User, Book, Review
from app import bcrypt
from bson import ObjectId

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/<user_id>')
def get_user(user_id):
    """Get user public profile."""
    user = User.find_by_id(user_id)
    
    if not user:
        if request.is_json:
            return jsonify({'error': 'User not found'}), 404
        return "User not found", 404
    
    # Get user's books
    books = Book.find_by_user(user_id)
    
    # Get user's reviews
    reviews = Review.find_by_reviewer(user_id)
    
    if request.is_json:
        return jsonify({
            'id': str(user['_id']),
            'full_name': user['full_name'],
            'bio': user.get('bio', ''),
            'profile_image_url': user.get('profile_image_url', ''),
            'total_nominations': user.get('total_nominations', 0),
            'total_wins': user.get('total_wins', 0),
            'books_count': len(books),
            'reviews_count': len(reviews)
        }), 200
    
    return render_template('users/public_profile.html', user=user, books=books, reviews_count=len(reviews))


@bp.route('/me/edit', methods=['GET', 'POST'])
def edit_profile():
    """Edit current user profile."""
    user_id = session.get('user_id')
    
    if not user_id:
        if request.is_json:
            return jsonify({'error': 'Authentication required'}), 401
        return redirect(url_for('auth.login'))
    
    user = User.find_by_id(user_id)
    
    if request.method == 'GET':
        return render_template('users/edit_profile.html', user=user)
    
    data = request.get_json() if request.is_json else request.form
    
    update_data = {}
    if 'full_name' in data:
        update_data['full_name'] = data['full_name'].strip()
    if 'bio' in data:
        update_data['bio'] = data['bio'].strip()
    
    User.update(user_id, update_data)
    
    if request.is_json:
        return jsonify({'message': 'Profile updated successfully'}), 200
    
    flash('Profile updated successfully', 'success')
    return redirect(url_for('auth.profile'))


@bp.route('/me/change-password', methods=['GET', 'POST'])
def change_password():
    """Change current user password."""
    user_id = session.get('user_id')
    
    if not user_id:
        flash('Authentication required', 'error')
        return redirect(url_for('auth.login'))
    
    user = User.find_by_id(user_id)
    
    if request.method == 'GET':
        return render_template('users/change_password.html', user=user)
    
    data = request.get_json() if request.is_json else request.form
    
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    
    # Verify current password
    if not User.verify_password(user, current_password):
        if request.is_json:
            return jsonify({'error': 'Current password is incorrect'}), 400
        flash('Current password is incorrect', 'error')
        return render_template('users/change_password.html', user=user)
    
    # Validate new password
    if len(new_password) < 8:
        if request.is_json:
            return jsonify({'error': 'New password must be at least 8 characters'}), 400
        flash('New password must be at least 8 characters', 'error')
        return render_template('users/change_password.html', user=user)
    
    # Check if passwords match
    if new_password != confirm_password:
        if request.is_json:
            return jsonify({'error': 'Passwords do not match'}), 400
        flash('Passwords do not match', 'error')
        return render_template('users/change_password.html', user=user)
    
    # Update password
    password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    User.update(user_id, {'password_hash': password_hash})
    
    if request.is_json:
        return jsonify({'message': 'Password changed successfully'}), 200
    
    flash('Password changed successfully', 'success')
    return redirect(url_for('auth.profile'))

