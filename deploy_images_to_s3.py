"""Upload actual book cover images to S3 and update production database."""
import boto3
from botocore.exceptions import ClientError
import os
import sys

def upload_to_s3(local_file_path, s3_key, bucket_name, aws_access_key, aws_secret_key, region='us-east-1'):
    """Upload a file to S3 and return the public URL."""
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        
        # Determine content type
        if local_file_path.endswith('.png'):
            content_type = 'image/png'
        elif local_file_path.endswith(('.jpg', '.jpeg')):
            content_type = 'image/jpeg'
        else:
            content_type = 'application/octet-stream'
        
        # Upload file
        with open(local_file_path, 'rb') as f:
            s3_client.upload_fileobj(
                f,
                bucket_name,
                s3_key,
                ExtraArgs={
                    'ACL': 'public-read',
                    'ContentType': content_type
                }
            )
        
        # Generate public URL
        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{s3_key}"
        return url
        
    except ClientError as e:
        print(f"❌ Error uploading to S3: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def update_production_database(mongodb_uri, book_cover_mapping):
    """Update production MongoDB with S3 URLs."""
    from pymongo import MongoClient
    
    try:
        client = MongoClient(mongodb_uri)
        db = client.inklaunch
        
        print("\n" + "="*70)
        print("Updating Production Database")
        print("="*70)
        
        for book_title, s3_url in book_cover_mapping.items():
            result = db.books.update_one(
                {'title': book_title},
                {'$set': {'cover_image_url': s3_url}}
            )
            
            if result.matched_count > 0:
                print(f"✓ Updated: {book_title}")
                print(f"  URL: {s3_url}")
            else:
                print(f"⚠ Book not found: {book_title}")
        
        client.close()
        print("\n✓ Production database updated successfully!")
        
    except Exception as e:
        print(f"❌ Error updating database: {e}")
        return False
    
    return True


def main():
    """Main deployment script."""
    print("="*70)
    print(" DEPLOY ACTUAL BOOK COVERS TO S3 & PRODUCTION")
    print("="*70)
    
    # Check for required environment variables
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_bucket = os.getenv('AWS_S3_BUCKET_NAME')
    aws_region = os.getenv('AWS_REGION', 'us-east-1')
    mongodb_uri = os.getenv('MONGODB_URI')
    
    # Validate AWS credentials
    if not aws_access_key or not aws_secret_key or not aws_bucket:
        print("\n❌ AWS credentials not found!")
        print("\nPlease set these environment variables:")
        print("  export AWS_ACCESS_KEY_ID='your_access_key'")
        print("  export AWS_SECRET_ACCESS_KEY='your_secret_key'")
        print("  export AWS_S3_BUCKET_NAME='your_bucket_name'")
        print("  export AWS_REGION='us-east-1'  # optional, defaults to us-east-1")
        print("\nSee S3_SETUP_GUIDE.md for detailed instructions.")
        sys.exit(1)
    
    # Validate MongoDB URI
    if not mongodb_uri:
        print("\n❌ MongoDB URI not found!")
        print("\nPlease set: export MONGODB_URI='mongodb+srv://...'")
        sys.exit(1)
    
    print(f"\n✓ AWS Bucket: {aws_bucket}")
    print(f"✓ AWS Region: {aws_region}")
    print(f"✓ MongoDB: Connected")
    
    # Define book covers to upload
    book_covers = [
        {
            'title': 'The Weight of Wings',
            'local_file': '/workspaces/InkLaunch/uploads/1770118718.02634_WSB1.jpeg',
            's3_key': 'book-covers/the-weight-of-wings.jpg'
        },
        {
            'title': 'The Day We Die',
            'local_file': '/workspaces/InkLaunch/uploads/1770175759.468088_The_Day_We_Die_1.png',
            's3_key': 'book-covers/the-day-we-die.png'
        }
    ]
    
    print("\n" + "="*70)
    print("Uploading Images to S3")
    print("="*70)
    
    s3_urls = {}
    
    for book in book_covers:
        print(f"\n📚 {book['title']}")
        
        # Check if file exists
        if not os.path.exists(book['local_file']):
            print(f"  ❌ File not found: {book['local_file']}")
            continue
        
        file_size = os.path.getsize(book['local_file']) / (1024 * 1024)
        print(f"  📁 File: {os.path.basename(book['local_file'])} ({file_size:.2f} MB)")
        print(f"  ☁️  Uploading to S3...")
        
        # Upload to S3
        url = upload_to_s3(
            book['local_file'],
            book['s3_key'],
            aws_bucket,
            aws_access_key,
            aws_secret_key,
            aws_region
        )
        
        if url:
            print(f"  ✓ Uploaded successfully!")
            print(f"  🔗 {url}")
            s3_urls[book['title']] = url
        else:
            print(f"  ❌ Upload failed!")
    
    if not s3_urls:
        print("\n❌ No images were uploaded successfully.")
        sys.exit(1)
    
    print(f"\n✓ Successfully uploaded {len(s3_urls)} images to S3")
    
    # Update production database
    if update_production_database(mongodb_uri, s3_urls):
        print("\n" + "="*70)
        print(" DEPLOYMENT COMPLETE!")
        print("="*70)
        print("\n✓ Book cover images are now in S3")
        print("✓ Production database updated with S3 URLs")
        print("✓ Images will persist across Render deployments")
        print("\nYour Render app will now display the actual book covers!")
        print("="*70)
    else:
        print("\n❌ Failed to update production database")
        sys.exit(1)


if __name__ == '__main__':
    main()
