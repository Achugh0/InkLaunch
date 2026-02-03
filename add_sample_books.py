"""Add sample books for testing the homepage."""
from app import create_app, mongo
from datetime import datetime
from bson import ObjectId

app = create_app()

with app.app_context():
    # Get the first user (admin)
    user = mongo.db.users.find_one()
    
    if not user:
        print("❌ No users found. Please create a user first.")
        exit(1)
    
    user_id = user['_id']
    
    sample_books = [
        {
            'title': 'The Art of Programming',
            'subtitle': 'A Comprehensive Guide',
            'description': 'An in-depth exploration of programming principles and best practices. This book covers fundamental concepts, design patterns, and advanced techniques that every developer should know. Whether you are a beginner or an experienced programmer, this guide will help you write cleaner, more efficient code.',
            'genre': 'IT & Technology',
            'page_count': 450,
            'price': 29.99
        },
        {
            'title': 'Silicon Dreams',
            'subtitle': 'Life in a Tech Startup',
            'description': 'A gripping tale of ambition, innovation, and the human cost of chasing success in Silicon Valley. Follow the journey of a young entrepreneur as she navigates the challenges of building a startup, dealing with investors, and maintaining her sanity in the fast-paced world of technology.',
            'genre': 'Corporate Satire',
            'page_count': 320,
            'price': 19.99
        },
        {
            'title': 'Mindful Coding',
            'subtitle': 'Finding Balance in Development',
            'description': 'Discover how to maintain your mental health and productivity as a software developer. This book offers practical advice on work-life balance, stress management, and building sustainable coding practices that will serve you throughout your career. Learn from experts who have been in the trenches.',
            'genre': 'Self-Help',
            'page_count': 280,
            'price': 24.99
        },
        {
            'title': 'The Bug Collector',
            'subtitle': 'A Mystery Novel',
            'description': 'When a series of mysterious bugs appears in a major software release, senior developer Sarah Chen must unravel a conspiracy that goes deeper than anyone imagined. A thrilling mystery that combines technology, corporate intrigue, and personal drama in a page-turning narrative that will keep you guessing until the end.',
            'genre': 'Mystery',
            'page_count': 380,
            'price': 22.99
        },
        {
            'title': 'Digital Nomad',
            'subtitle': 'Working Remotely Around the World',
            'description': 'Practical guidance for developers who want to work while traveling. Learn how to find remote work opportunities, manage clients across time zones, and build a sustainable lifestyle that combines work and adventure. Includes real stories from digital nomads and actionable advice for getting started.',
            'genre': 'Business',
            'page_count': 240,
            'price': 18.99
        },
        {
            'title': 'Code & Conscience',
            'subtitle': 'Ethics in Software Engineering',
            'description': 'An exploration of the ethical dilemmas facing modern software developers. From privacy concerns to algorithmic bias, this book examines the responsibilities of engineers in shaping technology that affects billions of lives. Essential reading for anyone who wants to build technology with purpose.',
            'genre': 'Non-Fiction',
            'page_count': 350,
            'price': 27.99
        }
    ]
    
    print(f"Adding {len(sample_books)} sample books for user: {user.get('email')}...")
    
    for book_data in sample_books:
        book_doc = {
            'user_id': user_id,
            'title': book_data['title'],
            'subtitle': book_data.get('subtitle', ''),
            'description': book_data['description'],
            'cover_image_url': '',
            'genre': book_data['genre'],
            'isbn': '',
            'publication_date': datetime.utcnow(),
            'language': 'English',
            'page_count': book_data.get('page_count', 0),
            'price': book_data.get('price', 0.0),
            'amazon_link': '',
            'goodreads_link': '',
            'status': 'active',
            'views_count': 0,
            'is_award_winner': False,
            'award_badges': [],
            'competition_wins': 0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = mongo.db.books.insert_one(book_doc)
        print(f"✓ Added: {book_data['title']} (ID: {result.inserted_id})")
    
    total_books = mongo.db.books.count_documents({})
    print(f"\n✓ Success! Total books in database: {total_books}")
    print(f"Visit http://localhost:5000 to see your homepage!")
