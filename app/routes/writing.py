"""Writing and creative tools routes."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models import (Book, User, TitleTest, CoverFeedback, WordCountTracker, 
                        WritingPrompt)
from bson import ObjectId
from datetime import datetime
import random

writing_bp = Blueprint('writing', __name__, url_prefix='/writing')


@writing_bp.route('/')
def index():
    """Writing tools index page."""
    user = User.find_by_id(session.get('user_id')) if 'user_id' in session else None
    return render_template('writing/index.html', user=user)


@writing_bp.route('/title-tester', methods=['GET', 'POST'])
def title_tester():
    """Test book titles with community polling."""
    if 'user_id' not in session:
        flash('Please log in to access this feature.', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        genre = request.form.get('genre')
        description = request.form.get('description', '')
        title_options = []
        
        # Get up to 5 title options
        for i in range(1, 6):
            title = request.form.get(f'title_{i}')
            if title:
                title_options.append(title)
        
        if len(title_options) < 2:
            flash('Please provide at least 2 title options.', 'warning')
            return redirect(url_for('writing.title_tester'))
        
        # Check for duplicate titles
        duplicate_warnings = []
        for title in title_options:
            duplicates = TitleTest.check_duplicate_titles(title)
            if duplicates:
                duplicate_warnings.append({
                    'title': title,
                    'similar_books': duplicates
                })
        
        # Create title test
        test_id = TitleTest.create(
            author_id=session['user_id'],
            book_genre=genre,
            title_options=title_options,
            description=description
        )
        
        if duplicate_warnings:
            flash(f'Warning: Some titles have similar existing books. Check the results page.', 'warning')
        
        flash('Title test created! Share with the community to get votes.', 'success')
        return redirect(url_for('writing.view_title_test', test_id=str(test_id)))
    
    # GET request
    user = User.find_by_id(session['user_id'])
    active_tests = TitleTest.find_active_tests()
    
    return render_template('writing/title_tester.html', 
                         user=user,
                         active_tests=active_tests)


@writing_bp.route('/title-tester/<test_id>')
def view_title_test(test_id):
    """View a title test and its results."""
    test = TitleTest.find_by_id(test_id)
    if not test:
        flash('Title test not found.', 'danger')
        return redirect(url_for('writing.title_tester'))
    
    author = User.find_by_id(str(test['author_id']))
    user = User.find_by_id(session.get('user_id')) if 'user_id' in session else None
    
    return render_template('writing/view_title_test.html', 
                         test=test,
                         author=author,
                         user=user)


@writing_bp.route('/title-tester/<test_id>/vote/<int:title_index>', methods=['POST'])
def vote_title(test_id, title_index):
    """Vote on a title option."""
    if 'user_id' not in session:
        flash('Please log in to vote.', 'warning')
        return redirect(url_for('auth.login'))
    
    test = TitleTest.find_by_id(test_id)
    if not test:
        return jsonify({'error': 'Test not found'}), 404
    
    if title_index >= len(test['title_options']):
        return jsonify({'error': 'Invalid title index'}), 400
    
    # Record vote
    TitleTest.vote(test_id, title_index)
    
    flash('Vote recorded!', 'success')
    return redirect(url_for('writing.view_title_test', test_id=test_id))


@writing_bp.route('/cover-feedback', methods=['GET', 'POST'])
def cover_feedback():
    """Get community feedback on book covers."""
    if 'user_id' not in session:
        flash('Please log in to access this feature.', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        cover_url = request.form.get('cover_url')
        genre = request.form.get('genre')
        description = request.form.get('description', '')
        
        if not cover_url:
            flash('Please provide a cover image URL.', 'warning')
            return redirect(url_for('writing.cover_feedback'))
        
        CoverFeedback.create(
            author_id=session['user_id'],
            cover_url=cover_url,
            book_genre=genre,
            description=description
        )
        
        flash('Cover submitted for feedback!', 'success')
        return redirect(url_for('writing.cover_feedback'))
    
    # GET request
    user = User.find_by_id(session['user_id'])
    recent_covers = CoverFeedback.find_recent(limit=20)
    
    # Enrich with author data
    for cover in recent_covers:
        cover['author'] = User.find_by_id(str(cover['author_id']))
    
    return render_template('writing/cover_feedback.html', 
                         user=user,
                         recent_covers=recent_covers)


@writing_bp.route('/cover-feedback/<feedback_id>/rate', methods=['POST'])
def rate_cover(feedback_id):
    """Rate a cover design."""
    if 'user_id' not in session:
        flash('Please log in to provide feedback.', 'warning')
        return redirect(url_for('auth.login'))
    
    rating = int(request.form.get('rating', 0))
    comment = request.form.get('comment', '')
    
    if rating < 1 or rating > 5:
        flash('Rating must be between 1 and 5.', 'warning')
        return redirect(url_for('writing.cover_feedback'))
    
    CoverFeedback.add_feedback(
        feedback_id=feedback_id,
        user_id=session['user_id'],
        rating=rating,
        comment=comment
    )
    
    flash('Feedback submitted!', 'success')
    return redirect(url_for('writing.cover_feedback'))


@writing_bp.route('/word-count-tracker', methods=['GET', 'POST'])
def word_count_tracker():
    """Track writing progress with word counts."""
    if 'user_id' not in session:
        flash('Please log in to access this feature.', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create':
            book_title = request.form.get('book_title')
            target_word_count = int(request.form.get('target_word_count', 50000))
            is_public = request.form.get('is_public') == 'on'
            
            WordCountTracker.create(
                author_id=session['user_id'],
                book_title=book_title,
                target_word_count=target_word_count,
                is_public=is_public
            )
            
            flash('Word count tracker created!', 'success')
        
        elif action == 'add_entry':
            tracker_id = request.form.get('tracker_id')
            word_count = int(request.form.get('word_count'))
            notes = request.form.get('notes', '')
            
            WordCountTracker.add_entry(tracker_id, word_count, notes)
            flash('Progress updated!', 'success')
        
        return redirect(url_for('writing.word_count_tracker'))
    
    # GET request
    user = User.find_by_id(session['user_id'])
    my_trackers = WordCountTracker.find_by_author(session['user_id'])
    public_trackers = WordCountTracker.find_public_trackers(limit=10)
    
    # Enrich public trackers with author data
    for tracker in public_trackers:
        tracker['author'] = User.find_by_id(str(tracker['author_id']))
    
    return render_template('writing/word_count_tracker.html', 
                         user=user,
                         my_trackers=my_trackers,
                         public_trackers=public_trackers)


@writing_bp.route('/writing-prompts')
def writing_prompts():
    """Browse and use writing prompts."""
    genre = request.args.get('genre')
    
    # Get a random prompt
    prompt = WritingPrompt.get_random_prompt(genre=genre)
    
    if prompt:
        WritingPrompt.increment_usage(str(prompt['_id']))
    
    user = User.find_by_id(session.get('user_id')) if 'user_id' in session else None
    
    genres = ['Fantasy', 'Science Fiction', 'Romance', 'Mystery', 'Thriller', 
              'Horror', 'Literary Fiction', 'Historical', 'Contemporary']
    
    return render_template('writing/writing_prompts.html', 
                         user=user,
                         prompt=prompt,
                         genres=genres,
                         selected_genre=genre)


@writing_bp.route('/character-name-generator')
def character_name_generator():
    """Generate character names based on culture and genre."""
    culture = request.args.get('culture', 'English')
    gender = request.args.get('gender', 'any')
    genre = request.args.get('genre', 'Fantasy')
    
    # Sample name databases (in production, this would be a comprehensive database)
    name_database = {
        'English': {
            'male': ['James', 'William', 'Henry', 'Thomas', 'Edward', 'Charles'],
            'female': ['Elizabeth', 'Margaret', 'Catherine', 'Anne', 'Mary', 'Jane']
        },
        'Fantasy': {
            'male': ['Aethor', 'Draven', 'Kael', 'Theron', 'Zephyr', 'Aldric'],
            'female': ['Lyra', 'Seraphina', 'Elara', 'Morgana', 'Aria', 'Isolde']
        },
        'SciFi': {
            'male': ['Zane', 'Orion', 'Nova', 'Cyrus', 'Atlas', 'Phoenix'],
            'female': ['Lyra', 'Nova', 'Stella', 'Nebula', 'Astra', 'Vega']
        }
    }
    
    # Generate random names
    generated_names = []
    culture_names = name_database.get(culture, name_database['English'])
    
    if gender == 'any':
        all_names = culture_names.get('male', []) + culture_names.get('female', [])
    else:
        all_names = culture_names.get(gender, [])
    
    if all_names:
        generated_names = random.sample(all_names, min(10, len(all_names)))
    
    user = User.find_by_id(session.get('user_id')) if 'user_id' in session else None
    
    return render_template('writing/character_name_generator.html', 
                         user=user,
                         generated_names=generated_names,
                         culture=culture,
                         gender=gender,
                         genre=genre)


@writing_bp.route('/manuscript-formatter', methods=['GET', 'POST'])
def manuscript_formatter():
    """Format manuscript with proper styling."""
    if 'user_id' not in session:
        flash('Please log in to access this feature.', 'warning')
        return redirect(url_for('auth.login'))
    
    formatted_text = None
    
    if request.method == 'POST':
        manuscript_text = request.form.get('manuscript_text', '')
        format_type = request.form.get('format_type', 'standard')
        
        # Apply basic formatting
        lines = manuscript_text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
            
            # Check if it's a chapter heading
            if line.upper().startswith('CHAPTER'):
                formatted_lines.append(f'<h2 class="text-center mt-5 mb-4">{line}</h2>')
            # Check if it's a scene break
            elif line == '***' or line == '###':
                formatted_lines.append('<hr class="my-4" style="width: 30%; margin: auto;">')
            else:
                # Regular paragraph
                formatted_lines.append(f'<p class="mb-3" style="text-indent: 2em;">{line}</p>')
        
        formatted_text = '\n'.join(formatted_lines)
    
    user = User.find_by_id(session['user_id'])
    
    return render_template('writing/manuscript_formatter.html', 
                         user=user,
                         formatted_text=formatted_text)


@writing_bp.route('/blurb-generator', methods=['GET', 'POST'])
def blurb_generator():
    """AI-assisted book blurb generator."""
    if 'user_id' not in session:
        flash('Please log in to access this feature.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.find_by_id(session['user_id'])
    generated_blurb = None
    
    if request.method == 'POST':
        # Check usage limit (3 free per month)
        # In production, track this in user model
        
        book_title = request.form.get('book_title')
        genre = request.form.get('genre')
        plot_summary = request.form.get('plot_summary')
        tone = request.form.get('tone', 'exciting')
        
        # Simple template-based generation (in production, use OpenAI API)
        templates = {
            'exciting': f"In {book_title}, {plot_summary} Packed with action and suspense, this {genre} novel will keep you on the edge of your seat!",
            'mysterious': f"{plot_summary} In {book_title}, nothing is as it seems. A gripping {genre} that will leave you guessing until the very end.",
            'emotional': f"{book_title} is a heartfelt {genre} story about {plot_summary} A touching tale that will stay with you long after the final page."
        }
        
        generated_blurb = templates.get(tone, templates['exciting'])
        flash('Blurb generated! (1 of 3 free generations this month)', 'info')
    
    return render_template('writing/blurb_generator.html', 
                         user=user,
                         generated_blurb=generated_blurb)


@writing_bp.route('/genre-checker', methods=['GET', 'POST'])
def genre_checker():
    """Check if manuscript matches genre conventions."""
    if 'user_id' not in session:
        flash('Please log in to access this feature.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = User.find_by_id(session['user_id'])
    analysis_result = None
    
    if request.method == 'POST':
        genre = request.form.get('genre')
        manuscript_sample = request.form.get('manuscript_sample')
        
        # Simple keyword-based analysis (in production, use AI)
        genre_conventions = {
            'Romance': ['love', 'heart', 'kiss', 'relationship', 'passion'],
            'Mystery': ['clue', 'detective', 'murder', 'investigate', 'suspect'],
            'Fantasy': ['magic', 'sword', 'kingdom', 'quest', 'dragon'],
            'Science Fiction': ['space', 'technology', 'future', 'alien', 'robot']
        }
        
        keywords = genre_conventions.get(genre, [])
        found_keywords = [kw for kw in keywords if kw.lower() in manuscript_sample.lower()]
        
        match_percentage = (len(found_keywords) / len(keywords)) * 100 if keywords else 0
        
        analysis_result = {
            'genre': genre,
            'match_percentage': round(match_percentage, 1),
            'found_keywords': found_keywords,
            'suggestions': []
        }
        
        if match_percentage < 40:
            analysis_result['suggestions'].append(f'Consider adding more {genre}-specific elements')
        if match_percentage >= 70:
            analysis_result['suggestions'].append(f'Good job! Your manuscript aligns well with {genre} conventions')
    
    return render_template('writing/genre_checker.html', 
                         user=user,
                         analysis_result=analysis_result)
