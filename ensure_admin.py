"""Ensure ashchugh@gmail.com has admin role."""
from app import create_app, mongo

app = create_app()
with app.app_context():
    # Update user to ensure admin role
    result = mongo.db.users.update_one(
        {'email': 'ashchugh@gmail.com'},
        {'$set': {'role': 'admin', 'is_active': True}}
    )
    
    if result.matched_count > 0:
        print(f"✓ Updated ashchugh@gmail.com to admin role")
        
        # Verify
        user = mongo.db.users.find_one({'email': 'ashchugh@gmail.com'})
        print(f"  Email: {user['email']}")
        print(f"  Role: {user['role']}")
        print(f"  Active: {user['is_active']}")
    else:
        print("✗ User not found")
