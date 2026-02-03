"""Database models using PyMongo."""
from datetime import datetime
from bson import ObjectId
from app import mongo, bcrypt


class User:
    """User model."""
    
    collection = 'users'
    
    @staticmethod
    def create(email, password, full_name, bio='', role='user'):
        """Create a new user."""
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        user_data = {
            'email': email.lower(),
            'password_hash': password_hash,
            'full_name': full_name,
            'bio': bio,
            'profile_image_url': '',
            'role': role,
            'is_active': True,
            'total_nominations': 0,
            'total_wins': 0,
            'author_of_month_count': 0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = mongo.db[User.collection].insert_one(user_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_email(email):
        """Find user by email."""
        return mongo.db[User.collection].find_one({'email': email.lower()})
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID."""
        try:
            return mongo.db[User.collection].find_one({'_id': ObjectId(user_id)})
        except:
            return None
    
    @staticmethod
    def verify_password(user, password):
        """Verify user password."""
        return bcrypt.check_password_hash(user['password_hash'], password)
    
    @staticmethod
    def update(user_id, data):
        """Update user."""
        data['updated_at'] = datetime.utcnow()
        mongo.db[User.collection].update_one(
            {'_id': ObjectId(user_id)},
            {'$set': data}
        )
    
    @staticmethod
    def is_admin(user):
        """Check if user is admin."""
        return user and user.get('role') == 'admin'


class Book:
    """Book model."""
    
    collection = 'books'
    
    @staticmethod
    def create(user_id, data):
        """Create a new book."""
        book_data = {
            'user_id': ObjectId(user_id),
            'title': data.get('title'),
            'subtitle': data.get('subtitle', ''),
            'description': data.get('description'),
            'cover_image_url': data.get('cover_image_url', ''),
            'genre': data.get('genre'),
            'isbn': data.get('isbn', ''),
            'publication_date': data.get('publication_date'),
            'language': data.get('language', 'English'),
            'page_count': data.get('page_count', 0),
            'price': data.get('price', 0.0),
            'amazon_link': data.get('amazon_link', ''),
            'goodreads_link': data.get('goodreads_link', ''),
            'status': data.get('status', 'active'),
            'views_count': 0,
            'is_award_winner': False,
            'award_badges': [],
            'competition_wins': 0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = mongo.db[Book.collection].insert_one(book_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_id(book_id):
        """Find book by ID."""
        try:
            return mongo.db[Book.collection].find_one({'_id': ObjectId(book_id)})
        except:
            return None
    
    @staticmethod
    def find_all(filters=None, skip=0, limit=20, sort=None):
        """Find all books with filters."""
        query = filters or {}
        cursor = mongo.db[Book.collection].find(query)
        
        if sort:
            cursor = cursor.sort(sort)
        
        return list(cursor.skip(skip).limit(limit))
    
    @staticmethod
    def count(filters=None):
        """Count books with filters."""
        query = filters or {}
        return mongo.db[Book.collection].count_documents(query)
    
    @staticmethod
    def find_by_user(user_id):
        """Find all books by user."""
        return list(mongo.db[Book.collection].find({'user_id': ObjectId(user_id)}))
    
    @staticmethod
    def update(book_id, data):
        """Update book."""
        data['updated_at'] = datetime.utcnow()
        mongo.db[Book.collection].update_one(
            {'_id': ObjectId(book_id)},
            {'$set': data}
        )
    
    @staticmethod
    def delete(book_id):
        """Delete book."""
        mongo.db[Book.collection].delete_one({'_id': ObjectId(book_id)})
    
    @staticmethod
    def increment_views(book_id):
        """Increment book views."""
        mongo.db[Book.collection].update_one(
            {'_id': ObjectId(book_id)},
            {'$inc': {'views_count': 1}}
        )


class Review:
    """Review model."""
    
    collection = 'reviews'
    
    @staticmethod
    def create(book_id, reviewer_id, rating, review_text):
        """Create a new review."""
        review_data = {
            'book_id': ObjectId(book_id),
            'reviewer_id': ObjectId(reviewer_id),
            'rating': rating,
            'review_text': review_text,
            'status': 'pending',
            'is_featured': False,
            'helpful_count': 0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = mongo.db[Review.collection].insert_one(review_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_id(review_id):
        """Find review by ID."""
        try:
            return mongo.db[Review.collection].find_one({'_id': ObjectId(review_id)})
        except:
            return None
    
    @staticmethod
    def find_by_book(book_id, status='approved'):
        """Find all reviews for a book."""
        query = {'book_id': ObjectId(book_id)}
        if status:
            query['status'] = status
        return list(mongo.db[Review.collection].find(query).sort('created_at', -1))
    
    @staticmethod
    def find_by_reviewer(reviewer_id):
        """Find all reviews by reviewer."""
        return list(mongo.db[Review.collection].find({'reviewer_id': ObjectId(reviewer_id)}))
    
    @staticmethod
    def update_status(review_id, status):
        """Update review status."""
        mongo.db[Review.collection].update_one(
            {'_id': ObjectId(review_id)},
            {'$set': {'status': status, 'updated_at': datetime.utcnow()}}
        )
    
    @staticmethod
    def delete(review_id):
        """Delete review."""
        mongo.db[Review.collection].delete_one({'_id': ObjectId(review_id)})
    
    @staticmethod
    def get_average_rating(book_id):
        """Get average rating for a book."""
        pipeline = [
            {'$match': {'book_id': ObjectId(book_id), 'status': 'approved'}},
            {'$group': {'_id': None, 'avg_rating': {'$avg': '$rating'}, 'count': {'$sum': 1}}}
        ]
        result = list(mongo.db[Review.collection].aggregate(pipeline))
        if result:
            return {'average': round(result[0]['avg_rating'], 1), 'count': result[0]['count']}
        return {'average': 0, 'count': 0}


class ReviewRequest:
    """Review request model."""
    
    collection = 'review_requests'
    
    @staticmethod
    def create(book_id, requester_id, requested_user_id, message=''):
        """Create a review request."""
        request_data = {
            'book_id': ObjectId(book_id),
            'requester_id': ObjectId(requester_id),
            'requested_user_id': ObjectId(requested_user_id),
            'message': message,
            'status': 'open',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = mongo.db[ReviewRequest.collection].insert_one(request_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_user(user_id):
        """Find all review requests for a user."""
        return list(mongo.db[ReviewRequest.collection].find(
            {'requested_user_id': ObjectId(user_id), 'status': 'open'}
        ))
    
    @staticmethod
    def update_status(request_id, status):
        """Update request status."""
        mongo.db[ReviewRequest.collection].update_one(
            {'_id': ObjectId(request_id)},
            {'$set': {'status': status, 'updated_at': datetime.utcnow()}}
        )


class Article:
    """Article model."""
    
    collection = 'articles'
    
    @staticmethod
    def create(author_id, title, content, category, excerpt='', status='draft'):
        """Create a new article."""
        import re
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        
        article_data = {
            'author_id': ObjectId(author_id),
            'title': title,
            'slug': slug,
            'content': content,
            'excerpt': excerpt,
            'featured_image': '',
            'category': category,
            'tags': [],
            'status': status,
            'views_count': 0,
            'published_at': datetime.utcnow() if status == 'published' else None,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = mongo.db[Article.collection].insert_one(article_data)
        return result.inserted_id
    
    @staticmethod
    def find_published(skip=0, limit=20):
        """Find all published articles."""
        return list(mongo.db[Article.collection].find(
            {'status': 'published'}
        ).sort('published_at', -1).skip(skip).limit(limit))
    
    @staticmethod
    def find_by_slug(slug):
        """Find article by slug."""
        return mongo.db[Article.collection].find_one({'slug': slug})


class CompetitionPeriod:
    """Competition period model."""
    
    collection = 'competition_periods'
    
    @staticmethod
    def create(month, year, start_date, end_date, nomination_deadline):
        """Create a competition period."""
        period_data = {
            'month': month,
            'year': year,
            'start_date': start_date,
            'end_date': end_date,
            'nomination_deadline': nomination_deadline,
            'winner_announcement_date': None,
            'status': 'active',
            'theme': '',
            'description': '',
            'prize_details': '',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = mongo.db[CompetitionPeriod.collection].insert_one(period_data)
        return result.inserted_id
    
    @staticmethod
    def find_active():
        """Find active competition period."""
        return mongo.db[CompetitionPeriod.collection].find_one({'status': 'active'})
    
    @staticmethod
    def find_by_id(period_id):
        """Find period by ID."""
        try:
            return mongo.db[CompetitionPeriod.collection].find_one({'_id': ObjectId(period_id)})
        except:
            return None


class Nomination:
    """Nomination model."""
    
    collection = 'competition_nominations'
    
    @staticmethod
    def create(period_id, book_id, user_id, nomination_statement):
        """Create a nomination."""
        nomination_data = {
            'period_id': ObjectId(period_id),
            'book_id': ObjectId(book_id),
            'user_id': ObjectId(user_id),
            'nomination_statement': nomination_statement,
            'submission_date': datetime.utcnow(),
            'status': 'pending',
            'admin_notes': '',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = mongo.db[Nomination.collection].insert_one(nomination_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_period(period_id):
        """Find all nominations for a period."""
        return list(mongo.db[Nomination.collection].find({'period_id': ObjectId(period_id)}))
    
    @staticmethod
    def find_by_user_and_period(user_id, period_id):
        """Find user's nomination for a period."""
        return mongo.db[Nomination.collection].find_one({
            'user_id': ObjectId(user_id),
            'period_id': ObjectId(period_id)
        })


class AIBookReview:
    """AI book review model."""
    
    collection = 'ai_book_reviews'
    
    @staticmethod
    def create(nomination_id, book_id, review_data):
        """Create an AI review."""
        ai_review_data = {
            'nomination_id': ObjectId(nomination_id),
            'book_id': ObjectId(book_id),
            'ai_model': review_data.get('ai_model', 'gpt-4-turbo'),
            'overall_rating': review_data.get('overall_rating'),
            'content_quality_score': review_data.get('content_quality_score'),
            'writing_style_score': review_data.get('writing_style_score'),
            'originality_score': review_data.get('originality_score'),
            'market_potential_score': review_data.get('market_potential_score'),
            'technical_quality_score': review_data.get('technical_quality_score'),
            'review_summary': review_data.get('review_summary'),
            'strengths': review_data.get('strengths', []),
            'weaknesses': review_data.get('weaknesses', []),
            'recommendations': review_data.get('recommendations'),
            'genre_alignment': review_data.get('genre_alignment'),
            'target_audience': review_data.get('target_audience'),
            'comparable_titles': review_data.get('comparable_titles', []),
            'key_themes': review_data.get('key_themes', []),
            'readability_score': review_data.get('readability_score'),
            'sentiment_analysis': review_data.get('sentiment_analysis'),
            'processing_time_seconds': review_data.get('processing_time_seconds', 0),
            'tokens_used': review_data.get('tokens_used', 0),
            'review_date': datetime.utcnow()
        }
        
        result = mongo.db[AIBookReview.collection].insert_one(ai_review_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_nomination(nomination_id):
        """Find AI review by nomination."""
        return mongo.db[AIBookReview.collection].find_one({'nomination_id': ObjectId(nomination_id)})
