"""Audit logging models for tracking all system activities."""
from datetime import datetime
from app import mongo
from bson import ObjectId


class AuditLog:
    """Base audit log model."""
    
    collection = 'audit_logs'
    
    # Log categories
    CATEGORY_AUTH = 'authentication'
    CATEGORY_USER = 'user_management'
    CATEGORY_BOOK = 'book_management'
    CATEGORY_REVIEW = 'review_management'
    CATEGORY_COMPETITION = 'competition_management'
    CATEGORY_ADMIN = 'admin_action'
    CATEGORY_SYSTEM = 'system'
    CATEGORY_SECURITY = 'security'
    
    # Action types
    ACTION_LOGIN = 'login'
    ACTION_LOGOUT = 'logout'
    ACTION_LOGIN_FAILED = 'login_failed'
    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'
    ACTION_APPROVE = 'approve'
    ACTION_REJECT = 'reject'
    ACTION_UPLOAD = 'upload'
    ACTION_DOWNLOAD = 'download'
    ACTION_VIEW = 'view'
    ACTION_ERROR = 'error'
    ACTION_WARNING = 'warning'
    
    @staticmethod
    def log(category, action, user_id=None, target_type=None, target_id=None, 
            details=None, ip_address=None, user_agent=None, success=True, error_message=None):
        """
        Create an audit log entry.
        
        Args:
            category: Log category (AUTH, USER, BOOK, etc.)
            action: Action performed (LOGIN, CREATE, UPDATE, etc.)
            user_id: ID of user performing action (None for anonymous)
            target_type: Type of target entity (user, book, review, etc.)
            target_id: ID of target entity
            details: Additional details as dict
            ip_address: User's IP address
            user_agent: User's browser/client
            success: Whether action succeeded
            error_message: Error message if failed
        """
        log_entry = {
            'category': category,
            'action': action,
            'user_id': ObjectId(user_id) if user_id else None,
            'target_type': target_type,
            'target_id': ObjectId(target_id) if target_id and target_id != 'unknown' else target_id,
            'details': details or {},
            'ip_address': ip_address,
            'user_agent': user_agent,
            'success': success,
            'error_message': error_message,
            'timestamp': datetime.utcnow()
        }
        
        result = mongo.db[AuditLog.collection].insert_one(log_entry)
        return result.inserted_id
    
    @staticmethod
    def find_by_user(user_id, limit=50):
        """Find audit logs for a specific user."""
        return list(mongo.db[AuditLog.collection].find(
            {'user_id': ObjectId(user_id)}
        ).sort('timestamp', -1).limit(limit))
    
    @staticmethod
    def find_by_category(category, limit=100):
        """Find audit logs by category."""
        return list(mongo.db[AuditLog.collection].find(
            {'category': category}
        ).sort('timestamp', -1).limit(limit))
    
    @staticmethod
    def find_by_target(target_type, target_id, limit=50):
        """Find audit logs for a specific target entity."""
        query = {'target_type': target_type}
        if target_id:
            query['target_id'] = ObjectId(target_id) if target_id != 'unknown' else target_id
        return list(mongo.db[AuditLog.collection].find(query).sort('timestamp', -1).limit(limit))
    
    @staticmethod
    def find_failed_logins(hours=24, limit=100):
        """Find failed login attempts in last N hours."""
        from datetime import timedelta
        since = datetime.utcnow() - timedelta(hours=hours)
        return list(mongo.db[AuditLog.collection].find({
            'category': AuditLog.CATEGORY_AUTH,
            'action': AuditLog.ACTION_LOGIN_FAILED,
            'timestamp': {'$gte': since}
        }).sort('timestamp', -1).limit(limit))
    
    @staticmethod
    def find_recent(limit=100, category=None):
        """Find recent audit logs."""
        query = {}
        if category:
            query['category'] = category
        return list(mongo.db[AuditLog.collection].find(query).sort('timestamp', -1).limit(limit))
    
    @staticmethod
    def get_user_stats(user_id):
        """Get activity statistics for a user."""
        pipeline = [
            {'$match': {'user_id': ObjectId(user_id)}},
            {'$group': {
                '_id': '$category',
                'count': {'$sum': 1},
                'last_activity': {'$max': '$timestamp'}
            }}
        ]
        return list(mongo.db[AuditLog.collection].aggregate(pipeline))
    
    @staticmethod
    def get_system_stats(days=7):
        """Get system-wide activity statistics."""
        from datetime import timedelta
        since = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {'$match': {'timestamp': {'$gte': since}}},
            {'$group': {
                '_id': {
                    'category': '$category',
                    'action': '$action'
                },
                'count': {'$sum': 1},
                'success_count': {
                    '$sum': {'$cond': ['$success', 1, 0]}
                },
                'failure_count': {
                    '$sum': {'$cond': ['$success', 0, 1]}
                }
            }},
            {'$sort': {'count': -1}}
        ]
        return list(mongo.db[AuditLog.collection].aggregate(pipeline))


class UserSession:
    """Track user login sessions."""
    
    collection = 'user_sessions'
    
    @staticmethod
    def create_session(user_id, ip_address=None, user_agent=None):
        """Create a new session record."""
        session_data = {
            'user_id': ObjectId(user_id),
            'login_time': datetime.utcnow(),
            'ip_address': ip_address,
            'user_agent': user_agent,
            'is_active': True,
            'logout_time': None
        }
        result = mongo.db[UserSession.collection].insert_one(session_data)
        
        # Update user's last login
        mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$set': {
                    'last_login': datetime.utcnow(),
                    'last_login_ip': ip_address
                }
            }
        )
        
        return result.inserted_id
    
    @staticmethod
    def end_session(session_id):
        """End a session."""
        mongo.db[UserSession.collection].update_one(
            {'_id': ObjectId(session_id)},
            {
                '$set': {
                    'logout_time': datetime.utcnow(),
                    'is_active': False
                }
            }
        )
    
    @staticmethod
    def get_user_sessions(user_id, limit=10):
        """Get user's recent sessions."""
        return list(mongo.db[UserSession.collection].find(
            {'user_id': ObjectId(user_id)}
        ).sort('login_time', -1).limit(limit))
    
    @staticmethod
    def get_active_sessions(user_id):
        """Get user's active sessions."""
        return list(mongo.db[UserSession.collection].find({
            'user_id': ObjectId(user_id),
            'is_active': True
        }))
