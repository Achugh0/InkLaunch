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
        
        # Generate unique user ID (e.g., INK001234)
        user_count = mongo.db[User.collection].count_documents({}) + 1
        unique_user_id = f"INK{user_count:06d}"
        
        # Generate username from full name (for URL)
        username = full_name.lower().replace(' ', '-')
        # Ensure username is unique
        existing = mongo.db[User.collection].find_one({'username': username})
        if existing:
            username = f"{username}-{user_count}"
        
        user_data = {
            'user_id': unique_user_id,  # Unique user ID
            'username': username,  # URL-friendly username
            'email': email.lower(),
            'password_hash': password_hash,
            'full_name': full_name,
            'bio': bio,
            'profile_image_url': '',
            'banner_image_url': '',  # Profile banner image
            'website_url': '',  # Author website
            'social_links': {  # Social media profiles
                'twitter': '',
                'facebook': '',
                'instagram': '',
                'linkedin': '',
                'goodreads': '',
                'amazon_author': ''
            },
            'role': role,
            'is_active': True,
            'is_verified': False,  # Verified author badge
            'total_nominations': 0,
            'total_wins': 0,
            'author_of_month_count': 0,
            # Analytics
            'profile_views': 0,
            'follower_count': 0,
            'following_count': 0,
            # Badge and achievement system
            'badges': [],  # Array of badge objects: {type, name, icon, earned_date, competition_id}
            'achievements': [],  # Array of achievement milestones
            'competition_stats': {
                'total_entered': 0,
                'total_wins': 0,
                'total_finalist': 0,
                'total_submissions': 0,
                'best_rank': None  # 1, 2, 3 for placements
            },
            # Milestones for timeline
            'milestones': [],  # Array: {title, description, date, icon}
            'featured_until': None,  # Date when homepage feature expires
            'premium_until': None,  # Date when premium membership expires
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
    def find_by_username(username):
        """Find user by username."""
        return mongo.db[User.collection].find_one({'username': username})
    
    @staticmethod
    def search(query='', filters=None, skip=0, limit=20, sort=None):
        """Search users with filters."""
        search_filters = filters if filters else {}
        
        # Add text search if query provided
        if query:
            search_filters['$or'] = [
                {'full_name': {'$regex': query, '$options': 'i'}},
                {'email': {'$regex': query, '$options': 'i'}},
                {'bio': {'$regex': query, '$options': 'i'}},
                {'username': {'$regex': query, '$options': 'i'}},
                {'user_id': {'$regex': query, '$options': 'i'}}
            ]
        
        cursor = mongo.db[User.collection].find(search_filters)
        
        if sort:
            cursor = cursor.sort(sort)
        
        return list(cursor.skip(skip).limit(limit))
    
    @staticmethod
    def count_search(query='', filters=None):
        """Count users matching search."""
        search_filters = filters if filters else {}
        
        if query:
            search_filters['$or'] = [
                {'full_name': {'$regex': query, '$options': 'i'}},
                {'email': {'$regex': query, '$options': 'i'}},
                {'bio': {'$regex': query, '$options': 'i'}},
                {'username': {'$regex': query, '$options': 'i'}},
                {'user_id': {'$regex': query, '$options': 'i'}}
            ]
        
        return mongo.db[User.collection].count_documents(search_filters)
    
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
    
    @staticmethod
    def award_badge(user_id, badge_type, badge_name, badge_icon, competition_id=None):
        """Award a badge to a user."""
        badge = {
            'type': badge_type,  # 'competition_winner', 'competition_finalist', 'achievement'
            'name': badge_name,
            'icon': badge_icon,
            'earned_date': datetime.utcnow(),
            'competition_id': competition_id
        }
        
        mongo.db[User.collection].update_one(
            {'_id': ObjectId(user_id)},
            {
                '$push': {'badges': badge},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
    
    @staticmethod
    def update_competition_stats(user_id, stat_updates):
        """Update user's competition statistics."""
        update_fields = {'updated_at': datetime.utcnow()}
        
        for key, value in stat_updates.items():
            if key in ['total_entered', 'total_wins', 'total_finalist', 'total_submissions']:
                update_fields[f'competition_stats.{key}'] = value
            elif key == 'best_rank':
                # Only update if it's a better rank (lower number)
                user = User.find_by_id(user_id)
                current_best = user.get('competition_stats', {}).get('best_rank')
                if current_best is None or value < current_best:
                    update_fields['competition_stats.best_rank'] = value
        
        mongo.db[User.collection].update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_fields}
        )
    
    @staticmethod
    def get_competition_stats(user_id):
        """Get user's competition statistics."""
        user = User.find_by_id(user_id)
        if not user:
            return None
        return user.get('competition_stats', {
            'total_entered': 0,
            'total_wins': 0,
            'total_finalist': 0,
            'total_submissions': 0,
            'best_rank': None
        })


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
            # Enhanced metadata
            'genres': data.get('genres', [data.get('genre')]) if data.get('genre') else [],  # Multiple genres (up to 5)
            'genre': data.get('genre'),  # Primary genre for backwards compatibility
            'isbn': data.get('isbn', ''),
            'isbn13': data.get('isbn13', ''),
            'publisher': data.get('publisher', ''),
            'publication_date': data.get('publication_date'),
            'language': data.get('language', 'English'),
            'page_count': data.get('page_count', 0),
            'word_count': data.get('word_count', 0),
            'format': data.get('format', 'ebook'),  # ebook, paperback, hardcover, audiobook
            'edition': data.get('edition', '1st'),
            # Series information
            'series_name': data.get('series_name', ''),
            'series_number': data.get('series_number', 0),
            'is_series': data.get('is_series', False),
            # Content ratings
            'age_rating': data.get('age_rating', 'all-ages'),  # all-ages, 13+, 16+, 18+
            'trigger_warnings': data.get('trigger_warnings', []),  # Array of warning tags
            'content_tags': data.get('content_tags', []),  # Additional content descriptors
            # Pricing and links
            'price': data.get('price', 0.0),
            'amazon_link': data.get('amazon_link', ''),
            'goodreads_link': data.get('goodreads_link', ''),
            'purchase_links': data.get('purchase_links', {}),  # {store_name: url}
            # Sample content
            'sample_chapter': data.get('sample_chapter', ''),  # First chapter/excerpt (3000 words max)
            'excerpt': data.get('excerpt', ''),  # Short excerpt for preview
            # Characters and setting
            'characters': data.get('characters', []),  # Array: {name, description, image_url}
            'settings': data.get('settings', []),  # Array: {name, description}
            # Status and visibility
            'status': data.get('status', 'active'),
            'is_published': data.get('is_published', True),
            'publish_date': data.get('publish_date', datetime.utcnow()),
            # Awards and recognition
            'is_award_winner': False,
            'award_badges': [],
            'competition_wins': 0,
            # Analytics
            'views_count': 0,
            'unique_views': 0,
            'favorites_count': 0,
            'shares_count': 0,
            'sample_reads': 0,
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
    def search(query='', filters=None, skip=0, limit=20, sort=None):
        """Search books with filters."""
        search_filters = filters if filters else {}
        
        # Add text search if query provided
        if query:
            search_filters['$or'] = [
                {'title': {'$regex': query, '$options': 'i'}},
                {'subtitle': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}},
                {'genre': {'$regex': query, '$options': 'i'}},
                {'isbn': {'$regex': query, '$options': 'i'}}
            ]
        
        cursor = mongo.db[Book.collection].find(search_filters)
        
        if sort:
            cursor = cursor.sort(sort)
        else:
            cursor = cursor.sort([('created_at', -1)])
        
        return list(cursor.skip(skip).limit(limit))
    
    @staticmethod
    def count_search(query='', filters=None):
        """Count books matching search."""
        search_filters = filters if filters else {}
        
        if query:
            search_filters['$or'] = [
                {'title': {'$regex': query, '$options': 'i'}},
                {'subtitle': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}},
                {'genre': {'$regex': query, '$options': 'i'}},
                {'isbn': {'$regex': query, '$options': 'i'}}
            ]
        
        return mongo.db[Book.collection].count_documents(search_filters)
    
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
    def find_by_category(category, skip=0, limit=20):
        """Find published articles by category."""
        return list(mongo.db[Article.collection].find(
            {'status': 'published', 'category': category}
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


class Competition:
    """Competition model."""
    
    collection = 'competitions'
    
    @staticmethod
    def create(title, description, genre_categories, submission_start_date, submission_end_date,
               evaluation_criteria, max_submissions_per_author, entry_fee_amount, prize_structure,
               created_by_admin_id, winner_announcement_date=None):
        """Create a new competition."""
        competition_data = {
            'title': title,
            'description': description,
            'genre_categories': genre_categories,  # Array of genres
            'submission_start_date': submission_start_date,
            'submission_end_date': submission_end_date,
            'evaluation_criteria': evaluation_criteria,  # JSON with weighted criteria
            'max_submissions_per_author': max_submissions_per_author,
            'entry_fee_amount': entry_fee_amount,
            'prize_structure': prize_structure,  # JSON for 1st/2nd/3rd prizes
            'status': 'draft',  # draft, accepting_submissions, closed, evaluating, admin_review, completed, archived
            'winner_announcement_date': winner_announcement_date,
            'visibility_settings': {
                'show_rankings': False,
                'show_scores': False,
                'show_feedback_to_all': False
            },
            'created_by_admin_id': ObjectId(created_by_admin_id),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = mongo.db[Competition.collection].insert_one(competition_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_id(competition_id):
        """Find competition by ID."""
        try:
            return mongo.db[Competition.collection].find_one({'_id': ObjectId(competition_id)})
        except:
            return None
    
    @staticmethod
    def find_all(status=None, skip=0, limit=20):
        """Find all competitions, optionally filtered by status."""
        query = {}
        if status:
            query['status'] = status
        
        competitions = list(mongo.db[Competition.collection]
                          .find(query)
                          .sort('created_at', -1)
                          .skip(skip)
                          .limit(limit))
        return competitions
    
    @staticmethod
    def find_active():
        """Find all active competitions (accepting submissions)."""
        now = datetime.utcnow()
        query = {
            'status': 'accepting_submissions',
            'submission_start_date': {'$lte': now},
            'submission_end_date': {'$gte': now}
        }
        return list(mongo.db[Competition.collection].find(query).sort('submission_end_date', 1))
    
    @staticmethod
    def find_upcoming():
        """Find upcoming competitions (not yet started)."""
        now = datetime.utcnow()
        query = {
            'status': 'accepting_submissions',
            'submission_start_date': {'$gt': now}
        }
        return list(mongo.db[Competition.collection].find(query).sort('submission_start_date', 1))
    
    @staticmethod
    def update_status(competition_id, status):
        """Update competition status."""
        mongo.db[Competition.collection].update_one(
            {'_id': ObjectId(competition_id)},
            {
                '$set': {
                    'status': status,
                    'updated_at': datetime.utcnow()
                }
            }
        )
    
    @staticmethod
    def update(competition_id, update_data):
        """Update competition data."""
        update_data['updated_at'] = datetime.utcnow()
        mongo.db[Competition.collection].update_one(
            {'_id': ObjectId(competition_id)},
            {'$set': update_data}
        )
    
    @staticmethod
    def count_submissions(competition_id):
        """Count total submissions for a competition."""
        return mongo.db[CompetitionSubmission.collection].count_documents({
            'competition_id': ObjectId(competition_id)
        })


class CompetitionSubmission:
    """Competition submission model."""
    
    collection = 'competition_submissions'
    
    @staticmethod
    def create(competition_id, author_id, manuscript_title, manuscript_file_url,
               word_count, genre, synopsis, author_statement='', entry_fee_paid=False):
        """Create a new competition submission."""
        submission_data = {
            'competition_id': ObjectId(competition_id),
            'author_id': ObjectId(author_id),
            'manuscript_title': manuscript_title,
            'manuscript_file_url': manuscript_file_url,
            'word_count': word_count,
            'genre': genre,
            'synopsis': synopsis,
            'author_statement': author_statement,
            'submission_timestamp': datetime.utcnow(),
            'entry_fee_paid': entry_fee_paid,
            'payment_transaction_id': '',
            'submission_status': 'pending',  # pending, validated, under_review, disqualified, winner, participant
            'disqualification_reason': '',
            'created_at': datetime.utcnow()
        }
        
        result = mongo.db[CompetitionSubmission.collection].insert_one(submission_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_id(submission_id):
        """Find submission by ID."""
        try:
            return mongo.db[CompetitionSubmission.collection].find_one({'_id': ObjectId(submission_id)})
        except:
            return None
    
    @staticmethod
    def find_by_competition(competition_id, skip=0, limit=100):
        """Find all submissions for a competition."""
        submissions = list(mongo.db[CompetitionSubmission.collection]
                          .find({'competition_id': ObjectId(competition_id)})
                          .sort('submission_timestamp', -1)
                          .skip(skip)
                          .limit(limit))
        return submissions
    
    @staticmethod
    def find_by_author(author_id, skip=0, limit=20):
        """Find all submissions by an author."""
        submissions = list(mongo.db[CompetitionSubmission.collection]
                          .find({'author_id': ObjectId(author_id)})
                          .sort('submission_timestamp', -1)
                          .skip(skip)
                          .limit(limit))
        return submissions
    
    @staticmethod
    def count_by_author_and_competition(author_id, competition_id):
        """Count submissions by author for a specific competition."""
        return mongo.db[CompetitionSubmission.collection].count_documents({
            'author_id': ObjectId(author_id),
            'competition_id': ObjectId(competition_id)
        })
    
    @staticmethod
    def update_status(submission_id, status, disqualification_reason=''):
        """Update submission status."""
        update_data = {
            'submission_status': status
        }
        if disqualification_reason:
            update_data['disqualification_reason'] = disqualification_reason
        
        mongo.db[CompetitionSubmission.collection].update_one(
            {'_id': ObjectId(submission_id)},
            {'$set': update_data}
        )


class AIEvaluation:
    """AI evaluation model for competition submissions."""
    
    collection = 'ai_evaluations'
    
    @staticmethod
    def create(submission_id, competition_id, ai_model_version, criteria_scores,
               overall_score, strengths_identified, weaknesses_identified,
               detailed_feedback, confidence_score, processing_time_seconds):
        """Create a new AI evaluation."""
        evaluation_data = {
            'submission_id': ObjectId(submission_id),
            'competition_id': ObjectId(competition_id),
            'ai_model_version': ai_model_version,
            'evaluation_timestamp': datetime.utcnow(),
            'criteria_scores': criteria_scores,  # JSON breakdown by criterion
            'overall_score': overall_score,
            'strengths_identified': strengths_identified,  # Array
            'weaknesses_identified': weaknesses_identified,  # Array
            'detailed_feedback': detailed_feedback,
            'confidence_score': confidence_score,
            'processing_time_seconds': processing_time_seconds
        }
        
        result = mongo.db[AIEvaluation.collection].insert_one(evaluation_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_submission(submission_id):
        """Find evaluation by submission ID."""
        return mongo.db[AIEvaluation.collection].find_one({'submission_id': ObjectId(submission_id)})
    
    @staticmethod
    def find_by_competition(competition_id):
        """Find all evaluations for a competition, sorted by score."""
        evaluations = list(mongo.db[AIEvaluation.collection]
                          .find({'competition_id': ObjectId(competition_id)})
                          .sort('overall_score', -1))
        return evaluations


class CompetitionWinner:
    """Competition winner model."""
    
    collection = 'competition_winners'
    
    @staticmethod
    def create(competition_id, submission_id, author_id, rank_position,
               final_score, prize_awarded, winner_feedback):
        """Create a new competition winner."""
        winner_data = {
            'competition_id': ObjectId(competition_id),
            'submission_id': ObjectId(submission_id),
            'author_id': ObjectId(author_id),
            'rank_position': rank_position,
            'final_score': final_score,
            'prize_awarded': prize_awarded,
            'winner_feedback': winner_feedback,
            'announced_at': datetime.utcnow(),
            'notification_sent': False
        }
        
        result = mongo.db[CompetitionWinner.collection].insert_one(winner_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_competition(competition_id):
        """Find all winners for a competition, ordered by rank."""
        winners = list(mongo.db[CompetitionWinner.collection]
                      .find({'competition_id': ObjectId(competition_id)})
                      .sort('rank_position', 1))
        return winners
    
    @staticmethod
    def find_by_author(author_id):
        """Find all wins by an author."""
        winners = list(mongo.db[CompetitionWinner.collection]
                      .find({'author_id': ObjectId(author_id)})
                      .sort('announced_at', -1))
        return winners
    
    @staticmethod
    def mark_notification_sent(winner_id):
        """Mark that winner notification has been sent."""
        mongo.db[CompetitionWinner.collection].update_one(
            {'_id': ObjectId(winner_id)},
            {'$set': {'notification_sent': True}}
        )


class PressKit:
    """Press kit model for authors."""
    
    collection = 'press_kits'
    
    @staticmethod
    def create(author_id, bio, headshot_url, book_covers, 
               media_mentions=None, awards=None, contact_info=None):
        """Create a new press kit."""
        press_kit_data = {
            'author_id': ObjectId(author_id),
            'bio': bio,
            'headshot_url': headshot_url,
            'book_covers': book_covers,  # List of URLs
            'media_mentions': media_mentions or [],
            'awards': awards or [],
            'contact_info': contact_info or {},
            'download_count': 0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = mongo.db[PressKit.collection].insert_one(press_kit_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_author(author_id):
        """Find press kit by author."""
        return mongo.db[PressKit.collection].find_one({'author_id': ObjectId(author_id)})
    
    @staticmethod
    def update(press_kit_id, updates):
        """Update press kit."""
        updates['updated_at'] = datetime.utcnow()
        mongo.db[PressKit.collection].update_one(
            {'_id': ObjectId(press_kit_id)},
            {'$set': updates}
        )
    
    @staticmethod
    def increment_downloads(press_kit_id):
        """Increment download count."""
        mongo.db[PressKit.collection].update_one(
            {'_id': ObjectId(press_kit_id)},
            {'$inc': {'download_count': 1}}
        )


class NewsletterSubscriber:
    """Newsletter subscriber model."""
    
    collection = 'newsletter_subscribers'
    
    @staticmethod
    def create(author_id, email, subscriber_name=''):
        """Create a new subscriber."""
        subscriber_data = {
            'author_id': ObjectId(author_id),
            'email': email.lower(),
            'subscriber_name': subscriber_name,
            'subscribed_at': datetime.utcnow(),
            'is_active': True
        }
        
        result = mongo.db[NewsletterSubscriber.collection].insert_one(subscriber_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_author(author_id, active_only=True):
        """Find subscribers by author."""
        query = {'author_id': ObjectId(author_id)}
        if active_only:
            query['is_active'] = True
        return list(mongo.db[NewsletterSubscriber.collection].find(query))
    
    @staticmethod
    def unsubscribe(subscriber_id):
        """Unsubscribe a user."""
        mongo.db[NewsletterSubscriber.collection].update_one(
            {'_id': ObjectId(subscriber_id)},
            {'$set': {'is_active': False}}
        )


class BookGiveaway:
    """Book giveaway model."""
    
    collection = 'book_giveaways'
    
    @staticmethod
    def create(author_id, book_id, title, description, 
               start_date, end_date, num_winners=1, entry_requirements=None):
        """Create a new book giveaway."""
        giveaway_data = {
            'author_id': ObjectId(author_id),
            'book_id': ObjectId(book_id),
            'title': title,
            'description': description,
            'start_date': start_date,
            'end_date': end_date,
            'num_winners': num_winners,
            'entry_requirements': entry_requirements or [],
            'status': 'active',  # active, ended, cancelled
            'entry_count': 0,
            'winners_selected': False,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = mongo.db[BookGiveaway.collection].insert_one(giveaway_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_id(giveaway_id):
        """Find giveaway by ID."""
        try:
            return mongo.db[BookGiveaway.collection].find_one({'_id': ObjectId(giveaway_id)})
        except:
            return None
    
    @staticmethod
    def find_active_giveaways(skip=0, limit=20):
        """Find all active giveaways."""
        return list(mongo.db[BookGiveaway.collection]
                   .find({'status': 'active', 'end_date': {'$gt': datetime.utcnow()}})
                   .skip(skip).limit(limit)
                   .sort('created_at', -1))
    
    @staticmethod
    def find_by_author(author_id):
        """Find giveaways by author."""
        return list(mongo.db[BookGiveaway.collection]
                   .find({'author_id': ObjectId(author_id)})
                   .sort('created_at', -1))


class GiveawayEntry:
    """Giveaway entry model."""
    
    collection = 'giveaway_entries'
    
    @staticmethod
    def create(giveaway_id, user_id, entry_data=None):
        """Create a new giveaway entry."""
        entry = {
            'giveaway_id': ObjectId(giveaway_id),
            'user_id': ObjectId(user_id),
            'entry_data': entry_data or {},
            'is_winner': False,
            'entered_at': datetime.utcnow()
        }
        
        result = mongo.db[GiveawayEntry.collection].insert_one(entry)
        return result.inserted_id
    
    @staticmethod
    def find_by_giveaway(giveaway_id):
        """Find all entries for a giveaway."""
        return list(mongo.db[GiveawayEntry.collection].find({'giveaway_id': ObjectId(giveaway_id)}))
    
    @staticmethod
    def check_entered(giveaway_id, user_id):
        """Check if user has entered a giveaway."""
        return mongo.db[GiveawayEntry.collection].find_one({
            'giveaway_id': ObjectId(giveaway_id),
            'user_id': ObjectId(user_id)
        }) is not None


class TitleTest:
    """Title testing/polling model."""
    
    collection = 'title_tests'
    
    @staticmethod
    def create(author_id, book_genre, title_options, description=''):
        """Create a new title test."""
        test_data = {
            'author_id': ObjectId(author_id),
            'book_genre': book_genre,
            'title_options': [{'title': t, 'votes': 0} for t in title_options],
            'description': description,
            'status': 'active',  # active, closed
            'total_votes': 0,
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow().replace(hour=23, minute=59, second=59)  # Expires end of day
        }
        
        result = mongo.db[TitleTest.collection].insert_one(test_data)
        return result.inserted_id
    
    @staticmethod
    def find_by_id(test_id):
        """Find title test by ID."""
        try:
            return mongo.db[TitleTest.collection].find_one({'_id': ObjectId(test_id)})
        except:
            return None
    
    @staticmethod
    def find_active_tests(skip=0, limit=20):
        """Find active title tests."""
        return list(mongo.db[TitleTest.collection]
                   .find({'status': 'active', 'expires_at': {'$gt': datetime.utcnow()}})
                   .skip(skip).limit(limit)
                   .sort('created_at', -1))
    
    @staticmethod
    def vote(test_id, title_index):
        """Record a vote for a title."""
        mongo.db[TitleTest.collection].update_one(
            {'_id': ObjectId(test_id)},
            {
                '$inc': {
                    f'title_options.{title_index}.votes': 1,
                    'total_votes': 1
                }
            }
        )
    
    @staticmethod
    def check_duplicate_titles(title):
        """Check if title exists in the database."""
        from app.models import Book
        similar_books = list(mongo.db[Book.collection].find({
            'title': {'$regex': title, '$options': 'i'}
        }).limit(10))
        return similar_books


class CoverFeedback:
    """Cover design feedback model."""
    
    collection = 'cover_feedback'
    
    @staticmethod
    def create(author_id, cover_url, book_genre, description=''):
        """Create a new cover feedback request."""
        feedback_data = {
            'author_id': ObjectId(author_id),
            'cover_url': cover_url,
            'book_genre': book_genre,
            'description': description,
            'feedback_items': [],
            'average_rating': 0,
            'total_ratings': 0,
            'created_at': datetime.utcnow()
        }
        
        result = mongo.db[CoverFeedback.collection].insert_one(feedback_data)
        return result.inserted_id
    
    @staticmethod
    def add_feedback(feedback_id, user_id, rating, comment=''):
        """Add feedback to a cover."""
        feedback_item = {
            'user_id': ObjectId(user_id),
            'rating': rating,
            'comment': comment,
            'created_at': datetime.utcnow()
        }
        
        result = mongo.db[CoverFeedback.collection].find_one({'_id': ObjectId(feedback_id)})
        if result:
            new_total = result['total_ratings'] + 1
            new_avg = ((result['average_rating'] * result['total_ratings']) + rating) / new_total
            
            mongo.db[CoverFeedback.collection].update_one(
                {'_id': ObjectId(feedback_id)},
                {
                    '$push': {'feedback_items': feedback_item},
                    '$set': {
                        'average_rating': new_avg,
                        'total_ratings': new_total
                    }
                }
            )
    
    @staticmethod
    def find_recent(skip=0, limit=20):
        """Find recent cover feedback requests."""
        return list(mongo.db[CoverFeedback.collection]
                   .find({})
                   .skip(skip).limit(limit)
                   .sort('created_at', -1))


class WordCountTracker:
    """Word count tracking model."""
    
    collection = 'word_count_tracker'
    
    @staticmethod
    def create(author_id, book_title, target_word_count, is_public=True):
        """Create a new word count tracker."""
        tracker_data = {
            'author_id': ObjectId(author_id),
            'book_title': book_title,
            'target_word_count': target_word_count,
            'current_word_count': 0,
            'is_public': is_public,
            'entries': [],  # Daily updates
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = mongo.db[WordCountTracker.collection].insert_one(tracker_data)
        return result.inserted_id
    
    @staticmethod
    def add_entry(tracker_id, word_count, notes=''):
        """Add a word count entry."""
        entry = {
            'word_count': word_count,
            'notes': notes,
            'date': datetime.utcnow()
        }
        
        mongo.db[WordCountTracker.collection].update_one(
            {'_id': ObjectId(tracker_id)},
            {
                '$push': {'entries': entry},
                '$set': {
                    'current_word_count': word_count,
                    'updated_at': datetime.utcnow()
                }
            }
        )
    
    @staticmethod
    def find_by_author(author_id):
        """Find trackers by author."""
        return list(mongo.db[WordCountTracker.collection]
                   .find({'author_id': ObjectId(author_id)})
                   .sort('updated_at', -1))
    
    @staticmethod
    def find_public_trackers(skip=0, limit=20):
        """Find public word count trackers."""
        return list(mongo.db[WordCountTracker.collection]
                   .find({'is_public': True})
                   .skip(skip).limit(limit)
                   .sort('updated_at', -1))


class WritingPrompt:
    """Writing prompt model."""
    
    collection = 'writing_prompts'
    
    @staticmethod
    def create(prompt_text, genre, difficulty='medium'):
        """Create a new writing prompt."""
        prompt_data = {
            'prompt_text': prompt_text,
            'genre': genre,
            'difficulty': difficulty,  # easy, medium, hard
            'use_count': 0,
            'created_at': datetime.utcnow()
        }
        
        result = mongo.db[WritingPrompt.collection].insert_one(prompt_data)
        return result.inserted_id
    
    @staticmethod
    def get_random_prompt(genre=None):
        """Get a random writing prompt."""
        pipeline = []
        if genre:
            pipeline.append({'$match': {'genre': genre}})
        pipeline.append({'$sample': {'size': 1}})
        
        prompts = list(mongo.db[WritingPrompt.collection].aggregate(pipeline))
        return prompts[0] if prompts else None
    
    @staticmethod
    def increment_usage(prompt_id):
        """Increment prompt usage count."""
        mongo.db[WritingPrompt.collection].update_one(
            {'_id': ObjectId(prompt_id)},
            {'$inc': {'use_count': 1}}
        )


class SocialShare:
    """Social media share tracking model."""
    
    collection = 'social_shares'
    
    @staticmethod
    def create(book_id, author_id, platform, share_url):
        """Record a social share."""
        share_data = {
            'book_id': ObjectId(book_id),
            'author_id': ObjectId(author_id),
            'platform': platform,  # facebook, twitter, instagram, whatsapp
            'share_url': share_url,
            'created_at': datetime.utcnow()
        }
        
        result = mongo.db[SocialShare.collection].insert_one(share_data)
        return result.inserted_id
    
    @staticmethod
    def get_share_count(book_id):
        """Get total share count for a book."""
        return mongo.db[SocialShare.collection].count_documents({'book_id': ObjectId(book_id)})
    
    @staticmethod
    def get_shares_by_platform(book_id):
        """Get share counts grouped by platform."""
        pipeline = [
            {'$match': {'book_id': ObjectId(book_id)}},
            {'$group': {
                '_id': '$platform',
                'count': {'$sum': 1}
            }}
        ]
        return list(mongo.db[SocialShare.collection].aggregate(pipeline))
