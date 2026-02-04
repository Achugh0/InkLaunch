"""Manuscript competition routes for authors."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from app.models import Competition, CompetitionSubmission, CompetitionWinner, User, Book
from app import mongo

bp = Blueprint('manuscript_competitions', __name__, url_prefix='/manuscript-competitions')

# Configure upload folder
UPLOAD_FOLDER = 'uploads/manuscripts'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/')
def browse():
    """Browse all active and upcoming competitions."""
    genre_filter = request.args.get('genre', '')
    
    # Get active competitions (currently accepting submissions)
    active_competitions = Competition.find_active()
    
    # Get upcoming competitions (not yet started)
    upcoming_competitions = Competition.find_upcoming()
    
    # Combine active and upcoming
    all_competitions = active_competitions + upcoming_competitions
    
    # Filter by genre if specified
    if genre_filter:
        all_competitions = [c for c in all_competitions if genre_filter in c['genre_categories']]
    
    # Get completed competitions (for showcasing winners)
    completed_competitions = Competition.find_all(status='completed', limit=6)
    
    # Add submission counts and status flags
    now = datetime.utcnow()
    for comp in all_competitions:
        comp['submission_count'] = Competition.count_submissions(str(comp['_id']))
        comp['is_upcoming'] = comp['submission_start_date'] > now
        comp['is_active'] = comp['submission_start_date'] <= now <= comp['submission_end_date']
    
    for comp in completed_competitions:
        comp['submission_count'] = Competition.count_submissions(str(comp['_id']))
    
    # Get all unique genres from all competitions
    all_genres = set()
    for comp in all_competitions:
        all_genres.update(comp['genre_categories'])
    
    return render_template('manuscript_competitions/browse.html',
                         active_competitions=all_competitions,
                         completed_competitions=completed_competitions,
                         all_genres=sorted(all_genres),
                         current_genre=genre_filter)


@bp.route('/<competition_id>')
def detail(competition_id):
    """View competition details."""
    competition = Competition.find_by_id(competition_id)
    if not competition:
        flash('Competition not found.', 'danger')
        return redirect(url_for('manuscript_competitions.browse'))
    
    # Check if user has already submitted
    user_submission = None
    from flask import session
    if session.get('user_id'):
        submissions = CompetitionSubmission.find_by_author(str(session['user_id']))
        user_submission = next((s for s in submissions if str(s['competition_id']) == competition_id), None)
    
    # Get submission count
    submission_count = Competition.count_submissions(competition_id)
    
    # Get winners if competition is completed
    winners = []
    if competition['status'] in ['completed', 'archived']:
        winners = CompetitionWinner.find_by_competition(competition_id)
        for winner in winners:
            submission = CompetitionSubmission.find_by_id(str(winner['submission_id']))
            author = User.find_by_id(str(winner['author_id']))
            winner['submission'] = submission
            winner['author'] = author
    
    # Calculate time remaining or time until opening
    now = datetime.utcnow()
    time_remaining = None
    is_upcoming = competition['submission_start_date'] > now
    
    if competition['status'] == 'accepting_submissions':
        if is_upcoming:
            # Competition hasn't started yet
            delta = competition['submission_start_date'] - now
            days = delta.days
            hours = delta.seconds // 3600
            time_remaining = {'days': days, 'hours': hours, 'until_start': True}
        else:
            # Competition is active
            delta = competition['submission_end_date'] - now
            if delta.total_seconds() > 0:
                days = delta.days
                hours = delta.seconds // 3600
                time_remaining = {'days': days, 'hours': hours, 'until_start': False}
    
    return render_template('manuscript_competitions/detail.html',
                         competition=competition,
                         user_submission=user_submission,
                         submission_count=submission_count,
                         winners=winners,
                         time_remaining=time_remaining,
                         is_upcoming=is_upcoming)


@bp.route('/<competition_id>/submit', methods=['GET', 'POST'])
@login_required
def submit_entry(competition_id):
    """Submit an entry to a competition."""
    competition = Competition.find_by_id(competition_id)
    if not competition:
        flash('Competition not found.', 'danger')
        return redirect(url_for('manuscript_competitions.browse'))
    
    # Check if competition is accepting submissions
    if competition['status'] != 'accepting_submissions':
        flash('This competition is not currently accepting submissions.', 'warning')
        return redirect(url_for('manuscript_competitions.detail', competition_id=competition_id))
    
    # Check if submission window is open
    now = datetime.utcnow()
    if now < competition['submission_start_date'] or now > competition['submission_end_date']:
        flash('Submission window is closed.', 'warning')
        return redirect(url_for('manuscript_competitions.detail', competition_id=competition_id))
    
    # Check if user has reached max submissions
    user_submission_count = CompetitionSubmission.count_by_author_and_competition(
        str(session['user_id']), competition_id
    )
    if user_submission_count >= competition['max_submissions_per_author']:
        flash(f'You have reached the maximum of {competition["max_submissions_per_author"]} submission(s) for this competition.', 'warning')
        return redirect(url_for('manuscript_competitions.detail', competition_id=competition_id))
    
    if request.method == 'POST':
        submission_type = request.form.get('submission_type', 'new')  # 'new' or 'existing'
        
        if submission_type == 'existing':
            # Use existing book from user's library
            book_id = request.form.get('existing_book_id')
            if not book_id:
                flash('Please select a book from your library.', 'danger')
                return redirect(request.url)
            
            book = Book.find_by_id(book_id)
            if not book:
                flash('Book not found.', 'danger')
                return redirect(request.url)
            
            # Verify the book belongs to the user
            if str(book['user_id']) != str(session['user_id']):
                flash('You can only submit your own books.', 'danger')
                return redirect(request.url)
            
            # Use book details
            manuscript_title = book['title']
            genre = book.get('genre', request.form.get('genre'))
            synopsis = book.get('description', '')
            word_count = book.get('page_count', 0) * 250  # Approximate word count
            manuscript_file_url = book.get('cover_image_url', '')  # Link to book entry
            author_statement = request.form.get('author_statement', '')
            
        else:
            # New manuscript upload
            manuscript_title = request.form.get('manuscript_title')
            genre = request.form.get('genre')
            synopsis = request.form.get('synopsis')
            author_statement = request.form.get('author_statement', '')
            
            # Handle file upload
            if 'manuscript_file' not in request.files:
                flash('No manuscript file uploaded.', 'danger')
                return redirect(request.url)
            
            file = request.files['manuscript_file']
            if file.filename == '':
                flash('No manuscript file selected.', 'danger')
                return redirect(request.url)
            
            if not allowed_file(file.filename):
                flash('Invalid file type. Please upload PDF, DOCX, or TXT file.', 'danger')
                return redirect(request.url)
            
            # Save file
            filename = secure_filename(f"{session['user_id']}_{competition_id}_{datetime.utcnow().timestamp()}_{file.filename}")
            
            # Ensure upload directory exists
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            manuscript_file_url = file_path
            
            # Get word count (simplified - in production, parse the file)
            word_count = int(request.form.get('word_count', 0))
        
        # Create submission (entry fee handling would go here for paid competitions)
        entry_fee_paid = competition['entry_fee_amount'] == 0  # Auto-approve if free
        
        submission_id = CompetitionSubmission.create(
            competition_id=competition_id,
            author_id=str(session['user_id']),
            manuscript_title=manuscript_title,
            manuscript_file_url=manuscript_file_url,
            word_count=word_count,
            genre=genre,
            synopsis=synopsis,
            author_statement=author_statement,
            entry_fee_paid=entry_fee_paid
        )
        
        # Update user's competition stats (increment submissions and entries)
        user = User.find_by_id(str(session['user_id']))
        current_stats = user.get('competition_stats', {})
        
        # Check if this is first submission to this competition
        user_submissions = CompetitionSubmission.find_by_author(str(session['user_id']))
        is_first_submission = sum(1 for s in user_submissions if str(s['competition_id']) == competition_id) == 1
        
        User.update_competition_stats(
            user_id=str(session['user_id']),
            stat_updates={
                'total_submissions': current_stats.get('total_submissions', 0) + 1,
                'total_entered': current_stats.get('total_entered', 0) + (1 if is_first_submission else 0)
            }
        )
        
        flash('Your submission has been received successfully!', 'success')
        return redirect(url_for('manuscript_competitions.my_submissions'))
    
    # GET: Load user's existing books
    user_books = Book.find_by_user(str(session['user_id']))
    
    return render_template('manuscript_competitions/submit.html',
                         competition=competition,
                         user_books=user_books)


@bp.route('/my-submissions')
@login_required
def my_submissions():
    """View user's competition submissions."""
    submissions = CompetitionSubmission.find_by_author(str(session['user_id']))
    
    # Enrich submissions with competition data
    for submission in submissions:
        competition = Competition.find_by_id(str(submission['competition_id']))
        submission['competition'] = competition
        
        # Check if user won
        if submission['submission_status'] == 'winner':
            winner = mongo.db.competition_winners.find_one({
                'submission_id': submission['_id']
            })
            submission['winner_info'] = winner
    
    return render_template('manuscript_competitions/my_submissions.html',
                         submissions=submissions)


@bp.route('/my-wins')
@login_required
def my_wins():
    """View user's competition wins."""
    wins = CompetitionWinner.find_by_author(str(session['user_id']))
    
    # Enrich with competition and submission data
    for win in wins:
        competition = Competition.find_by_id(str(win['competition_id']))
        submission = CompetitionSubmission.find_by_id(str(win['submission_id']))
        win['competition'] = competition
        win['submission'] = submission
    
    return render_template('manuscript_competitions/my_wins.html', wins=wins)
