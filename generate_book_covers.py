"""Generate professional-looking book cover images."""
from PIL import Image, ImageDraw, ImageFont
import os

def create_book_cover(title, author, filename, bg_color, text_color):
    """Create a book cover image with title and author."""
    # Create image
    width, height = 400, 600
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)
    
    # Try to use a nice font, fall back to default if not available
    try:
        # Try different font sizes for title
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        author_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        author_font = ImageFont.load_default()
    
    # Draw decorative elements
    # Top border
    draw.rectangle([(20, 20), (380, 25)], fill=text_color)
    # Bottom border
    draw.rectangle([(20, 575), (380, 580)], fill=text_color)
    
    # Draw title (wrapped if needed)
    title_words = title.split()
    lines = []
    current_line = []
    
    for word in title_words:
        current_line.append(word)
        test_line = ' '.join(current_line)
        bbox = draw.textbbox((0, 0), test_line, font=title_font)
        if bbox[2] - bbox[0] > 340:  # Max width
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    
    # Calculate vertical position for centered text
    title_height = len(lines) * 60
    start_y = (height - title_height - 100) // 2
    
    # Draw title lines
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = start_y + (i * 60)
        draw.text((x, y), line, fill=text_color, font=title_font)
    
    # Draw author name at bottom
    author_bbox = draw.textbbox((0, 0), author, font=author_font)
    author_width = author_bbox[2] - author_bbox[0]
    author_x = (width - author_width) // 2
    author_y = height - 80
    draw.text((author_x, author_y), author, fill=text_color, font=author_font)
    
    # Add subtle texture/pattern
    for i in range(0, width, 40):
        for j in range(0, height, 40):
            if (i + j) % 80 == 0:
                draw.ellipse([i, j, i+2, j+2], fill=text_color, outline=text_color)
    
    # Save image
    output_path = f'/workspaces/InkLaunch/app/static/images/book-covers/{filename}'
    image.save(output_path, 'JPEG', quality=95)
    print(f"✓ Created: {output_path}")
    return f'/static/images/book-covers/{filename}'


# Create book covers
covers = [
    {
        'title': 'The Weight of Wings',
        'author': 'Ashish Chugh',
        'filename': 'weight-of-wings.jpg',
        'bg_color': '#2C1810',  # Dark brown
        'text_color': '#D4AF37'  # Gold
    },
    {
        'title': 'The Day We Die',
        'author': 'Ashish Chugh',
        'filename': 'the-day-we-die.jpg',
        'bg_color': '#1A3A52',  # Dark blue
        'text_color': '#E8E8E8'  # Off-white
    }
]

print("Generating book cover images...\n")
for cover_data in covers:
    create_book_cover(
        title=cover_data['title'],
        author=cover_data['author'],
        filename=cover_data['filename'],
        bg_color=cover_data['bg_color'],
        text_color=cover_data['text_color']
    )

print("\n✓ All book covers generated successfully!")
