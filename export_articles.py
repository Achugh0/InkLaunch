"""Export articles from local database and push to MongoDB Atlas."""
from app import create_app, mongo
import json
from datetime import datetime
from bson import ObjectId

def json_serializer(obj):
    """JSON serializer for objects not serializable by default."""
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)

app = create_app()

def export_articles():
    """Export all articles to JSON file."""
    with app.app_context():
        articles = list(mongo.db.articles.find())
        
        # Convert ObjectIds to strings for JSON serialization
        articles_data = []
        for article in articles:
            article_copy = article.copy()
            article_copy['_id'] = str(article_copy['_id'])
            if 'author_id' in article_copy:
                article_copy['author_id'] = str(article_copy['author_id'])
            articles_data.append(article_copy)
        
        # Save to JSON file
        with open('articles_export.json', 'w', encoding='utf-8') as f:
            json.dump(articles_data, f, indent=2, default=json_serializer)
        
        print(f"✓ Exported {len(articles_data)} articles to articles_export.json")
        return articles_data

def import_articles_to_atlas(uri=None):
    """Import articles to MongoDB Atlas."""
    if uri is None:
        print("Please provide MongoDB Atlas URI as parameter")
        return
    
    from pymongo import MongoClient
    
    # Load articles from JSON
    with open('articles_export.json', 'r', encoding='utf-8') as f:
        articles_data = json.load(f)
    
    # Connect to Atlas
    client = MongoClient(uri)
    db = client.inklaunch
    
    # Clear existing articles (optional - comment out if you want to keep existing)
    # db.articles.delete_many({})
    
    # Insert articles
    for article in articles_data:
        # Remove _id to let MongoDB generate new ones or keep existing
        article_id = article.pop('_id', None)
        
        # Check if article already exists
        existing = db.articles.find_one({'title': article['title']})
        if existing:
            print(f"  - Skipping '{article['title']}' (already exists)")
            continue
        
        # Insert article
        result = db.articles.insert_one(article)
        print(f"  + Added '{article['title']}'")
    
    client.close()
    print(f"\n✓ Import complete!")

if __name__ == '__main__':
    import sys
    
    # Export articles
    articles = export_articles()
    
    print("\nArticles exported:")
    for i, article in enumerate(articles, 1):
        print(f"  {i}. {article['title']}")
    
    # Check if Atlas URI provided
    if len(sys.argv) > 1:
        atlas_uri = sys.argv[1]
        print(f"\n{'='*60}")
        print("Importing to MongoDB Atlas...")
        print('='*60)
        import_articles_to_atlas(atlas_uri)
    else:
        print("\n" + "="*60)
        print("To import to MongoDB Atlas, run:")
        print('python3 export_articles.py "your-mongodb-atlas-uri"')
        print("="*60)
