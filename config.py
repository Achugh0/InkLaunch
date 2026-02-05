"""Application configuration."""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Security
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True').lower() == 'true'  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max upload
    FORCE_HTTPS = os.getenv('FORCE_HTTPS', 'True').lower() == 'true'
    
    # Rate limiting
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'True').lower() == 'true'
    LOGIN_ATTEMPTS_LIMIT = int(os.getenv('LOGIN_ATTEMPTS_LIMIT', '5'))
    LOGIN_ATTEMPTS_WINDOW = int(os.getenv('LOGIN_ATTEMPTS_WINDOW', '900'))  # 15 minutes
    UPLOAD_RATE_LIMIT = int(os.getenv('UPLOAD_RATE_LIMIT', '10'))
    UPLOAD_RATE_WINDOW = int(os.getenv('UPLOAD_RATE_WINDOW', '3600'))  # 1 hour
    
    # MongoDB
    MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/inklaunch?serverSelectionTimeoutMS=2000&connectTimeoutMS=2000')
    MONGO_DBNAME = os.getenv('MONGODB_DB_NAME', 'inklaunch')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '86400'))
    )
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # Admin
    ADMIN_EMAILS = os.getenv('ADMIN_EMAILS', 'admin@example.com').split(',')
    
    # AWS S3
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME', 'inklaunch-book-covers')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    
    # Cloudinary (alternative to S3)
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME', '')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY', '')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET', '')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    AI_MODEL = os.getenv('AI_MODEL', 'gpt-4-turbo')
    
    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@inklaunch.com')
    
    # Upload (moved MAX_CONTENT_LENGTH to Security section above)
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,gif,webp').split(','))
    
    # Pagination
    ITEMS_PER_PAGE = int(os.getenv('ITEMS_PER_PAGE', '20'))
    
    # Validation
    REVIEW_MIN_LENGTH = int(os.getenv('REVIEW_MIN_LENGTH', '50'))
    NOMINATION_STATEMENT_MIN_LENGTH = int(os.getenv('NOMINATION_STATEMENT_MIN_LENGTH', '200'))
    NOMINATION_STATEMENT_MAX_LENGTH = int(os.getenv('NOMINATION_STATEMENT_MAX_LENGTH', '500'))


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/inklaunch_test'
    MONGO_DBNAME = 'inklaunch_test'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
