"""Create admin user directly in MongoDB Atlas."""
import os
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from datetime import datetime

# Use your Atlas connection string
ATLAS_URI = input("Enter your MongoDB Atlas URI: ")

print(f"\nConnecting to MongoDB Atlas...")

try:
    client = MongoClient(ATLAS_URI, serverSelectionTimeoutMS=5000)
    db = client['inklaunch']
    
    # Test connection
    client.admin.command('ping')
    print("✅ Connected successfully!")
    
    # Check if user already exists
    existing = db.users.find_one({'email': 'ashchugh@gmail.com'})
    if existing:
        print("⚠️  User ashchugh@gmail.com already exists!")
        update = input("Do you want to update the password? (yes/no): ")
        if update.lower() != 'yes':
            print("Aborted.")
            exit(0)
    
    # Create password hash
    bcrypt = Bcrypt()
    password_hash = bcrypt.generate_password_hash('Ashna@2000!').decode('utf-8')
    
    # Create user data
    user_data = {
        'user_id': 'INK000001',
        'username': 'ashchugh',
        'full_name': 'Ashish Chugh',
        'email': 'ashchugh@gmail.com',
        'password_hash': password_hash,
        'bio': 'Platform Administrator',
        'role': 'admin',
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'points': 0,
        'badges': [],
        'profile_photo': None,
        'total_books_reviewed': 0,
        'total_reviews_received': 0,
        'avg_rating_given': 0.0,
        'avg_rating_received': 0.0
    }
    
    if existing:
        # Update existing user
        db.users.update_one(
            {'email': 'ashchugh@gmail.com'},
            {'$set': {
                'password_hash': password_hash,
                'role': 'admin',
                'updated_at': datetime.utcnow()
            }}
        )
        print("✅ User updated successfully!")
    else:
        # Insert new user
        result = db.users.insert_one(user_data)
        print(f"✅ Admin user created successfully!")
        print(f"   User ID: {result.inserted_id}")
    
    print("\n📧 Email: ashchugh@gmail.com")
    print("🔑 Password: Ashna@2000!")
    print("\nYou can now login to your app!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure:")
    print("1. The connection string is correct")
    print("2. Network access allows connections (0.0.0.0/0)")
    print("3. Database user has read/write permissions")
