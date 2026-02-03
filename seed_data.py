"""Seed database with sample books."""
from app import create_app, mongo
from app.models import User, Book
from datetime import datetime
import os

# Sample book data based on the covers provided
SAMPLE_BOOKS = [
    {
        'title': 'The Weight of Wings',
        'subtitle': 'When silence is mistaken for strength, both become fatal',
        'description': 'A profound exploration of psychological fiction that delves into the human condition. When silence becomes a weapon rather than a shield, the consequences ripple through lives in unexpected ways. This gripping narrative examines the fine line between strength and vulnerability, challenging readers to confront their own perceptions of courage and communication. Through richly developed characters and atmospheric prose, this story unveils the weight we all carry and the wings we need to find freedom.',
        'genre': 'Psychological Fiction',
        'author_name': 'Ashish Chugh',
        'page_count': 320,
        'cover_url': 'https://via.placeholder.com/300x450/1a1f3a/d4af37?text=The+Weight+of+Wings'
    },
    {
        'title': 'Ruins of Breath',
        'subtitle': 'The most suffocating prison is the one you build yourself',
        'description': 'A haunting psychological thriller that explores the prisons we create in our own minds. When reality becomes indistinguishable from the barriers we construct, survival means confronting the darkest corners of consciousness. This masterfully crafted narrative weaves together themes of isolation, self-deception, and the desperate human need for connection. Through atmospheric tension and penetrating character study, readers are drawn into a world where the greatest escape is from oneself.',
        'genre': 'Psychological Fiction',
        'author_name': 'Ashish Chugh',
        'page_count': 285,
        'cover_url': 'https://via.placeholder.com/300x450/7d9298/000000?text=Ruins+of+Breath'
    },
    {
        'title': 'The Day the Door Stayed Shut',
        'subtitle': '',
        'description': 'A minimalist exploration of isolation and choice. Sometimes the most significant moments are defined not by what happens, but by what doesn\'t. This contemplative work examines a single day when a door that should have opened remained closed, and the cascading consequences that followed. Through sparse prose and powerful imagery, the narrative builds tension from stillness, finding profound meaning in absence and the spaces between action.',
        'genre': 'Fiction',
        'author_name': 'Ashish Chugh',
        'page_count': 240,
        'cover_url': 'https://via.placeholder.com/300x450/333333/d4af37?text=The+Day+the+Door+Stayed+Shut'
    },
    {
        'title': 'The Day We Die',
        'subtitle': '',
        'description': 'An existential journey through time, mortality, and the moments that define us. Set against the backdrop of urban isolation, this philosophical narrative explores what it means to truly live when confronted with inevitable endings. Through interconnected stories and profound observations, the book challenges readers to examine their own relationship with time, purpose, and the legacy we leave behind. A meditation on mortality that paradoxically celebrates life.',
        'genre': 'Fiction',
        'author_name': 'Ashish Chugh',
        'page_count': 310,
        'cover_url': 'https://via.placeholder.com/300x450/4a7c8c/000000?text=The+Day+We+Die'
    },
    {
        'title': 'The Art of Failing Upwards',
        'subtitle': 'A Guide to What NOT to Do in Management',
        'description': 'A refreshingly honest and hilariously insightful exploration of management dysfunction. Through witty observations and painfully accurate corporate archetypes, this book takes readers on a safari through the world of the gloriously flawed boss. From the Gaslighter who rewrites reality to the Politician who values optics over outcomes, each chapter reveals the deep dysfunction that drives flawed work environments. This is more than complaints—it\'s wisdom disguised as comedy, offering guidance for every employee who has survived a bad boss and every manager brave enough to see their reflection.',
        'genre': 'Corporate Satire',
        'author_name': 'Ashish Chugh',
        'page_count': 275,
        'cover_url': 'https://via.placeholder.com/300x450/e8d5ba/d62828?text=The+Art+of+Failing+Upwards'
    },
    {
        'title': 'Performance Appraisals: R for Reality',
        'subtitle': 'Contains scenes of emotional manipulation, budgetary disappointment, and career nudity',
        'description': 'A brutally honest satire of the corporate performance review process. Rated R for Reality, this unflinching look at workplace assessment reveals the uncomfortable truths behind annual reviews, promotion politics, and the theater of professional development. Through razor-sharp wit and uncomfortable accuracy, this book exposes the gap between corporate ideals and everyday experience. Essential reading for anyone who has ever sat through a performance review wondering if they\'re part of a genuine evaluation or an elaborate charade.',
        'genre': 'Corporate Satire',
        'author_name': 'Ashish Chugh',
        'page_count': 195,
        'cover_url': 'https://via.placeholder.com/300x450/e8d5ba/8b0000?text=Performance+Appraisals'
    }
]

def seed_database():
    """Seed the database with sample books."""
    app = create_app()
    
    with app.app_context():
        # Create author account if doesn't exist
        author_email = 'ashchugh@gmail.com'
        author = User.find_by_email(author_email)
        
        if not author:
            print(f"Creating author account: {author_email}")
            author_id = User.create(
                email=author_email,
                password='InkLaunch2026!',
                full_name='Ashish Chugh',
                bio='Author of psychological fiction and corporate satire. Exploring the human condition through narrative and the workplace through wit.',
                role='admin'
            )
            author = User.find_by_id(str(author_id))
        else:
            print(f"Author account already exists: {author_email}")
        
        # Add sample books
        for book_data in SAMPLE_BOOKS:
            # Check if book already exists
            existing = mongo.db.books.find_one({
                'title': book_data['title'],
                'user_id': author['_id']
            })
            
            if existing:
                print(f"Book already exists: {book_data['title']}")
                continue
            
            print(f"Adding book: {book_data['title']}")
            
            book_create_data = {
                'title': book_data['title'],
                'subtitle': book_data['subtitle'],
                'description': book_data['description'],
                'genre': book_data['genre'],
                'page_count': book_data['page_count'],
                'cover_image_url': book_data['cover_url'],
                'language': 'English',
                'publication_date': datetime.utcnow(),
                'status': 'active'
            }
            
            Book.create(str(author['_id']), book_create_data)
        
        print("\n✓ Database seeding completed!")
        print(f"✓ Total books in repository: {mongo.db.books.count_documents({})}")

if __name__ == '__main__':
    seed_database()
