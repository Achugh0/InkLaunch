"""User routes."""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash, current_app
from app.models import User, Book, Review, CompetitionSubmission
from app.services.s3_service import s3_service
from app import bcrypt, mongo
from bson import ObjectId
from datetime import datetime
from werkzeug.utils import secure_filename
import os

bp = Blueprint('users', __name__, url_prefix='/users')


def allowed_file(filename):
    """Check if file extension is allowed."""
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'jpg', 'jpeg', 'png', 'gif'})
    return ext in allowed


@bp.route('/')
def list_users():
    """List and search users."""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('ITEMS_PER_PAGE', 20)
    query = request.args.get('q', '').strip()
    role_filter = request.args.get('role', '')
    status_filter = request.args.get('status', '')
    sort_by = request.args.get('sort', 'created_at')
    
    # Build filters
    filters = {}
    if role_filter:
        filters['role'] = role_filter
    if status_filter == 'active':
        filters['is_active'] = True
    elif status_filter == 'inactive':
        filters['is_active'] = False
    
    # Set sort order
    sort_mapping = {
        'created_at': [('created_at', -1)],
        'name': [('full_name', 1)],
        'books': [('total_nominations', -1)],
        'wins': [('total_wins', -1)]
    }
    sort_order = sort_mapping.get(sort_by, [('created_at', -1)])
    
    # Search users
    skip = (page - 1) * per_page
    users = User.search(query=query, filters=filters, skip=skip, limit=per_page, sort=sort_order)
    total = User.count_search(query=query, filters=filters)
    
    # Enrich with book counts
    for user in users:
        user['book_count'] = Book.count({'user_id': user['_id']})
    
    total_pages = (total + per_page - 1) // per_page
    
    if request.is_json:
        return jsonify({
            'users': [{
                'id': str(u['_id']),
                'user_id': u.get('user_id', ''),
                'full_name': u['full_name'],
                'email': u['email'],
                'bio': u.get('bio', ''),
                'role': u.get('role', 'user'),
                'book_count': u.get('book_count', 0),
                'total_wins': u.get('total_wins', 0)
            } for u in users],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages
        }), 200
    
    return render_template('users/list.html', 
                         users=users, 
                         page=page, 
                         total=total, 
                         per_page=per_page,
                         total_pages=total_pages,
                         query=query,
                         role_filter=role_filter,
                         status_filter=status_filter,
                         sort_by=sort_by)


@bp.route('/<user_id>')
def get_user(user_id):
    """Get user public profile with achievements and badges."""
    user = User.find_by_id(user_id)
    
    if not user:
        if request.is_json:
            return jsonify({'error': 'User not found'}), 404
        flash('User not found', 'danger')
        return redirect(url_for('main.index'))
    
    # Increment profile views
    from app import mongo
    mongo.db['users'].update_one(
        {'_id': user['_id']},
        {'$inc': {'profile_views': 1}}
    )
    
    # Get user's books
    books = Book.find_by_user(user_id)
    
    # Get user's reviews
    reviews = Review.find_by_reviewer(user_id)
    
    # Get competition statistics
    competition_stats = user.get('competition_stats', {
        'total_entered': 0,
        'total_wins': 0,
        'total_finalist': 0,
        'total_submissions': 0,
        'best_rank': None
    })
    
    # Get badges (sorted by date, newest first)
    badges = sorted(
        user.get('badges', []), 
        key=lambda x: x.get('earned_date', datetime.min), 
        reverse=True
    )
    
    # Get milestones
    milestones = sorted(
        user.get('milestones', []),
        key=lambda x: x.get('date', datetime.min),
        reverse=True
    )
    
    # Get competition submissions for this user
    submissions = list(mongo.db['competition_submissions'].find(
        {'author_id': ObjectId(user_id)}
    ).sort('submitted_at', -1).limit(10))
    
    # Get competition details for submissions
    for submission in submissions:
        comp = mongo.db['competitions'].find_one({'_id': submission['competition_id']})
        submission['competition'] = comp
    
    # Check if user is featured
    from datetime import datetime
    is_featured = False
    featured_until = user.get('featured_until')
    if featured_until and featured_until > datetime.utcnow():
        is_featured = True
    
    # Check premium status
    is_premium = False
    premium_until = user.get('premium_until')
    if premium_until and premium_until > datetime.utcnow():
        is_premium = True
    
    if request.is_json:
        return jsonify({
            'id': str(user['_id']),
            'full_name': user['full_name'],
            'bio': user.get('bio', ''),
            'profile_image_url': user.get('profile_image_url', ''),
            'total_nominations': user.get('total_nominations', 0),
            'total_wins': user.get('total_wins', 0),
            'books_count': len(books),
            'reviews_count': len(reviews),
            'competition_stats': competition_stats,
            'badges': badges,
            'is_featured': is_featured,
            'is_premium': is_premium
        }), 200
    
    return render_template('users/public_profile.html', 
                         user=user, 
                         books=books, 
                         reviews_count=len(reviews),
                         competition_stats=competition_stats,
                         badges=badges,
                         milestones=milestones,
                         recent_submissions=submissions,
                         is_featured=is_featured,
                         is_premium=is_premium)


