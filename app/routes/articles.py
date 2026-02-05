"""Article routes."""
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from app.models import Article, User

bp = Blueprint('articles', __name__, url_prefix='/articles')


@bp.route('/')
def list_articles():
    """List all published articles."""
    try:
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
            try:
                author = User.find_by_id(str(article['author_id']))
                article['author'] = author if author else {'full_name': 'InkLaunch Team', 'bio': ''}
            except Exception as e:
                # If author not found, use placeholder
                article['author'] = {'full_name': 'InkLaunch Team', 'bio': ''}
        
        if request.is_json:
            return jsonify({
                'articles': [{
                    'id': str(a['_id']),
                    'title': a['title'],
                    'excerpt': a.get('excerpt'),
                    'category': a.get('category'),
                    'author': a['author']['full_name'] if a.get('author') else 'Unknown',
                    'published_at': a['published_at'].isoformat() if a.get('published_at') and hasattr(a['published_at'], 'isoformat') else str(a.get('published_at', ''))
                } for a in articles]
            }), 200
        
        return render_template('articles/list.html', articles=articles, current_category=category)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in list_articles: {error_details}")
        flash(f'Error loading articles: {str(e)}', 'error')
        return render_template('articles/list.html', articles=[], current_category=None)


@bp.route('/<slug>')
def get_article(slug):
    """Get article by slug."""
    try:
        article = Article.find_by_slug(slug)
        
        if not article:
            if request.is_json:
                return jsonify({'error': 'Article not found'}), 404
            flash('Article not found', 'error')
            return redirect(url_for('articles.list_articles'))
        
        # Get author info
        try:
            author = User.find_by_id(str(article['author_id']))
            article['author'] = author
        except:
            article['author'] = {'full_name': 'InkLaunch Team', 'bio': ''}
        
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
    except Exception as e:
        flash(f'Error loading article: {str(e)}', 'error')
        return redirect(url_for('articles.list_articles'))
