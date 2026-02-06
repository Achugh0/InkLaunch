"""Flask application factory."""
from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import config
import os
import markdown

# Initialize extensions
mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()


def create_app(config_name=None):
    """Application factory pattern."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    # Map common environment names to config keys
    config_mapping = {
        'prod': 'production',
        'production': 'production',
        'dev': 'development',
        'development': 'development',
        'test': 'testing',
        'testing': 'testing'
    }
    
    config_name = config_mapping.get(config_name.lower(), 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    try:
        mongo.init_app(app)
        # Test MongoDB connection
        with app.app_context():
            if mongo.db is None:
                app.logger.warning("MongoDB connection failed - mongo.db is None. Check MONGODB_URI environment variable.")
    except Exception as e:
        app.logger.error(f"Failed to initialize MongoDB: {e}")
        app.logger.error("Make sure MONGODB_URI is set in your environment variables.")
    
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    
    # Initialize security headers
    from app.security import SecurityHeaders
    SecurityHeaders.init_app(app)
    
    # Add CSRF token to all templates
    @app.context_processor
    def inject_csrf_token():
        from app.security import generate_csrf_token
        return dict(csrf_token=generate_csrf_token)
    
    # Set absolute path for upload folder
    if not os.path.isabs(app.config['UPLOAD_FOLDER']):
        app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, '..', app.config['UPLOAD_FOLDER'])
        app.config['UPLOAD_FOLDER'] = os.path.abspath(app.config['UPLOAD_FOLDER'])
    
    # Create upload folder
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register custom template filters
    @app.template_filter('markdown')
    def markdown_filter(text):
        """Convert markdown to HTML."""
        if not text:
            return ''
        return markdown.markdown(text, extensions=['nl2br', 'fenced_code', 'tables'])

    def normalize_media_url(url):
        """Normalize media URLs stored in the database."""
        if not url:
            return ''
        normalized = url.strip()
        if normalized.startswith('//'):
            return f"https:{normalized}"
        if normalized.startswith('http://'):
            return f"https://{normalized[len('http://'):]}"
        if normalized.startswith('https://'):
            return normalized
        if normalized.startswith('/'):
            return normalized
        if normalized.startswith('static/'):
            return f"/{normalized}"
        if normalized.startswith('uploads/'):
            return f"/{normalized}"
        if normalized.startswith('res.cloudinary.com/') or normalized.startswith('cloudinary.com/'):
            return f"https://{normalized}"

        bucket = app.config.get('AWS_S3_BUCKET_NAME')
        if bucket:
            region = app.config.get('AWS_REGION', 'us-east-1')
            return f"https://{bucket}.s3.{region}.amazonaws.com/{normalized}"

        return f"/{normalized}"

    app.add_template_filter(normalize_media_url, 'media_url')
    app.jinja_env.globals['media_url'] = normalize_media_url
    
    # Register blueprints
    from app.routes import auth, books, reviews, users, admin, articles, tools, competitions, services
    from app.routes import competitions_admin, manuscript_competitions, marketing, writing, audit
    from app.routes.analytics import analytics_bp
    from app.routes.pulse import pulse_bp
    from app.routes.genre_selector import genre_selector_bp
    from app.routes.genre_intelligence import genre_intel_bp
    from app.routes.brand_kit import brand_kit_bp
    from app.routes.epub_validator import epub_validator_bp
    from app.routes.metadata_editor import metadata_editor_bp
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(books.bp)
    app.register_blueprint(reviews.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(articles.bp)
    app.register_blueprint(tools.bp)
    app.register_blueprint(competitions.bp)
    app.register_blueprint(services.bp)
    app.register_blueprint(competitions_admin.bp)
    app.register_blueprint(manuscript_competitions.bp)
    app.register_blueprint(marketing.marketing_bp)
    app.register_blueprint(writing.writing_bp)
    app.register_blueprint(audit.bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(pulse_bp)
    app.register_blueprint(genre_selector_bp)
    app.register_blueprint(genre_intel_bp)
    app.register_blueprint(brand_kit_bp)
    app.register_blueprint(epub_validator_bp)
    app.register_blueprint(metadata_editor_bp)
    app.register_blueprint(analytics_bp)
    
    # Register main routes
    from app.routes import main
    app.register_blueprint(main.bp)
    
    return app