@bp.route('/author/<username>')
def get_user_by_username(username):
    """Get user by username - for SEO-friendly URLs."""
    user = User.find_by_username(username)
    
    if not user:
        flash('Author not found', 'danger')
        return redirect(url_for('main.index'))
    
    # Redirect to the main profile route
    return get_user(str(user['_id']))


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
    
    data = request.form if not request.is_json else request.get_json()
    
    update_data = {}
    if 'full_name' in data:
        update_data['full_name'] = data['full_name'].strip()
    if 'bio' in data:
        bio = data['bio'].strip()
        # Limit bio to 500 words
        words = bio.split()
        if len(words) > 500:
            bio = ' '.join(words[:500])
        update_data['bio'] = bio
    if 'website_url' in data:
        update_data['website_url'] = data['website_url'].strip()
    
    # Social media links
    social_links = {}
    for platform in ['twitter', 'facebook', 'instagram', 'linkedin', 'goodreads', 'amazon_author']:
        if f'social_{platform}' in data:
            social_links[platform] = data[f'social_{platform}'].strip()
    if social_links:
        update_data['social_links'] = social_links
    
    # Handle profile image upload
    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file and file.filename and allowed_file(file.filename):
            try:
                # Delete old profile image if exists
                old_image = user.get('profile_image_url', '')
                if old_image:
                    if 's3.amazonaws.com' in old_image:
                        s3_service.delete_file(old_image)
                    elif old_image.startswith('/uploads/'):
                        old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.basename(old_image))
                        if os.path.exists(old_path):
                            try:
                                os.remove(old_path)
                            except:
                                pass
                
                # Upload new image
                if s3_service.is_s3_configured():
                    profile_url = s3_service.upload_file(file, folder='profiles')
                    if profile_url:
                        update_data['profile_image_url'] = profile_url
                else:
                    # Fallback to local storage
                    filename = secure_filename(file.filename)
                    timestamp = datetime.utcnow().timestamp()
                    unique_filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
                    file.save(filepath)
                    update_data['profile_image_url'] = f"/uploads/{unique_filename}"
            except Exception as e:
                current_app.logger.error(f"Failed to upload profile image: {str(e)}")
    
    # Handle banner image upload
    if 'banner_image' in request.files:
        file = request.files['banner_image']
        if file and file.filename and allowed_file(file.filename):
            try:
                # Delete old banner image if exists
                old_banner = user.get('banner_image_url', '')
                if old_banner:
                    if 's3.amazonaws.com' in old_banner:
                        s3_service.delete_file(old_banner)
                    elif old_banner.startswith('/uploads/'):
                        old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.basename(old_banner))
                        if os.path.exists(old_path):
                            try:
                                os.remove(old_path)
                            except:
                                pass
                
                # Upload new banner
                if s3_service.is_s3_configured():
                    banner_url = s3_service.upload_file(file, folder='banners')
                    if banner_url:
                        update_data['banner_image_url'] = banner_url
                else:
                    # Fallback to local storage
                    filename = secure_filename(file.filename)
                    timestamp = datetime.utcnow().timestamp()
                    unique_filename = f"banner_{timestamp}_{filename}"
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                    os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
                    file.save(filepath)
                    update_data['banner_image_url'] = f"/uploads/{unique_filename}"
            except Exception as e:
                current_app.logger.error(f"Failed to upload banner image: {str(e)}")
    
    update_data['updated_at'] = datetime.utcnow()
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


@bp.route('/me/delete-photo', methods=['POST'])
def delete_profile_photo():
    """Delete current user's profile photo."""
    user_id = session.get('user_id')
    
    if not user_id:
        if request.is_json:
            return jsonify({'error': 'Authentication required'}), 401
        flash('Authentication required', 'error')
        return redirect(url_for('auth.login'))
    
    user = User.find_by_id(user_id)
    
    # Delete old profile image if exists
    old_image = user.get('profile_image_url', '')
    if old_image:
        if 's3.amazonaws.com' in old_image:
            s3_service.delete_file(old_image)
        elif old_image.startswith('/uploads/'):
            old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.basename(old_image))
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except:
                    pass
    
    # Remove from database
    User.update(user_id, {'profile_image_url': ''})
    
    if request.is_json:
        return jsonify({'message': 'Profile photo deleted successfully'}), 200
    
    flash('Profile photo deleted successfully', 'success')
    return redirect(url_for('auth.profile'))
