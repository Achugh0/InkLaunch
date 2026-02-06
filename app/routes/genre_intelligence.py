from flask import Blueprint, render_template, request
from app.services.genre_intelligence_service import (
    genre_suggestion_engine, competitive_analysis, market_trends,
    keyword_recommendations, cover_style_guidance, pricing_recommendations,
    marketing_platform_suggestions
)

genre_intel_bp = Blueprint('genre_intel', __name__, url_prefix='/tools')

@genre_intel_bp.route('/genre-intelligence', methods=['GET', 'POST'])
def genre_intelligence():
    # Placeholder: call all 7 tools with mock data
    context = {}
    if request.method == 'POST':
        excerpt = request.form.get('excerpt', '')
        context['suggestions'] = genre_suggestion_engine(excerpt)
        context['competitive'] = competitive_analysis(excerpt)
        context['trends'] = market_trends(excerpt)
        context['keywords'] = keyword_recommendations(excerpt)
        context['cover'] = cover_style_guidance(excerpt)
        context['pricing'] = pricing_recommendations(excerpt)
        context['marketing'] = marketing_platform_suggestions(excerpt)
    return render_template('tools/genre_intelligence.html', **context)
