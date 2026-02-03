"""Competition routes."""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash, current_app
from app.models import CompetitionPeriod, Nomination, Book, User, AIBookReview
from app.services.ai_service import AIService
from app import mongo
from bson import ObjectId
from datetime import datetime

bp = Blueprint('competitions', __name__, url_prefix='/competitions')


@bp.route('/')
def list_competitions():
    """List all competitions."""
    competitions = list(mongo.db.competition_periods.find().sort('year', -1).sort('month', -1))
    
    return render_template('competitions/list.html', competitions=competitions)


@bp.route('/current')
def current_competition():
    """Get current active competition."""
    competition = CompetitionPeriod.find_active()
    
    if not competition:
        if request.is_json:
            return jsonify({'message': 'No active competition'}), 404
        flash('No active competition at the moment', 'info')
        return redirect(url_for('competitions.list_competitions'))
    
    # Get nominations for this period
    nominations = Nomination.find_by_period(str(competition['_id']))
    
    # Enrich nominations
    for nom in nominations:
        book = Book.find_by_id(str(nom['book_id']))
        user = User.find_by_id(str(nom['user_id']))
        nom['book'] = book
        nom['user'] = user
    
    if request.is_json:
        return jsonify({
            'id': str(competition['_id']),
            'month': competition['month'],
            'year': competition['year'],
            'status': competition['status'],
            'nominations_count': len(nominations)
        }), 200
    
    return render_template('competitions/current.html', competition=competition, nominations=nominations)


@bp.route('/nominate', methods=['GET', 'POST'])
def nominate():
    """Submit a nomination."""
    user_id = session.get('user_id')
    
    if not user_id:
        if request.is_json:
            return jsonify({'error': 'Authentication required'}), 401
        flash('Please log in to submit a nomination', 'error')
        return redirect(url_for('auth.login'))
    
    # Get active competition
    competition = CompetitionPeriod.find_active()
    
    if not competition:
        if request.is_json:
            return jsonify({'error': 'No active competition'}), 404
        flash('No active competition at the moment', 'info')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'GET':
        # Get user's books
        my_books = Book.find_by_user(user_id)
        
        # Check if already nominated
        existing = Nomination.find_by_user_and_period(user_id, str(competition['_id']))
        
        return render_template('competitions/nominate.html', 
                             competition=competition, 
                             books=my_books,
                             existing_nomination=existing)
    
    data = request.get_json() if request.is_json else request.form
    
    book_id = data.get('book_id')
    nomination_statement = data.get('nomination_statement', '').strip()
    
    # Validation
    if not book_id or not nomination_statement:
        if request.is_json:
            return jsonify({'error': 'Book and nomination statement are required'}), 400
        flash('Book and nomination statement are required', 'error')
        return redirect(url_for('competitions.nominate'))
    
    min_length = current_app.config['NOMINATION_STATEMENT_MIN_LENGTH']
    max_length = current_app.config['NOMINATION_STATEMENT_MAX_LENGTH']
    
    if len(nomination_statement) < min_length or len(nomination_statement) > max_length:
        if request.is_json:
            return jsonify({'error': f'Nomination statement must be between {min_length} and {max_length} characters'}), 400
        flash(f'Nomination statement must be between {min_length} and {max_length} characters', 'error')
        return redirect(url_for('competitions.nominate'))
    
    # Check if book belongs to user
    book = Book.find_by_id(book_id)
    if not book or str(book['user_id']) != user_id:
        if request.is_json:
            return jsonify({'error': 'Invalid book selection'}), 400
        flash('Invalid book selection', 'error')
        return redirect(url_for('competitions.nominate'))
    
    # Check if already nominated
    existing = Nomination.find_by_user_and_period(user_id, str(competition['_id']))
    if existing:
        if request.is_json:
            return jsonify({'error': 'You have already submitted a nomination for this period'}), 400
        flash('You have already submitted a nomination for this period', 'error')
        return redirect(url_for('competitions.current_competition'))
    
    # Create nomination
    nomination_id = Nomination.create(str(competition['_id']), book_id, user_id, nomination_statement)
    
    if request.is_json:
        return jsonify({
            'message': 'Nomination submitted successfully',
            'nomination_id': str(nomination_id)
        }), 201
    
    flash('Nomination submitted successfully!', 'success')
    return redirect(url_for('competitions.current_competition'))


@bp.route('/admin/trigger-ai-review/<nomination_id>', methods=['POST'])
def trigger_ai_review(nomination_id):
    """Trigger AI review for a nomination (admin only)."""
    user_role = session.get('user_role')
    
    if user_role != 'admin':
        if request.is_json:
            return jsonify({'error': 'Admin access required'}), 403
        flash('Admin access required', 'error')
        return redirect(url_for('main.index'))
    
    nomination = mongo.db.competition_nominations.find_one({'_id': ObjectId(nomination_id)})
    
    if not nomination:
        if request.is_json:
            return jsonify({'error': 'Nomination not found'}), 404
        flash('Nomination not found', 'error')
        return redirect(url_for('admin.dashboard'))
    
    # Get book details
    book = Book.find_by_id(str(nomination['book_id']))
    user = User.find_by_id(str(nomination['user_id']))
    
    # Call AI service
    try:
        ai_service = AIService()
        review_data = ai_service.review_book(book, nomination, user)
        
        # Store AI review
        AIBookReview.create(nomination_id, str(book['_id']), review_data)
        
        # Update nomination status
        mongo.db.competition_nominations.update_one(
            {'_id': ObjectId(nomination_id)},
            {'$set': {'status': 'under_review'}}
        )
        
        if request.is_json:
            return jsonify({
                'message': 'AI review completed successfully',
                'review': review_data
            }), 200
        
        flash('AI review completed successfully', 'success')
        return redirect(url_for('competitions.current_competition'))
        
    except Exception as e:
        if request.is_json:
            return jsonify({'error': str(e)}), 500
        flash(f'AI review failed: {str(e)}', 'error')
        return redirect(url_for('competitions.current_competition'))
