from flask import Blueprint, render_template, request
from app.services.genre_service import ai_genre_suggestion, get_genre_taxonomy

genre_selector_bp = Blueprint('genre_selector', __name__, url_prefix='/tools')

@genre_selector_bp.route('/genre-selector', methods=['GET', 'POST'])
def genre_selector():
    genres = get_genre_taxonomy()
    ai_suggestions = []
    excerpt = ''
    if request.method == 'POST':
        excerpt = request.form.get('excerpt', '')
        if excerpt:
            ai_suggestions = ai_genre_suggestion(excerpt)
    return render_template('tools/genre_selector.html', genres=genres, ai_suggestions=ai_suggestions, excerpt=excerpt)
