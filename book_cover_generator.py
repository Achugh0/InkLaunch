"""Generate book cover images for InkLaunch books.

This script can be used to generate professional-looking book cover images
for books in the database that don't have cover images yet.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import sys

# Color schemes for book covers
COLOR_SCHEMES = [
    {'bg': '#2C1810', 'text': '#D4AF37', 'name': 'Classic Gold'},  # Dark brown + Gold
    {'bg': '#1A3A52', 'text': '#E8E8E8', 'name': 'Navy Blue'},     # Dark blue + Off-white
    {'bg': '#1F1F1F', 'text': '#FF6B6B', 'name': 'Dark Red'},      # Black + Red
    {'bg': '#0D3B2E', 'text': '#C7F0D8', 'name': 'Forest Green'},  # Dark green + Mint
    {'bg': '#3D1F3A', 'text': '#FFD700', 'name': 'Royal Purple'},  # Purple + Gold
    {'bg': '#4A2C2A', 'text': '#FFB366', 'name': 'Warm Earth'},    # Brown + Orange
    {'bg': '#1A1A2E', 'text': '#00D9FF', 'name': 'Tech Blue'},     # Dark + Cyan
    {'bg': '#2D1B1B', 'text': '#E8C4A0', 'name': 'Vintage Cream'}, # Dark brown + Cream
]


def create_book_cover(title, author, output_filename, scheme_index=0):
    """
    Create a professional book cover image.
    
    Args:
        title: Book title
        author: Author name
        output_filename: Output filename (without path)
        scheme_index: Index of color scheme to use (0-7)
    
    Returns:
        Full path to the created image
    """
    # Get color scheme
    scheme = COLOR_SCHEMES[scheme_index % len(COLOR_SCHEMES)]
    bg_color = scheme['bg']
    text_color = scheme['text']
    
    # Create image
    width, height = 400, 600
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        author_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        author_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw decorative borders
    draw.rectangle([(20, 20), (380, 25)], fill=text_color)
    draw.rectangle([(20, 575), (380, 580)], fill=text_color)
    draw.rectangle([(20, 20), (25, 580)], fill=text_color)
    draw.rectangle([(375, 20), (380, 580)], fill=text_color)
    
    # Wrap title text
    title_words = title.split()
    lines = []
    current_line = []
    
    for word in title_words:
        current_line.append(word)
        test_line = ' '.join(current_line)
        bbox = draw.textbbox((0, 0), test_line, font=title_font)
        if bbox[2] - bbox[0] > 340:  # Max width
            if len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw title
    title_height = len(lines) * 60
    start_y = (height - title_height - 120) // 2
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = start_y + (i * 60)
        # Add shadow effect
        draw.text((x+2, y+2), line, fill='#000000', font=title_font)
        draw.text((x, y), line, fill=text_color, font=title_font)
    
    # Draw author name
    author_bbox = draw.textbbox((0, 0), author, font=author_font)
    author_width = author_bbox[2] - author_bbox[0]
    author_x = (width - author_width) // 2
    author_y = height - 80
    draw.text((author_x, author_y), author, fill=text_color, font=author_font)
    
    # Add subtle decorative elements
    for i in range(0, width, 40):
        for j in range(50, height-100, 40):
            if (i + j) % 120 == 0:
                draw.ellipse([i-1, j-1, i+1, j+1], fill=text_color, outline=text_color)
    
    # Save image
    output_dir = '/workspaces/InkLaunch/app/static/images/book-covers'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)
    image.save(output_path, 'JPEG', quality=95)
    
    return output_path


def generate_covers_for_all_books():
    """Generate covers for all books without cover images."""
    from app import create_app, mongo
    
    app = create_app()
    
    with app.app_context():
        # Find books without cover images or with placeholder images
        books = list(mongo.db.books.find({
            '$or': [
                {'cover_image_url': ''},
                {'cover_image_url': {'$regex': 'placeholder|placehold'}}
            ]
        }))
        
        print(f"Found {len(books)} books needing cover images\n")
        
        for idx, book in enumerate(books):
            title = book.get('title', 'Untitled')
            
            # Get author name
            from app.models import User
            author = User.find_by_id(str(book.get('user_id')))
            author_name = author.get('full_name', 'Unknown Author') if author else 'Unknown Author'
            
            # Generate filename from title
            filename = title.lower().replace(' ', '-').replace("'", '')
            filename = ''.join(c for c in filename if c.isalnum() or c == '-')
            filename = f"{filename}.jpg"
            
            # Create cover
            output_path = create_book_cover(
                title=title,
                author=author_name,
                output_filename=filename,
                scheme_index=idx
            )
            
            # Update database
            cover_url = f"/static/images/book-covers/{filename}"
            mongo.db.books.update_one(
                {'_id': book['_id']},
                {'$set': {'cover_image_url': cover_url}}
            )
            
            print(f"✓ {title}")
            print(f"  Generated: {output_path}")
            print(f"  Color scheme: {COLOR_SCHEMES[idx % len(COLOR_SCHEMES)]['name']}")
            print()
        
        print(f"\n✓ Generated {len(books)} book covers!")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'all':
        generate_covers_for_all_books()
    else:
        print("Book Cover Generator for InkLaunch")
        print("=" * 50)
        print("\nUsage:")
        print("  python book_cover_generator.py all")
        print("    - Generate covers for all books without images")
        print()
        print("Or use as a module:")
        print("  from book_cover_generator import create_book_cover")
        print("  create_book_cover('My Book Title', 'Author Name', 'my-book.jpg', scheme_index=0)")
