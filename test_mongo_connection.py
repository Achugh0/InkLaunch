"""Test MongoDB connection independently."""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Get MongoDB URI from environment
mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/inklaunch')

print(f"Testing MongoDB connection...")
print(f"URI: {mongo_uri[:50]}... (truncated for security)")

try:
    # Try to connect
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    
    # Test connection
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
    
    # List databases
    dbs = client.list_database_names()
    print(f"✅ Available databases: {dbs}")
    
    # Check if inklaunch db exists
    if 'inklaunch' in dbs:
        db = client['inklaunch']
        collections = db.list_collection_names()
        print(f"✅ Collections in 'inklaunch': {collections}")
        
        # Count documents
        if 'users' in collections:
            user_count = db.users.count_documents({})
            print(f"✅ Users: {user_count}")
        if 'books' in collections:
            book_count = db.books.count_documents({})
            print(f"✅ Books: {book_count}")
    else:
        print("⚠️  'inklaunch' database doesn't exist yet - will be created on first insert")
    
except Exception as e:
    print(f"❌ MongoDB connection failed!")
    print(f"Error: {e}")
    print("\nPossible issues:")
    print("1. Check MongoDB Atlas Network Access - must allow 0.0.0.0/0 or Render IPs")
    print("2. Verify connection string has correct username/password")
    print("3. Check if MongoDB cluster is running/paused")
    print("4. Ensure database user has read/write permissions")
