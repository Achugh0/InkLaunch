"""Seed production database with sample books."""
from pymongo import MongoClient
from datetime import datetime
import os

# Sample book data with Cloudinary URLs
SAMPLE_BOOKS = [
    {
        'title': 'The Weight of Wings',
        'subtitle': 'When silence is mistaken for strength, both become fatal',
        'description': 'A profound exploration of psychological fiction that delves into the human condition. When silence becomes a weapon rather than a shield, the consequences ripple through lives in unexpected ways. This gripping narrative examines the fine line between strength and vulnerability, challenging readers to confront their own perceptions of courage and communication. Through richly developed characters and atmospheric prose, this story unveils the weight we all carry and the wings we need to find freedom.',
        'genre': 'Psychological Fiction',
        'author_name': 'Ashish Chugh',
        'page_count': 320,
        'cover_url': 'https://res.cloudinary.com/dw74ayc1s/image/upload/v1770276831/book-covers/zvbo5bxgoh1hrkicvmyx.jpg'
    },
    {
        'title': 'Ruins of Breath',
        'subtitle': 'The most suffocating prison is the one you build yourself',
        'description': 'A haunting psychological thriller that explores the prisons we create in our own minds. When reality becomes indistinguishable from the barriers we construct, survival means confronting the darkest corners of consciousness. This masterfully crafted narrative weaves together themes of isolation, self-deception, and the desperate human need for connection. Through atmospheric tension and penetrating character study, readers are drawn into a world where the greatest escape is from oneself.',
        'genre': 'Psychological Fiction',
        'author_name': 'Ashish Chugh',
        'page_count': 285,
        'cover_url': 'https://placehold.co/400x600/4ECDC4/FFFFFF?text=Ruins%20of%20Breath'
    },
    {
        'title': 'The Day the Door Stayed Shut',
        'subtitle': '',
        'description': 'A minimalist exploration of isolation and choice. Sometimes the most significant moments are defined not by what happens, but by what doesn\'t. This contemplative work examines a single day when a door that should have opened remained closed, and the cascading consequences that followed. Through sparse prose and powerful imagery, the narrative builds tension from stillness, finding profound meaning in absence and the spaces between action.',
        'genre': 'Fiction',
        'author_name': 'Ashish Chugh',
        'page_count': 240,
        'cover_url': 'https://placehold.co/400x600/FFE66D/000000?text=The%20Day%20the%20Door%20Stayed%20Shut'
    },
    {
        'title': 'The Day We Die',
        'subtitle': '',
        'description': 'An existential journey through time, mortality, and the moments that define us. Set against the backdrop of urban isolation, this philosophical narrative explores what it means to truly live when confronted with inevitable endings. Through interconnected stories and profound observations, the book challenges readers to examine their own relationship with time, purpose, and the legacy we leave behind. A meditation on mortality that paradoxically celebrates life.',
        'genre': 'Fiction',
        'author_name': 'Ashish Chugh',
        'page_count': 310,
        'cover_url': 'https://res.cloudinary.com/dw74ayc1s/image/upload/v1770276834/book-covers/ur5kafvmbhcadk5lhhld.jpg'
    },
    {
        'title': 'The Art of Failing Upwards',
        'subtitle': 'A Guide to What NOT to Do in Management',
        'description': 'A refreshingly honest and hilariously insightful exploration of management dysfunction. Through witty observations and painfully accurate corporate archetypes, this book takes readers on a safari through the world of the gloriously flawed boss. From the Gaslighter who rewrites reality to the Politician who values optics over outcomes, each chapter reveals the deep dysfunction that drives flawed work environments. This is more than complaints—it\'s wisdom disguised as comedy, offering guidance for every employee who has survived a bad boss and every manager brave enough to see their reflection.',
        'genre': 'Corporate Satire',
        'author_name': 'Ashish Chugh',
        'page_count': 275,
        'cover_url': 'https://placehold.co/400x600/FF8B94/FFFFFF?text=The%20Art%20of%20Failing%20Upwards'
    },
    {
        'title': 'Performance Appraisals: R for Reality',
        'subtitle': 'Contains scenes of emotional manipulation, budgetary disappointment, and career nudity',
        'description': 'A brutally honest satire of the corporate performance review process. Rated R for Reality, this unflinching look at workplace assessment reveals the uncomfortable truths behind annual reviews, promotion politics, and the theater of professional development. Through razor-sharp wit and uncomfortable accuracy, this book exposes the gap between corporate ideals and everyday experience. Essential reading for anyone who has ever sat through a performance review wondering if they\'re part of a genuine evaluation or an elaborate charade.',
        'genre': 'Corporate Satire',
        'author_name': 'Ashish Chugh',
        'page_count': 195,
        'cover_url': 'https://placehold.co/400x600/95E1D3/000000?text=Performance%20Appraisals'
    }
]

def seed_production():
    """Seed production database."""
    mongodb_uri = os.environ.get('MONGODB_URI')
    if not mongodb_uri:
        print("❌ Error: MONGODB_URI environment variable not set")
        return
    
    client = MongoClient(mongodb_uri)
    db = client.get_database()
    
    print("=" * 70)
    print(" SEEDING PRODUCTION DATABASE")
    print("=" * 70)
    print()
    
    # Get or create author
    author = db.users.find_one({'email': 'ashchugh@gmail.com'})
    if not author:
        print("❌ Error: Author account not found. Create admin user first.")
        return
    
    author_id = author['_id']
    print(f"✓ Author: {author.get('full_name', 'Unknown')}")
    print()
    
    # Add books
    added = 0
    updated = 0
    
    for book_data in SAMPLE_BOOKS:
        existing = db.books.find_one({
            'title': book_data['title'],
            'user_id': author_id
        })
        
        if existing:
            # Update cover_url if it's different
            if existing.get('cover_url') != book_data['cover_url']:
                db.books.update_one(
                    {'_id': existing['_id']},
                    {'$set': {'cover_url': book_data['cover_url']}}
                )
                print(f"📚 Updated: {book_data['title']}")
                print(f"   🔗 {book_data['cover_url'][:60]}...")
                updated += 1
            else:
                print(f"✓ Exists: {book_data['title']}")
        else:
            book_doc = {
                'title': book_data['title'],
                'subtitle': book_data.get('subtitle', ''),
                'description': book_data['description'],
                'genre': book_data['genre'],
                'page_count': book_data['page_count'],
                'cover_url': book_data['cover_url'],
                'user_id': author_id,
                'status': 'published',
                'publication_date': datetime.utcnow(),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'views': 0,
                'total_rating': 0,
                'number_of_reviews': 0,
                'average_rating': 0.0
            }
            
            db.books.insert_one(book_doc)
            print(f"📚 Added: {book_data['title']}")
            print(f"   🔗 {book_data['cover_url'][:60]}...")
            added += 1
        print()
    
    print("=" * 70)
    print(f"✓ Added: {added} books")
    print(f"✓ Updated: {updated} books")
    print(f"✓ Total books: {db.books.count_documents({'user_id': author_id})}")
    print("=" * 70)

if __name__ == '__main__':
    seed_production()
