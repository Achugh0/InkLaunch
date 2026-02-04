"""Article routes."""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from app.models import Article, User

bp = Blueprint('articles', __name__, url_prefix='/articles')


@bp.route('/')
def list_articles():
    """List all published articles."""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    per_page = 20
    
    skip = (page - 1) * per_page
    
    # Filter by category if provided
    if category:
        articles = Article.find_by_category(category, skip=skip, limit=per_page)
    else:
        articles = Article.find_published(skip=skip, limit=per_page)
    
    # Enrich with author info
    for article in articles:
        author = User.find_by_id(str(article['author_id']))
        article['author'] = author
    
    if request.is_json:
        return jsonify({
            'articles': [{
                'id': str(a['_id']),
                'title': a['title'],
                'excerpt': a.get('excerpt'),
                'category': a.get('category'),
                'author': a['author']['full_name'] if a['author'] else 'Unknown',
                'published_at': a['published_at'].isoformat() if a.get('published_at') else None
            } for a in articles]
        }), 200
    
    return render_template('articles/list.html', articles=articles, current_category=category)


@bp.route('/<slug>')
def get_article(slug):
    """Get article by slug."""
    article = Article.find_by_slug(slug)
    
    if not article:
        if request.is_json:
            return jsonify({'error': 'Article not found'}), 404
        flash('Article not found', 'error')
        return redirect(url_for('articles.list_articles'))
    
    # Get author info
    author = User.find_by_id(str(article['author_id']))
    article['author'] = author
    
    if request.is_json:
        return jsonify({
            'id': str(article['_id']),
            'title': article['title'],
            'content': article['content'],
            'category': article.get('category'),
            'author': {
                'name': author['full_name'],
                'bio': author.get('bio')
            } if author else None,
            'published_at': article['published_at'].isoformat() if article.get('published_at') else None
        }), 200
    
    return render_template('articles/detail.html', article=article)
