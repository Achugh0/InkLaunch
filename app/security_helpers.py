"""Security audit helper - ObjectId validation wrapper."""
from functools import wraps
from flask import flash, redirect, url_for, abort
from app.security import validate_object_id


def validate_id_param(param_name='id', redirect_to='main.index'):
    """Decorator to validate ObjectId parameters."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            id_value = kwargs.get(param_name)
            if id_value and not validate_object_id(id_value):
                flash('Invalid ID format', 'error')
                if redirect_to:
                    return redirect(url_for(redirect_to))
                abort(400)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
