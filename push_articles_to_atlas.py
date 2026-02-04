"""
Push Articles to MongoDB Atlas

Usage:
    python3 push_articles_to_atlas.py

You'll be prompted for your MongoDB Atlas URI.
Articles will be imported from articles_export.json

Note: This will NOT delete existing articles. It only adds new ones
      based on unique titles.
"""
from pymongo import MongoClient
import json
import getpass

def push_articles():
    """Push articles to MongoDB Atlas."""
    # Load articles from JSON
    try:
        with open('articles_export.json', 'r', encoding='utf-8') as f:
            articles_data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: articles_export.json not found!")
        print("Run: python3 export_articles.py first")
        return
    
    print(f"📚 Loaded {len(articles_data)} articles from articles_export.json\n")
    
    # Get MongoDB Atlas URI
    print("Please enter your MongoDB Atlas URI:")
    print("Format: mongodb+srv://username:password@cluster.mongodb.net/inklaunch")
    atlas_uri = input("URI: ").strip()
    
    if not atlas_uri:
        print("❌ No URI provided. Exiting.")
        return
    
    try:
        # Connect to Atlas
        print("\n🔌 Connecting to MongoDB Atlas...")
        client = MongoClient(atlas_uri, serverSelectionTimeoutMS=5000)
        db = client.inklaunch
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected successfully!\n")
        
        # Import articles
        added = 0
        skipped = 0
        
        print("📝 Importing articles:")
        print("=" * 60)
        
        for article in articles_data:
            # Remove _id to let MongoDB generate new ones
            article.pop('_id', None)
            
            # Check if article already exists
            existing = db.articles.find_one({'title': article['title']})
            if existing:
                print(f"  ⏭️  Skipping: {article['title']}")
                skipped += 1
                continue
            
            # Insert article
            result = db.articles.insert_one(article)
            print(f"  ✅ Added: {article['title']}")
            added += 1
        
        print("=" * 60)
        print(f"\n✨ Import complete!")
        print(f"  - Added: {added} articles")
        print(f"  - Skipped: {skipped} articles (already exist)")
        print(f"  - Total in export: {len(articles_data)} articles")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Check your MongoDB Atlas URI is correct")
        print("  2. Verify your IP address is whitelisted in Atlas")
        print("  3. Ensure your database user has read/write permissions")

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  Push Articles to MongoDB Atlas")
    print("=" * 60 + "\n")
    push_articles()
