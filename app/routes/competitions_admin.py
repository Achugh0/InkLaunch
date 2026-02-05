"""Admin routes for competition management."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from functools import wraps
from datetime import datetime, timedelta
from bson import ObjectId
from app.models import Competition, CompetitionSubmission, AIEvaluation, CompetitionWinner, User, Book, Review
from app.services.ai_service import evaluate_manuscript
import os

bp = Blueprint('competitions_admin', __name__, url_prefix='/admin/competitions')


def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id') or session.get('user_role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


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
@login_required
@admin_required
def list_competitions():
    """List all competitions in admin panel."""
    status_filter = request.args.get('status', '')
    
    if status_filter:
        competitions = Competition.find_all(status=status_filter)
    else:
        competitions = Competition.find_all(limit=100)
    
    # Add submission counts
    for comp in competitions:
        comp['submission_count'] = Competition.count_submissions(str(comp['_id']))
    
    return render_template('admin/competitions/list.html', competitions=competitions)


@bp.route('/analytics')
@login_required
@admin_required
def analytics_dashboard():
    """Comprehensive analytics dashboard for competitions and platform metrics."""
    from app import mongo
    from datetime import timedelta
    
    # === COMPETITION METRICS ===
    total_competitions = mongo.db['competitions'].count_documents({})
    total_submissions = mongo.db['competition_submissions'].count_documents({})
    total_evaluations = mongo.db['ai_evaluations'].count_documents({})
    total_winners = mongo.db['competition_winners'].count_documents({})
    
    # === USER METRICS ===
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    total_users = mongo.db['users'].count_documents({})
    active_users_30d = mongo.db['users'].count_documents({
        '$or': [
            {'last_login': {'$gte': thirty_days_ago}},
            {'created_at': {'$gte': thirty_days_ago}}
        ]
    })
    new_users_today = mongo.db['users'].count_documents({'created_at': {'$gte': today_start}})
    
    users_this_week = mongo.db['users'].count_documents({'created_at': {'$gte': seven_days_ago}})
    users_last_week = mongo.db['users'].count_documents({
        'created_at': {'$gte': seven_days_ago - timedelta(days=7), '$lt': seven_days_ago}
    })
    user_growth_rate = ((users_this_week - users_last_week) / users_last_week * 100) if users_last_week > 0 else 0
    
    # === CONTENT METRICS ===
    total_books = mongo.db['books'].count_documents({})
    books_added_today = mongo.db['books'].count_documents({'created_at': {'$gte': today_start}})
    books_this_week = mongo.db['books'].count_documents({'created_at': {'$gte': seven_days_ago}})
    books_last_week = mongo.db['books'].count_documents({
        'created_at': {'$gte': seven_days_ago - timedelta(days=7), '$lt': seven_days_ago}
    })
    book_growth_rate = ((books_this_week - books_last_week) / books_last_week * 100) if books_last_week > 0 else 0
    avg_books_per_author = total_books / total_users if total_users > 0 else 0
    
    # === ENGAGEMENT METRICS ===
    total_reviews = mongo.db['reviews'].count_documents({})
    reviews_today = mongo.db['reviews'].count_documents({'created_at': {'$gte': today_start}})
    avg_reviews_per_book = total_reviews / total_books if total_books > 0 else 0
    
    avg_rating_result = list(mongo.db['reviews'].aggregate([
        {'$group': {'_id': None, 'avg_rating': {'$avg': '$rating'}}}
    ]))
    avg_rating = avg_rating_result[0].get('avg_rating', 0) if avg_rating_result else 0
    
    users_in_competitions = mongo.db['competition_submissions'].distinct('author_id')
    competition_participation_rate = (len(users_in_competitions) / total_users * 100) if total_users > 0 else 0
    
    # === COMPETITION ANALYTICS ===
    status_breakdown = list(mongo.db['competitions'].aggregate([
        {'$group': {'_id': '$status', 'count': {'$sum': 1}}}
    ]))
    
    submissions_by_comp = list(mongo.db['competition_submissions'].aggregate([
        {'$group': {'_id': '$competition_id', 'count': {'$sum': 1}, 'avg_word_count': {'$avg': '$word_count'}}},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ]))
    for item in submissions_by_comp:
        comp = mongo.db['competitions'].find_one({'_id': item['_id']})
        item['competition'] = comp
    
    genre_stats = list(mongo.db['competition_submissions'].aggregate([
        {'$group': {'_id': '$genre', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}
    ]))
    
    score_stats = list(mongo.db['ai_evaluations'].aggregate([
        {'$group': {
            '_id': '$competition_id',
            'avg_overall_score': {'$avg': '$overall_score'},
            'avg_plot': {'$avg': '$scores.plot_story_structure'},
            'avg_character': {'$avg': '$scores.character_development'},
            'avg_writing': {'$avg': '$scores.writing_quality_style'},
            'avg_originality': {'$avg': '$scores.originality_creativity'},
            'evaluations_count': {'$sum': 1}
        }},
        {'$sort': {'avg_overall_score': -1}}
    ]))
    for item in score_stats:
        comp = mongo.db['competitions'].find_one({'_id': item['_id']})
        item['competition'] = comp
    
    top_authors = list(mongo.db['users'].aggregate([
        {'$match': {'competition_stats.total_wins': {'$gt': 0}}},
        {'$sort': {'competition_stats.total_wins': -1}},
        {'$limit': 10},
        {'$project': {'full_name': 1, 'email': 1, 'competition_stats': 1}}
    ]))
    
    recent_submissions = list(mongo.db['competition_submissions'].aggregate([
        {'$match': {'submitted_at': {'$gte': thirty_days_ago}}},
        {'$group': {
            '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$submitted_at'}},
            'count': {'$sum': 1}
        }},
        {'$sort': {'_id': 1}}
    ]))
    
    # === TRENDS (Last 30 Days) ===
    user_registration_trend = list(mongo.db['users'].aggregate([
        {'$match': {'created_at': {'$gte': thirty_days_ago}}},
        {'$group': {
            '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$created_at'}},
            'count': {'$sum': 1}
        }},
        {'$sort': {'_id': 1}}
    ]))
    
    book_addition_trend = list(mongo.db['books'].aggregate([
        {'$match': {'created_at': {'$gte': thirty_days_ago}}},
        {'$group': {
            '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$created_at'}},
            'count': {'$sum': 1}
        }},
        {'$sort': {'_id': 1}}
    ]))
    
    review_activity_trend = list(mongo.db['reviews'].aggregate([
        {'$match': {'created_at': {'$gte': thirty_days_ago}}},
        {'$group': {
            '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$created_at'}},
            'count': {'$sum': 1}
        }},
        {'$sort': {'_id': 1}}
    ]))
    
    active_competitions = Competition.find_active()
    upcoming_competitions = Competition.find_upcoming()
    
    for comp in active_competitions + upcoming_competitions:
        comp['submission_count'] = Competition.count_submissions(str(comp['_id']))
        comp['evaluation_count'] = mongo.db['ai_evaluations'].count_documents({
            'competition_id': comp['_id']
        })
    
    return render_template('admin/competitions/analytics.html',
                         # Competition metrics
                         total_competitions=total_competitions,
                         total_submissions=total_submissions,
                         total_evaluations=total_evaluations,
                         total_winners=total_winners,
                         # User metrics
                         total_users=total_users,
                         active_users_30d=active_users_30d,
                         new_users_today=new_users_today,
                         user_growth_rate=user_growth_rate,
                         # Content metrics
                         total_books=total_books,
                         books_added_today=books_added_today,
                         book_growth_rate=book_growth_rate,
                         avg_books_per_author=avg_books_per_author,
                         # Engagement metrics
                         total_reviews=total_reviews,
                         reviews_today=reviews_today,
                         avg_reviews_per_book=avg_reviews_per_book,
                         avg_rating=avg_rating,
                         competition_participation_rate=competition_participation_rate,
                         # Competition analytics
                         status_breakdown=status_breakdown,
                         submissions_by_comp=submissions_by_comp,
                         genre_stats=genre_stats,
                         score_stats=score_stats,
                         top_authors=top_authors,
                         recent_submissions=recent_submissions,
                         active_competitions=active_competitions,
                         upcoming_competitions=upcoming_competitions,
                         # Trends
                         user_registration_trend=user_registration_trend,
                         book_addition_trend=book_addition_trend,
                         review_activity_trend=review_activity_trend)
    
    return render_template('admin/competitions/analytics.html',
                         total_competitions=total_competitions,
                         total_submissions=total_submissions,
                         total_evaluations=total_evaluations,
                         total_winners=total_winners,
                         status_breakdown=status_breakdown,
                         submissions_by_comp=submissions_by_comp,
                         genre_stats=genre_stats,
                         score_stats=score_stats,
                         top_authors=top_authors,
                         recent_submissions=recent_submissions,
                         active_competitions=active_competitions,
                         upcoming_competitions=upcoming_competitions)
    
    return render_template('admin/competitions/list.html', 
                         competitions=competitions,
                         current_filter=status_filter)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_competition():
    """Create a new competition."""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        genre_categories = request.form.getlist('genre_categories')
        
        # Parse dates
        submission_start = datetime.strptime(request.form.get('submission_start_date'), '%Y-%m-%d')
        submission_end = datetime.strptime(request.form.get('submission_end_date'), '%Y-%m-%d')
        
        winner_announcement = None
        if request.form.get('winner_announcement_date'):
            winner_announcement = datetime.strptime(request.form.get('winner_announcement_date'), '%Y-%m-%d')
        
        # Evaluation criteria (simple for MVP)
        evaluation_criteria = {
            'plot_structure': int(request.form.get('weight_plot', 25)),
            'character_development': int(request.form.get('weight_character', 25)),
            'writing_quality': int(request.form.get('weight_writing', 25)),
            'originality': int(request.form.get('weight_originality', 25))
        }
        
        # Prize structure
        prize_structure = {
            'first_place': request.form.get('prize_first', ''),
            'second_place': request.form.get('prize_second', ''),
            'third_place': request.form.get('prize_third', '')
        }
        
        max_submissions = int(request.form.get('max_submissions_per_author', 1))
        entry_fee = float(request.form.get('entry_fee_amount', 0))
        
        competition_id = Competition.create(
            title=title,
            description=description,
            genre_categories=genre_categories,
            submission_start_date=submission_start,
            submission_end_date=submission_end,
            evaluation_criteria=evaluation_criteria,
            max_submissions_per_author=max_submissions,
            entry_fee_amount=entry_fee,
            prize_structure=prize_structure,
            created_by_admin_id=str(session['user_id']),
            winner_announcement_date=winner_announcement
        )
        
        flash('Competition created successfully!', 'success')
        return redirect(url_for('competitions_admin.view_competition', competition_id=competition_id))
    
    # Available genres
    genres = ['Action', 'Adventure', 'Art', 'Biography', 'Business',
              'Children', 'Cooking', 'Crime', 'Dystopian', 'Education',
              'Essays', 'Fantasy', 'Fiction', 'Graphic Novel', 'Health',
              'Historical Fiction', 'History', 'Horror', 'Literary Fiction',
              'Memoir', 'Middle Grade', 'Mystery', 'Non-Fiction', 'Philosophy',
              'Poetry', 'Politics', 'Religion', 'Romance', 'Science',
              'Science Fiction', 'Self-Help', 'Technology', 'Thriller',
              'Travel', 'True Crime', 'Young Adult']
    
    return render_template('admin/competitions/create.html', genres=genres)


@bp.route('/<competition_id>')
@login_required
@admin_required
def view_competition(competition_id):
    """View competition details and manage submissions."""
    competition = Competition.find_by_id(competition_id)
    if not competition:
        flash('Competition not found.', 'danger')
        return redirect(url_for('competitions_admin.list_competitions'))
    
    # Get all submissions
    submissions = CompetitionSubmission.find_by_competition(competition_id)
    
    # Enrich submissions with author info and evaluation
    for submission in submissions:
        author = User.find_by_id(str(submission['author_id']))
        submission['author'] = author
        
        evaluation = AIEvaluation.find_by_submission(str(submission['_id']))
        submission['evaluation'] = evaluation
    
    # Get winners if announced
    winners = []
    if competition['status'] in ['completed', 'archived']:
        winners = CompetitionWinner.find_by_competition(competition_id)
        for winner in winners:
            author = User.find_by_id(str(winner['author_id']))
            winner['author'] = author
    
    return render_template('admin/competitions/view.html',
                         competition=competition,
                         submissions=submissions,
                         winners=winners)


@bp.route('/<competition_id>/publish', methods=['POST'])
@login_required
@admin_required
def publish_competition(competition_id):
    """Publish competition to accept submissions."""
    competition = Competition.find_by_id(competition_id)
    if not competition:
        flash('Competition not found.', 'danger')
        return redirect(url_for('competitions_admin.list_competitions'))
    
    if competition['status'] != 'draft':
        flash('Competition cannot be published from current status.', 'warning')
        return redirect(url_for('competitions_admin.view_competition', competition_id=competition_id))
    
    Competition.update_status(competition_id, 'accepting_submissions')
    flash('Competition published successfully! Authors can now submit entries.', 'success')
    
    return redirect(url_for('competitions_admin.view_competition', competition_id=competition_id))


@bp.route('/<competition_id>/close', methods=['POST'])
@login_required
@admin_required
def close_competition(competition_id):
    """Close competition submissions."""
    competition = Competition.find_by_id(competition_id)
    if not competition:
        flash('Competition not found.', 'danger')
        return redirect(url_for('competitions_admin.list_competitions'))
    
    if competition['status'] != 'accepting_submissions':
        flash('Competition is not accepting submissions.', 'warning')
        return redirect(url_for('competitions_admin.view_competition', competition_id=competition_id))
    
    Competition.update_status(competition_id, 'closed')
    flash('Competition closed. No more submissions will be accepted.', 'success')
    
    return redirect(url_for('competitions_admin.view_competition', competition_id=competition_id))


@bp.route('/<competition_id>/evaluate', methods=['POST'])
@login_required
@admin_required
def start_evaluation(competition_id):
    """Start AI evaluation of all submissions."""
    competition = Competition.find_by_id(competition_id)
    if not competition:
        flash('Competition not found.', 'danger')
        return redirect(url_for('competitions_admin.list_competitions'))
    
    if competition['status'] not in ['closed', 'evaluating']:
        flash('Competition must be closed before evaluation.', 'warning')
        return redirect(url_for('competitions_admin.view_competition', competition_id=competition_id))
    
    # Update status to evaluating
    Competition.update_status(competition_id, 'evaluating')
    
    # Get all submissions
    submissions = CompetitionSubmission.find_by_competition(competition_id)
    
    evaluated_count = 0
    for submission in submissions:
        # Check if already evaluated
        existing_eval = AIEvaluation.find_by_submission(str(submission['_id']))
        if existing_eval:
            continue
        
        # Evaluate submission
        try:
            result = evaluate_manuscript(
                manuscript_title=submission['manuscript_title'],
                synopsis=submission['synopsis'],
                word_count=submission['word_count'],
                genre=submission['genre'],
                criteria=competition['evaluation_criteria']
            )
            
            AIEvaluation.create(
                submission_id=str(submission['_id']),
                competition_id=competition_id,
                ai_model_version=result['model_version'],
                criteria_scores=result['criteria_scores'],
                overall_score=result['overall_score'],
                strengths_identified=result['strengths'],
                weaknesses_identified=result['weaknesses'],
                detailed_feedback=result['detailed_feedback'],
                confidence_score=result['confidence_score'],
                processing_time_seconds=result['processing_time']
            )
            
            # Update submission status
            CompetitionSubmission.update_status(str(submission['_id']), 'under_review')
            evaluated_count += 1
            
        except Exception as e:
            flash(f'Error evaluating submission {submission["manuscript_title"]}: {str(e)}', 'warning')
    
    # Update competition status to admin_review
    Competition.update_status(competition_id, 'admin_review')
    
    flash(f'Evaluation completed! {evaluated_count} submissions evaluated.', 'success')
    return redirect(url_for('competitions_admin.view_competition', competition_id=competition_id))


@bp.route('/<competition_id>/select-winners', methods=['GET', 'POST'])
@login_required
@admin_required
def select_winners(competition_id):
    """Select and announce winners."""
    competition = Competition.find_by_id(competition_id)
    if not competition:
        flash('Competition not found.', 'danger')
        return redirect(url_for('competitions_admin.list_competitions'))
    
    if competition['status'] != 'admin_review':
        flash('Competition must be in admin review status.', 'warning')
        return redirect(url_for('competitions_admin.view_competition', competition_id=competition_id))
    
    if request.method == 'POST':
        # Get selected winners
        winner_ids = request.form.getlist('winner_ids')
        
        if not winner_ids:
            flash('Please select at least one winner.', 'warning')
            return redirect(url_for('competitions_admin.select_winners', competition_id=competition_id))
        
        # Create winner records
        prize_keys = ['first_place', 'second_place', 'third_place']
        for idx, submission_id in enumerate(winner_ids[:3]):  # Top 3 winners
            submission = CompetitionSubmission.find_by_id(submission_id)
            evaluation = AIEvaluation.find_by_submission(submission_id)
            
            if not submission or not evaluation:
                continue
            
            rank = idx + 1
            prize = competition['prize_structure'].get(prize_keys[idx], 'Recognition')
            
            CompetitionWinner.create(
                competition_id=competition_id,
                submission_id=submission_id,
                author_id=str(submission['author_id']),
                rank_position=rank,
                final_score=evaluation['overall_score'],
                prize_awarded=prize,
                winner_feedback=evaluation['detailed_feedback']
            )
            
            # Award badges to winners
            badge_details = {
                1: {'name': 'Gold Winner 🥇', 'icon': '🏆', 'type': 'competition_winner'},
                2: {'name': 'Silver Winner 🥈', 'icon': '🥈', 'type': 'competition_winner'},
                3: {'name': 'Bronze Winner 🥉', 'icon': '🥉', 'type': 'competition_winner'}
            }
            
            badge_info = badge_details.get(rank)
            if badge_info:
                User.award_badge(
                    user_id=str(submission['author_id']),
                    badge_type=badge_info['type'],
                    badge_name=f"{badge_info['name']} - {competition['title']}",
                    badge_icon=badge_info['icon'],
                    competition_id=competition_id
                )
            
            # Update competition stats
            user = User.find_by_id(str(submission['author_id']))
            current_stats = user.get('competition_stats', {})
            
            User.update_competition_stats(
                user_id=str(submission['author_id']),
                stat_updates={
                    'total_wins': current_stats.get('total_wins', 0) + 1,
                    'total_finalist': current_stats.get('total_finalist', 0) + 1,
                    'best_rank': rank
                }
            )
            
            # Update submission status
            CompetitionSubmission.update_status(submission_id, 'winner')
        
        # Update all non-winner submissions to participant status
        all_submissions = CompetitionSubmission.find_by_competition(competition_id)
        for sub in all_submissions:
            if str(sub['_id']) not in winner_ids and sub['submission_status'] != 'winner':
                CompetitionSubmission.update_status(str(sub['_id']), 'participant')
        
        # Update competition status to completed
        Competition.update_status(competition_id, 'completed')
        
        flash('Winners announced successfully!', 'success')
        return redirect(url_for('competitions_admin.view_competition', competition_id=competition_id))
    
    # GET: Show evaluation results for winner selection
    evaluations = AIEvaluation.find_by_competition(competition_id)
    
    # Enrich with submission and author data
    for evaluation in evaluations:
        submission = CompetitionSubmission.find_by_id(str(evaluation['submission_id']))
        author = User.find_by_id(str(submission['author_id']))
        evaluation['submission'] = submission
        evaluation['author'] = author
    
    return render_template('admin/competitions/select_winners.html',
                         competition=competition,
                         evaluations=evaluations)


@bp.route('/<competition_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_competition(competition_id):
    """Edit competition details."""
    competition = Competition.find_by_id(competition_id)
    if not competition:
        flash('Competition not found.', 'danger')
        return redirect(url_for('competitions_admin.list_competitions'))
    
    # Only allow editing draft competitions
    if competition['status'] != 'draft':
        flash('Cannot edit published competition.', 'warning')
        return redirect(url_for('competitions_admin.view_competition', competition_id=competition_id))
    
    if request.method == 'POST':
        update_data = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'genre_categories': request.form.getlist('genre_categories'),
            'submission_start_date': datetime.strptime(request.form.get('submission_start_date'), '%Y-%m-%d'),
            'submission_end_date': datetime.strptime(request.form.get('submission_end_date'), '%Y-%m-%d'),
            'max_submissions_per_author': int(request.form.get('max_submissions_per_author', 1)),
            'entry_fee_amount': float(request.form.get('entry_fee_amount', 0))
        }
        
        if request.form.get('winner_announcement_date'):
            update_data['winner_announcement_date'] = datetime.strptime(
                request.form.get('winner_announcement_date'), '%Y-%m-%d'
            )
        
        Competition.update(competition_id, update_data)
        flash('Competition updated successfully!', 'success')
        return redirect(url_for('competitions_admin.view_competition', competition_id=competition_id))
    
    genres = ['Action', 'Adventure', 'Art', 'Biography', 'Business',
              'Children', 'Cooking', 'Crime', 'Dystopian', 'Education',
              'Essays', 'Fantasy', 'Fiction', 'Graphic Novel', 'Health',
              'Historical Fiction', 'History', 'Horror', 'Literary Fiction',
              'Memoir', 'Middle Grade', 'Mystery', 'Non-Fiction', 'Philosophy',
              'Poetry', 'Politics', 'Religion', 'Romance', 'Science',
              'Science Fiction', 'Self-Help', 'Technology', 'Thriller',
              'Travel', 'True Crime', 'Young Adult']
    
    return render_template('admin/competitions/edit.html', 
                         competition=competition,
                         genres=genres)
