"""
Initialize existing users with badge and competition tracking fields
"""

from app import create_app, mongo

app = create_app()

with app.app_context():
    # Update all existing users to have the new fields
    result = mongo.db['users'].update_many(
        {
            '$or': [
                {'badges': {'$exists': False}},
                {'competition_stats': {'$exists': False}},
                {'featured_until': {'$exists': False}},
                {'premium_until': {'$exists': False}}
            ]
        },
        {
            '$set': {
                'badges': [],
                'achievements': [],
                'competition_stats': {
                    'total_entered': 0,
                    'total_wins': 0,
                    'total_finalist': 0,
                    'total_submissions': 0,
                    'best_rank': None
                },
                'featured_until': None,
                'premium_until': None
            }
        }
    )
    
    print(f"✅ Updated {result.modified_count} users with new badge/achievement fields")
    print("✅ All users now have:")
    print("   - Badge tracking system")
    print("   - Competition statistics")
    print("   - Featured author status tracking")
    print("   - Premium membership tracking")
