"""Upload to ImgBB - Free unlimited image hosting."""
import requests
import base64
import os
import sys


def upload_to_imgbb(image_path, api_key):
    """Upload image to ImgBB."""
    url = "https://api.imgbb.com/1/upload"
    
    with open(image_path, 'rb') as file:
        payload = {
            'key': api_key,
            'image': base64.b64encode(file.read()),
        }
        
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            return response.json()['data']['url']
        else:
            print(f"Error: {response.text}")
            return None


def main():
    print("Upload Book Covers to ImgBB (Free)")
    print("="*60)
    
    api_key = os.getenv('IMGBB_API_KEY')
    mongodb_uri = os.getenv('MONGODB_URI')
    
    if not api_key:
        print("\n❌ Get free API key from: https://api.imgbb.com/")
        print("Then: export IMGBB_API_KEY='your_key'")
        sys.exit(1)
    
    books = [
        ('The Weight of Wings', '/workspaces/InkLaunch/uploads/1770118718.02634_WSB1.jpeg'),
        ('The Day We Die', '/workspaces/InkLaunch/uploads/1770175759.468088_The_Day_We_Die_1.png')
    ]
    
    urls = {}
    
    for title, path in books:
        print(f"\nUploading: {title}...")
        url = upload_to_imgbb(path, api_key)
        if url:
            print(f"✓ {url}")
            urls[title] = url
    
    # Update database
    if mongodb_uri and urls:
        from pymongo import MongoClient
        client = MongoClient(mongodb_uri)
        db = client.inklaunch
        
        for title, url in urls.items():
            db.books.update_one({'title': title}, {'$set': {'cover_image_url': url}})
            print(f"✓ Updated database: {title}")
        
        client.close()
    
    print("\n✓ Done! No configuration needed on Render.")
    print("Images are hosted on ImgBB forever, for free.")


if __name__ == '__main__':
    main()
