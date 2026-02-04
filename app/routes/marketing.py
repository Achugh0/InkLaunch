"""Marketing and promotion tools routes."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models import (Book, User, PressKit, NewsletterSubscriber, BookGiveaway, 
                        GiveawayEntry, SocialShare)
from bson import ObjectId
from datetime import datetime, timedelta
import os

marketing_bp = Blueprint('marketing', __name__, url_prefix='/marketing')


@marketing_bp.route('/')
def index():
    """Marketing tools index page."""
    user = User.find_by_id(session.get('user_id')) if 'user_id' in session else None
    return render_template('marketing/index.html', user=user)


@marketing_bp.route('/press-kit', methods=['GET', 'POST'])
def press_kit():
    """Generate and manage press kit."""
    if 'user_id' not in session:
        flash('Please log in to access this feature.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.find_by_id(session['user_id'])
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # Get form data
        bio = request.form.get('bio', user.get('bio', ''))
        headshot_url = request.form.get('headshot_url', user.get('profile_image_url', ''))
        
        # Get author's books for cover images
        books = Book.find_by_author(session['user_id'])
        book_covers = [book.get('cover_image_url', '') for book in books if book.get('cover_image_url')]
        
        # Check if press kit already exists
        existing_kit = PressKit.find_by_author(session['user_id'])
        
        if existing_kit:
            # Update existing press kit
            updates = {
                'bio': bio,
                'headshot_url': headshot_url,
                'book_covers': book_covers
            }
            PressKit.update(str(existing_kit['_id']), updates)
            flash('Press kit updated successfully!', 'success')
        else:
            # Create new press kit
            PressKit.create(
                author_id=session['user_id'],
                bio=bio,
                headshot_url=headshot_url,
                book_covers=book_covers
            )
            flash('Press kit created successfully!', 'success')
        
        return redirect(url_for('marketing.press_kit'))
    
    # GET request
    press_kit = PressKit.find_by_author(session['user_id'])
    books = Book.find_by_author(session['user_id'])
    
    return render_template('marketing/press_kit.html', 
                         user=user, 
                         press_kit=press_kit,
                         books=books)


@marketing_bp.route('/press-kit/download/<press_kit_id>')
def download_press_kit(press_kit_id):
    """Download press kit as PDF."""
    press_kit = PressKit.find_by_author(press_kit_id)
    if not press_kit:
        flash('Press kit not found.', 'danger')
        return redirect(url_for('marketing.press_kit'))
    
    # Increment download count
    PressKit.increment_downloads(press_kit_id)
    
    # In production, generate PDF here
    # For now, redirect to view
    flash('Press kit download feature coming soon!', 'info')
    return redirect(url_for('marketing.press_kit'))


@marketing_bp.route('/newsletter', methods=['GET', 'POST'])
def newsletter():
    """Manage newsletter subscribers."""
    if 'user_id' not in session:
        flash('Please log in to access this feature.', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name', '')
        
        if email:
            NewsletterSubscriber.create(
                author_id=session['user_id'],
                email=email,
                subscriber_name=name
            )
            flash('Subscriber added successfully!', 'success')
        
        return redirect(url_for('marketing.newsletter'))
    
    # GET request
    subscribers = NewsletterSubscriber.find_by_author(session['user_id'])
    user = User.find_by_id(session['user_id'])
    
    return render_template('marketing/newsletter.html', 
                         subscribers=subscribers,
                         user=user)


@marketing_bp.route('/newsletter/subscribe/<author_id>', methods=['POST'])
def subscribe(author_id):
    """Public endpoint for newsletter subscription."""
    email = request.form.get('email')
    name = request.form.get('name', '')
    
    if email:
        NewsletterSubscriber.create(
            author_id=author_id,
            email=email,
            subscriber_name=name
        )
        flash('Successfully subscribed to newsletter!', 'success')
    
    return redirect(request.referrer or url_for('main.index'))


@marketing_bp.route('/giveaways')
def list_giveaways():
    """List all active giveaways."""
    page = int(request.args.get('page', 1))
    per_page = 20
    skip = (page - 1) * per_page
    
    giveaways = BookGiveaway.find_active_giveaways(skip=skip, limit=per_page)
    
    # Enrich with book and author data
    for giveaway in giveaways:
        giveaway['book'] = Book.find_by_id(str(giveaway['book_id']))
        giveaway['author'] = User.find_by_id(str(giveaway['author_id']))
    
    return render_template('marketing/giveaways.html', 
                         giveaways=giveaways,
                         page=page)


@marketing_bp.route('/giveaways/create', methods=['GET', 'POST'])
def create_giveaway():
    """Create a new book giveaway."""
    if 'user_id' not in session:
        flash('Please log in to access this feature.', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        title = request.form.get('title')
        description = request.form.get('description')
        num_winners = int(request.form.get('num_winners', 1))
        duration_days = int(request.form.get('duration_days', 7))
        
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=duration_days)
        
        BookGiveaway.create(
            author_id=session['user_id'],
            book_id=book_id,
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            num_winners=num_winners
        )
        
        flash('Giveaway created successfully!', 'success')
        return redirect(url_for('marketing.my_giveaways'))
    
    # GET request
    books = Book.find_by_author(session['user_id'])
    user = User.find_by_id(session['user_id'])
    
    return render_template('marketing/create_giveaway.html', 
                         books=books,
                         user=user)


@marketing_bp.route('/giveaways/my')
def my_giveaways():
    """List author's giveaways."""
    if 'user_id' not in session:
        flash('Please log in to access this feature.', 'warning')
        return redirect(url_for('auth.login'))
    
    giveaways = BookGiveaway.find_by_author(session['user_id'])
    
    # Enrich with book data and entry counts
    for giveaway in giveaways:
        giveaway['book'] = Book.find_by_id(str(giveaway['book_id']))
        giveaway['entries'] = GiveawayEntry.find_by_giveaway(str(giveaway['_id']))
    
    user = User.find_by_id(session['user_id'])
    
    return render_template('marketing/my_giveaways.html', 
                         giveaways=giveaways,
                         user=user)


