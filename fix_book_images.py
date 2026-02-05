"""Fix book image URLs to use accessible placeholder service."""
from app import create_app, mongo
from urllib.parse import quote

app = create_app()

# Color palette for book covers
colors = [
    'FF6B6B/FFFFFF',  # Red
    '4ECDC4/FFFFFF',  # Teal
    'FFE66D/000000',  # Yellow
    'A8E6CF/000000',  # Mint
    'FF8B94/FFFFFF',  # Pink
    '95E1D3/000000',  # Turquoise
    'C7CEEA/000000',  # Lavender
    'FFDAC1/000000',  # Peach
    '667eea/FFFFFF',  # Purple
    'F38181/FFFFFF',  # Coral
]

with app.app_context():
    books = list(mongo.db.books.find({}))
    
    print(f"Updating {len(books)} books...")
    
    for idx, book in enumerate(books):
        title = book.get('title', 'Book')
        # URL encode the title for use in placeholder
        encoded_title = quote(title[:20])  # Limit to 20 chars
        
        # Pick a color based on book index
        color = colors[idx % len(colors)]
        
        # Use placehold.co instead of via.placeholder.com
        new_url = f"https://placehold.co/400x600/{color}?text={encoded_title}"
        
        # Update the book
        result = mongo.db.books.update_one(
            {'_id': book['_id']},
            {'$set': {'cover_image_url': new_url}}
        )
        
        if result.modified_count > 0:
            print(f"✓ Updated: {title}")
            print(f"  New URL: {new_url}")
        else:
            print(f"- Skipped: {title} (no change needed)")
    
    print(f"\n✓ Complete! Updated {len(books)} books.")
    print("Images should now display correctly.")
