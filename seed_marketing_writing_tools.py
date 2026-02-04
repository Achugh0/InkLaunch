"""Seed data for marketing and writing tools."""
from app import create_app, mongo
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Add sample writing prompts
    prompts = [
        {
            'prompt_text': 'A character discovers they can see 24 hours into the future, but only for strangers.',
            'genre': 'Science Fiction',
            'difficulty': 'medium',
            'use_count': 0,
            'created_at': datetime.utcnow()
        },
        {
            'prompt_text': 'Two rival authors fall in love while competing for the same book award.',
            'genre': 'Romance',
            'difficulty': 'easy',
            'use_count': 0,
            'created_at': datetime.utcnow()
        },
        {
            'prompt_text': 'A detective realizes the crime scene matches a chapter from their unpublished manuscript.',
            'genre': 'Mystery',
            'difficulty': 'hard',
            'use_count': 0,
            'created_at': datetime.utcnow()
        },
        {
            'prompt_text': 'In a world where magic is powered by storytelling, the greatest wizards are novelists.',
            'genre': 'Fantasy',
            'difficulty': 'medium',
            'use_count': 0,
            'created_at': datetime.utcnow()
        },
        {
            'prompt_text': 'A character wakes up to find everyone believes they wrote a bestselling book they\'ve never heard of.',
            'genre': 'Thriller',
            'difficulty': 'medium',
            'use_count': 0,
            'created_at': datetime.utcnow()
        },
        {
            'prompt_text': 'The last librarian on Earth must decide which 100 books to save from destruction.',
            'genre': 'Science Fiction',
            'difficulty': 'hard',
            'use_count': 0,
            'created_at': datetime.utcnow()
        },
        {
            'prompt_text': 'A cursed bookstore where every book purchased comes true in the worst possible way.',
            'genre': 'Horror',
            'difficulty': 'medium',
            'use_count': 0,
            'created_at': datetime.utcnow()
        },
        {
            'prompt_text': 'Two pen pals from different centuries discover a way to send letters through time.',
            'genre': 'Historical',
            'difficulty': 'easy',
            'use_count': 0,
            'created_at': datetime.utcnow()
        },
        {
            'prompt_text': 'A struggling writer finds a typewriter that turns lies into truth.',
            'genre': 'Fantasy',
            'difficulty': 'medium',
            'use_count': 0,
            'created_at': datetime.utcnow()
        },
        {
            'prompt_text': 'In a city where emotions are illegal, a poet starts an underground reading revolution.',
            'genre': 'Literary Fiction',
            'difficulty': 'hard',
            'use_count': 0,
            'created_at': datetime.utcnow()
        }
    ]
    
    # Clear existing prompts
    mongo.db.writing_prompts.delete_many({})
    
    # Insert new prompts
    result = mongo.db.writing_prompts.insert_many(prompts)
    print(f"✓ Added {len(result.inserted_ids)} writing prompts")
    
    print("\n✓ Marketing and writing tools seed data added successfully!")
    print("\nNew features available:")
    print("  • Writing Prompts: /writing/writing-prompts")
    print("  • Title Tester: /writing/title-tester")
    print("  • Cover Feedback: /writing/cover-feedback")
    print("  • Word Count Tracker: /writing/word-count-tracker")
    print("  • Character Name Generator: /writing/character-name-generator")
    print("  • Manuscript Formatter: /writing/manuscript-formatter")
    print("  • Blurb Generator: /writing/blurb-generator")
    print("  • Genre Checker: /writing/genre-checker")
    print("  • Press Kit: /marketing/press-kit")
    print("  • Newsletter: /marketing/newsletter")
    print("  • Giveaways: /marketing/giveaways")
