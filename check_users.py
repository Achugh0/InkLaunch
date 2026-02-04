"""Check user count."""
from app import create_app, mongo

app = create_app()
with app.app_context():
    count = mongo.db.users.count_documents({})
    print(f"Total users in database: {count}")
    
    # Get recently created users
    recent = list(mongo.db.users.find().sort('created_at', -1).limit(10))
    print("\nRecently created users:")
    for user in recent:
        print(f"  - {user['username']} ({user['full_name']})")
