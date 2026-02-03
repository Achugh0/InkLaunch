"""Authentication routes."""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app import mongo
import re

bp = Blueprint('auth', __name__, url_prefix='/auth')


def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'GET':
        return render_template('auth/register.html')
    
    data = request.get_json() if request.is_json else request.form
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    full_name = data.get('full_name', '').strip()
    bio = data.get('bio', '').strip()
    
    # Validation
    if not email or not password or not full_name:
        if request.is_json:
            return jsonify({'error': 'Email, password, and full name are required'}), 400
        flash('Email, password, and full name are required', 'error')
        return redirect(url_for('auth.register'))
    
    if not validate_email(email):
        if request.is_json:
            return jsonify({'error': 'Invalid email format'}), 400
        flash('Invalid email format', 'error')
        return redirect(url_for('auth.register'))
    
    is_valid, msg = validate_password(password)
    if not is_valid:
        if request.is_json:
            return jsonify({'error': msg}), 400
        flash(msg, 'error')
        return redirect(url_for('auth.register'))
    
    # Check if user exists
    if User.find_by_email(email):
        if request.is_json:
            return jsonify({'error': 'Email already registered'}), 400
        flash('Email already registered', 'error')
        return redirect(url_for('auth.register'))
    
    # Determine role (admin if in admin emails)
    from flask import current_app
    role = 'admin' if email in current_app.config['ADMIN_EMAILS'] else 'user'
    
    # Create user
    user_id = User.create(email, password, full_name, bio, role)
    
    if request.is_json:
        return jsonify({
            'message': 'Registration successful',
            'user_id': str(user_id)
        }), 201
    
    flash('Registration successful! Please log in.', 'success')
    return redirect(url_for('auth.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    data = request.get_json() if request.is_json else request.form
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        if request.is_json:
            return jsonify({'error': 'Email and password are required'}), 400
        flash('Email and password are required', 'error')
        return redirect(url_for('auth.login'))
    
    user = User.find_by_email(email)
    
    if not user or not User.verify_password(user, password):
        if request.is_json:
            return jsonify({'error': 'Invalid email or password'}), 401
        flash('Invalid email or password', 'error')
        return redirect(url_for('auth.login'))
    
    if not user.get('is_active', True):
        if request.is_json:
            return jsonify({'error': 'Account is inactive'}), 403
        flash('Account is inactive', 'error')
        return redirect(url_for('auth.login'))
    
    # Create access token
    access_token = create_access_token(identity=str(user['_id']))
    
    if request.is_json:
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': str(user['_id']),
                'email': user['email'],
                'full_name': user['full_name'],
                'role': user['role']
            }
        }), 200
    
    # For web sessions
    session['user_id'] = str(user['_id'])
    session['user_email'] = user['email']
    session['user_role'] = user['role']
    
    flash('Login successful!', 'success')
    return redirect(url_for('main.dashboard'))


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """User logout."""
    session.clear()
    
    if request.is_json:
        return jsonify({'message': 'Logout successful'}), 200
    
    flash('Logged out successfully', 'success')
    return redirect(url_for('main.index'))


@bp.route('/profile', methods=['GET'])
@jwt_required(optional=True)
def profile():
    """Get current user profile."""
    user_id = get_jwt_identity() or session.get('user_id')
    
    if not user_id:
        if request.is_json:
            return jsonify({'error': 'Not authenticated'}), 401
        return redirect(url_for('auth.login'))
    
    user = User.find_by_id(user_id)
    
    if not user:
        if request.is_json:
            return jsonify({'error': 'User not found'}), 404
        flash('User not found', 'error')
        return redirect(url_for('auth.login'))
    
    if request.is_json:
        return jsonify({
            'id': str(user['_id']),
            'email': user['email'],
            'full_name': user['full_name'],
            'bio': user['bio'],
            'profile_image_url': user.get('profile_image_url', ''),
            'role': user['role'],
            'total_nominations': user.get('total_nominations', 0),
            'total_wins': user.get('total_wins', 0),
            'created_at': user['created_at'].isoformat()
        }), 200
    
    return render_template('users/profile.html', user=user)
