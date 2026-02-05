"""Main routes."""
from flask import Blueprint, render_template, session, redirect, url_for, send_from_directory, current_app
from app.models import Book, User
from app import mongo
from bson import ObjectId

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Homepage."""
    try:
        # Get recent books
        books = Book.find_all(
            filters={'status': 'active'},
            sort=[('created_at', -1)],
            limit=12
        )
        
        # Enrich books with author info
        for book in books:
            author = User.find_by_id(str(book['user_id']))
            book['author'] = author
        
        # Get stats for homepage
        if mongo.db is not None:
            stats = {
                'total_users': mongo.db.users.count_documents({}),
                'total_books': mongo.db.books.count_documents({}),
                'total_reviews': mongo.db.reviews.count_documents({})
            }
            top_reviewers = list(mongo.db.reviews.aggregate([
                {'$match': {'status': 'approved'}},
                {'$group': {'_id': '$reviewer_id', 'review_count': {'$sum': 1}}},
                {'$sort': {'review_count': -1}},
                {'$limit': 6}
            ]))
        else:
            stats = {
                'total_users': 0,
                'total_books': 0,
                'total_reviews': 0
            }
            top_reviewers = []
    except Exception as e:
        # If database is not available, show empty page
        current_app.logger.error(f"Database connection error: {e}")
        books = []
        stats = {
            'total_users': 0,
            'total_books': 0,
            'total_reviews': 0
        }
        top_reviewers = []
    
    enriched_reviewers = []
    for item in top_reviewers:
        reviewer = User.find_by_id(str(item['_id']))
        if not reviewer:
            continue
        enriched_reviewers.append({
            'reviewer': reviewer,
            'review_count': item['review_count']
        })

    return render_template('index.html', books=books, stats=stats, top_reviewers=enriched_reviewers)


@bp.route('/dashboard')
def dashboard():
    """User dashboard."""
    user_id = session.get('user_id')
    
    if not user_id:
        return redirect(url_for('auth.login'))
    
    user = User.find_by_id(user_id)
    my_books = Book.find_by_user(user_id)
    
    return render_template('dashboard.html', user=user, books=my_books)


@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files. This is a fallback for local development.
    In production, images should be served directly from S3."""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@bp.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'healthy'}, 200
