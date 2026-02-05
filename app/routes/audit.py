"""Admin routes for audit logs."""
from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from app.models_audit import AuditLog, UserSession
from app.models import User
from datetime import datetime, timedelta

bp = Blueprint('audit', __name__, url_prefix='/admin/audit')


@bp.route('/')
def index():
    """Audit logs dashboard."""
    if session.get('user_role') != 'admin':
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    # Get filter parameters
    category = request.args.get('category', '')
    days = int(request.args.get('days', 7))
    
    # Get recent logs
    logs = AuditLog.find_recent(limit=100, category=category if category else None)
    
    # Enrich logs with user info
    for log in logs:
        if log.get('user_id'):
            user = User.find_by_id(str(log['user_id']))
            log['user'] = user
    
    # Get system stats
    stats = AuditLog.get_system_stats(days=days)
    
    # Count logs by category
    category_counts = {}
    for log in logs:
        cat = log.get('category', 'unknown')
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    return render_template('admin/audit/index.html',
                         logs=logs,
                         stats=stats,
                         category_counts=category_counts,
                         selected_category=category,
                         days=days)


@bp.route('/user/<user_id>')
def user_logs(user_id):
    """View audit logs for a specific user."""
    if session.get('user_role') != 'admin':
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    user = User.find_by_id(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('audit.index'))
    
    logs = AuditLog.find_by_user(user_id, limit=100)
    sessions = UserSession.get_user_sessions(user_id, limit=20)
    stats = AuditLog.get_user_stats(user_id)
    
    return render_template('admin/audit/user_logs.html',
                         user=user,
                         logs=logs,
                         sessions=sessions,
                         stats=stats)


@bp.route('/category/<category>')
def category_logs(category):
    """View audit logs by category."""
    if session.get('user_role') != 'admin':
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    logs = AuditLog.find_by_category(category, limit=200)
    
    # Enrich logs with user info
    for log in logs:
        if log.get('user_id'):
            user = User.find_by_id(str(log['user_id']))
            log['user'] = user
    
    return render_template('admin/audit/category_logs.html',
                         category=category,
                         logs=logs)


@bp.route('/security')
def security_logs():
    """View security-related logs."""
    if session.get('user_role') != 'admin':
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    # Get failed logins
    failed_logins = AuditLog.find_failed_logins(hours=24, limit=100)
    
    # Group by IP address
    ip_counts = {}
    for log in failed_logins:
        ip = log.get('ip_address', 'unknown')
        ip_counts[ip] = ip_counts.get(ip, 0) + 1
    
    # Sort by count
    suspicious_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)
    
    return render_template('admin/audit/security_logs.html',
                         failed_logins=failed_logins,
                         suspicious_ips=suspicious_ips)


@bp.route('/api/recent')
def api_recent():
    """API endpoint for recent logs (for real-time updates)."""
    if session.get('user_role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    limit = int(request.args.get('limit', 20))
    category = request.args.get('category', '')
    
    logs = AuditLog.find_recent(limit=limit, category=category if category else None)
    
    # Convert to JSON-serializable format
    logs_data = []
    for log in logs:
        user = None
        if log.get('user_id'):
            user_obj = User.find_by_id(str(log['user_id']))
            if user_obj:
                user = {
                    'id': str(user_obj['_id']),
                    'email': user_obj.get('email'),
                    'full_name': user_obj.get('full_name')
                }
        
        logs_data.append({
            'id': str(log['_id']),
            'category': log.get('category'),
            'action': log.get('action'),
            'user': user,
            'target_type': log.get('target_type'),
            'success': log.get('success'),
            'error_message': log.get('error_message'),
            'timestamp': log.get('timestamp').isoformat() if log.get('timestamp') else None,
            'details': log.get('details', {})
        })
    
    return jsonify({'logs': logs_data})