@marketing_bp.route('/giveaways/<giveaway_id>/enter', methods=['POST'])
def enter_giveaway(giveaway_id):
    """Enter a giveaway."""
    if 'user_id' not in session:
        flash('Please log in to enter giveaways.', 'warning')
        return redirect(url_for('auth.login'))
    
    giveaway = BookGiveaway.find_by_id(giveaway_id)
    if not giveaway:
        flash('Giveaway not found.', 'danger')
        return redirect(url_for('marketing.list_giveaways'))
    
    # Check if already entered
    if GiveawayEntry.check_entered(giveaway_id, session['user_id']):
        flash('You have already entered this giveaway.', 'info')
        return redirect(url_for('marketing.list_giveaways'))
    
    # Create entry
    GiveawayEntry.create(giveaway_id=giveaway_id, user_id=session['user_id'])
    
    flash('Successfully entered giveaway!', 'success')
    return redirect(url_for('marketing.list_giveaways'))


@marketing_bp.route('/social-share/<book_id>/<platform>')
def track_social_share(book_id, platform):
    """Track social media shares."""
    book = Book.find_by_id(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    # Get book URL
    book_url = url_for('books.book_detail', book_id=book_id, _external=True)
    
    # Create share record
    SocialShare.create(
        book_id=book_id,
        author_id=str(book['author_id']),
        platform=platform,
        share_url=book_url
    )
    
    # Generate platform-specific share URLs
    share_urls = {
        'facebook': f'https://www.facebook.com/sharer/sharer.php?u={book_url}',
        'twitter': f'https://twitter.com/intent/tweet?url={book_url}&text=Check out "{book["title"]}" on InkLaunch!',
        'whatsapp': f'https://wa.me/?text=Check out "{book["title"]}" on InkLaunch! {book_url}',
        'linkedin': f'https://www.linkedin.com/sharing/share-offsite/?url={book_url}'
    }
    
    if platform in share_urls:
        return redirect(share_urls[platform])
    
    return jsonify({'error': 'Invalid platform'}), 400


@marketing_bp.route('/widget/<book_id>')
def book_widget(book_id):
    """Get embeddable widget code for a book."""
    book = Book.find_by_id(book_id)
    if not book:
        flash('Book not found.', 'danger')
        return redirect(url_for('main.index'))
    
    author = User.find_by_id(str(book['author_id']))
    book_url = url_for('books.book_detail', book_id=book_id, _external=True)
    
    # Generate HTML widget code
    widget_code = f'''
<!-- InkLaunch Book Widget -->
<div style="border: 1px solid #ddd; padding: 20px; max-width: 400px; border-radius: 8px; font-family: Arial, sans-serif;">
    <img src="{book.get('cover_image_url', '')}" alt="{book['title']}" style="width: 100%; height: auto; margin-bottom: 15px;">
    <h3 style="margin: 0 0 10px 0; font-size: 18px;">{book['title']}</h3>
    <p style="margin: 0 0 10px 0; color: #666; font-size: 14px;">by {author['full_name']}</p>
    <p style="margin: 0 0 15px 0; font-size: 14px;">{book.get('description', '')[:150]}...</p>
    <a href="{book_url}" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 14px;">View on InkLaunch</a>
</div>
<!-- End InkLaunch Book Widget -->
    '''
    
    return render_template('marketing/widget.html', 
                         book=book,
                         author=author,
                         widget_code=widget_code)


@marketing_bp.route('/countdown/<book_id>')
def launch_countdown(book_id):
    """Display countdown for book launch."""
    book = Book.find_by_id(book_id)
    if not book:
        flash('Book not found.', 'danger')
        return redirect(url_for('main.index'))
    
    author = User.find_by_id(str(book['author_id']))
    
    return render_template('marketing/countdown.html', 
                         book=book,
                         author=author)
