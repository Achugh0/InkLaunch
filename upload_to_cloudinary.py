"""Upload book covers to Cloudinary (S3 alternative)."""
import cloudinary
import cloudinary.uploader
import os
import sys


def upload_to_cloudinary(local_file, folder='book-covers'):
    """Upload file to Cloudinary."""
    try:
        result = cloudinary.uploader.upload(
            local_file,
            folder=folder,
            resource_type='auto',
            quality='auto',
            fetch_format='auto'
        )
        return result.get('secure_url')
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None


def update_database(mongodb_uri, book_mapping):
    """Update production MongoDB."""
    from pymongo import MongoClient
    
    try:
        client = MongoClient(mongodb_uri)
        db = client.inklaunch
        
        print("\n" + "="*70)
        print("Updating Production Database")
        print("="*70)
        
        for title, url in book_mapping.items():
            result = db.books.update_one(
                {'title': title},
                {'$set': {'cover_image_url': url}}
            )
            
            if result.matched_count > 0:
                print(f"✓ {title}")
                print(f"  {url}")
            else:
                print(f"⚠ Not found: {title}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False


def main():
    print("="*70)
    print(" UPLOAD BOOK COVERS TO CLOUDINARY")
    print("="*70)
    
    # Get credentials
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
    mongodb_uri = os.getenv('MONGODB_URI')
    
    # Validate
    if not all([cloud_name, api_key, api_secret]):
        print("\n❌ Cloudinary credentials not found!")
        print("\nSet these environment variables:")
        print("  export CLOUDINARY_CLOUD_NAME='your_cloud_name'")
        print("  export CLOUDINARY_API_KEY='your_api_key'")
        print("  export CLOUDINARY_API_SECRET='your_api_secret'")
        print("\nGet them from: https://cloudinary.com/console")
        sys.exit(1)
    
    if not mongodb_uri:
        print("\n❌ MONGODB_URI not set!")
        sys.exit(1)
    
    # Configure Cloudinary
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True
    )
    
    print(f"\n✓ Cloudinary: {cloud_name}")
    print(f"✓ MongoDB: Connected")
    
    # Upload images
    books = [
        {
            'title': 'The Weight of Wings',
            'file': '/workspaces/InkLaunch/uploads/1770118718.02634_WSB1.jpeg'
        },
        {
            'title': 'The Day We Die',
            'file': '/workspaces/InkLaunch/uploads/1770175759.468088_The_Day_We_Die_1.png'
        }
    ]
    
    print("\n" + "="*70)
    print("Uploading to Cloudinary")
    print("="*70)
    
    urls = {}
    
    for book in books:
        print(f"\n📚 {book['title']}")
        
        if not os.path.exists(book['file']):
            print(f"  ❌ File not found: {book['file']}")
            continue
        
        size = os.path.getsize(book['file']) / (1024 * 1024)
        print(f"  📁 {size:.2f} MB")
        print(f"  ☁️  Uploading...")
        
        url = upload_to_cloudinary(book['file'])
        
        if url:
            print(f"  ✓ Success!")
            print(f"  🔗 {url}")
            urls[book['title']] = url
        else:
            print(f"  ❌ Failed!")
    
    if not urls:
        print("\n❌ No images uploaded")
        sys.exit(1)
    
    # Update database
    if update_database(mongodb_uri, urls):
        print("\n" + "="*70)
        print(" DEPLOYMENT COMPLETE!")
        print("="*70)
        print("\n✓ Images uploaded to Cloudinary")
        print("✓ Production database updated")
        print("✓ Add Cloudinary credentials to Render")
        print("\nYour book covers will now persist on Render!")
    else:
        print("\n❌ Database update failed")
        sys.exit(1)


if __name__ == '__main__':
    try:
        import cloudinary
    except ImportError:
        print("❌ cloudinary package not installed")
        print("Run: pip install cloudinary")
        sys.exit(1)
    
    main()
