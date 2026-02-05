"""Security middleware and configuration."""
from functools import wraps
from flask import session, redirect, url_for, flash, request, abort
from datetime import datetime, timedelta


def require_login(f):
    """Decorator to require user login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access this page', 'error')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def require_admin(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access this page', 'error')
            return redirect(url_for('auth.login'))
        if session.get('user_role') != 'admin':
            flash('Admin access required', 'error')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def validate_object_id(object_id):
    """Validate MongoDB ObjectId format to prevent injection."""
    from bson import ObjectId
    from bson.errors import InvalidId
    try:
        ObjectId(object_id)
        return True
    except (InvalidId, TypeError):
        return False


def sanitize_filename(filename):
    """Sanitize filename to prevent directory traversal."""
    import os
    import re
    # Remove path components
    filename = os.path.basename(filename)
    # Remove non-alphanumeric characters except . - _
    filename = re.sub(r'[^\w\s\-\.]', '', filename)
    # Remove leading/trailing whitespace and dots
    filename = filename.strip('. ')
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    return filename


def check_rate_limit(user_id, action, limit=10, window=60):
    """
    Simple rate limiting check.
    
    Args:
        user_id: User ID
        action: Action type (login, upload, etc.)
        limit: Max attempts per window
        window: Time window in seconds
    
    Returns:
        bool: True if within limit, False if exceeded
    """
    from app import mongo
    from datetime import datetime, timedelta
    
    key = f"rate_limit:{user_id}:{action}"
    now = datetime.utcnow()
    cutoff = now - timedelta(seconds=window)
    
    # Count recent attempts
    count = mongo.db.rate_limits.count_documents({
        'key': key,
        'timestamp': {'$gte': cutoff}
    })
    
    if count >= limit:
        return False
    
    # Record this attempt
    mongo.db.rate_limits.insert_one({
        'key': key,
        'timestamp': now
    })
    
    # Cleanup old records
    mongo.db.rate_limits.delete_many({
        'timestamp': {'$lt': cutoff}
    })
    
    return True


class SecurityHeaders:
    """Security headers middleware."""
    
    @staticmethod
    def init_app(app):
        """Add security headers to all responses."""
        @app.after_request
        def add_security_headers(response):
            # Prevent clickjacking
            response.headers['X-Frame-Options'] = 'SAMEORIGIN'
            
            # Prevent MIME type sniffing
            response.headers['X-Content-Type-Options'] = 'nosniff'
            
            # Enable XSS protection
            response.headers['X-XSS-Protection'] = '1; mode=block'
            
            # Strict transport security (HTTPS only)
            if app.config.get('FORCE_HTTPS', True):
                response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            
            # Content Security Policy
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://code.jquery.com; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
                "img-src 'self' data: https: http:; "
                "connect-src 'self' https://api.cloudinary.com"
            )
            response.headers['Content-Security-Policy'] = csp
            
            # Referrer policy
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            
            # Permissions policy
            response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
            
            return response


def generate_csrf_token():
    """Generate CSRF token for forms."""
    import secrets
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(32)
    return session['_csrf_token']


def validate_csrf_token(token):
    """Validate CSRF token."""
    return token == session.get('_csrf_token')
