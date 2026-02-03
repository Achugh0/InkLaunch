"""Tool routes."""
from flask import Blueprint, request, jsonify, render_template, session, flash, redirect, url_for

bp = Blueprint('tools', __name__, url_prefix='/tools')


@bp.route('/')
def list_tools():
    """List available tools."""
    tools = [
        {
            'id': 'metadata-checker',
            'name': 'Metadata Checker',
            'description': 'Validate and optimize your book metadata for better discoverability',
            'url': url_for('tools.metadata_checker')
        },
        {
            'id': 'isbn-validator',
            'name': 'ISBN Validator',
            'description': 'Validate ISBN-10 and ISBN-13 format',
            'url': url_for('tools.isbn_validator')
        }
    ]
    
    if request.is_json:
        return jsonify({'tools': tools}), 200
    
    return render_template('tools/list.html', tools=tools)


@bp.route('/metadata-checker', methods=['GET', 'POST'])
def metadata_checker():
    """Metadata checker tool."""
    if request.method == 'GET':
        return render_template('tools/metadata_checker.html')
    
    data = request.get_json() if request.is_json else request.form
    
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    
    results = {
        'title_length': len(title),
        'title_optimal': 60 <= len(title) <= 80,
        'description_length': len(description),
        'description_optimal': len(description) >= 150,
        'recommendations': []
    }
    
    if not results['title_optimal']:
        if len(title) < 60:
            results['recommendations'].append('Title is too short. Optimal length is 60-80 characters.')
        else:
            results['recommendations'].append('Title is too long. Optimal length is 60-80 characters.')
    
    if not results['description_optimal']:
        results['recommendations'].append('Description should be at least 150 characters for better SEO.')
    
    # Check for keywords
    if description.lower().count(title.lower().split()[0] if title else '') == 0:
        results['recommendations'].append('Consider including key words from the title in the description.')
    
    if not results['recommendations']:
        results['recommendations'].append('Your metadata looks good!')
    
    if request.is_json:
        return jsonify(results), 200
    
    return render_template('tools/metadata_checker.html', results=results, title=title, description=description)


@bp.route('/isbn-validator', methods=['GET', 'POST'])
def isbn_validator():
    """ISBN validator tool."""
    if request.method == 'GET':
        return render_template('tools/isbn_validator.html')
    
    data = request.get_json() if request.is_json else request.form
    isbn = data.get('isbn', '').strip().replace('-', '').replace(' ', '')
    
    # Fetch book details from Open Library API (free and legal)
    book_details = None
    if isbn:
        try:
            import requests
            # Try Open Library API first
            response = requests.get(f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data', timeout=5)
            if response.status_code == 200:
                data_json = response.json()
                if f'ISBN:{isbn}' in data_json:
                    book_info = data_json[f'ISBN:{isbn}']
                    book_details = {
                        'title': book_info.get('title', ''),
                        'authors': [author.get('name', '') for author in book_info.get('authors', [])],
                        'publishers': [pub.get('name', '') for pub in book_info.get('publishers', [])],
                        'publish_date': book_info.get('publish_date', ''),
                        'number_of_pages': book_info.get('number_of_pages', ''),
                        'cover_url': book_info.get('cover', {}).get('medium', ''),
                        'subjects': [subj.get('name', '') for subj in book_info.get('subjects', [])][:5]
                    }
        except Exception as e:
            # If API fails, continue with validation only
            pass
    
    def validate_isbn_10(isbn):
        """Validate ISBN-10 format."""
        if len(isbn) != 10:
            return False
        try:
            sum_val = 0
            for i in range(9):
                sum_val += int(isbn[i]) * (10 - i)
            checksum = isbn[9]
            if checksum.upper() == 'X':
                sum_val += 10
            else:
                sum_val += int(checksum)
            return sum_val % 11 == 0
        except:
            return False
    
    def validate_isbn_13(isbn):
        """Validate ISBN-13 format."""
        if len(isbn) != 13:
            return False
        try:
            sum_val = 0
            for i in range(12):
                multiplier = 1 if i % 2 == 0 else 3
                sum_val += int(isbn[i]) * multiplier
            checksum = (10 - (sum_val % 10)) % 10
            return checksum == int(isbn[12])
        except:
            return False
    
    is_valid = False
    isbn_type = None
    
    if len(isbn) == 10:
        is_valid = validate_isbn_10(isbn)
        isbn_type = 'ISBN-10'
    elif len(isbn) == 13:
        is_valid = validate_isbn_13(isbn)
        isbn_type = 'ISBN-13'
    
    results = {
        'isbn': isbn,
        'is_valid': is_valid,
        'type': isbn_type,
        'message': f'Valid {isbn_type}' if is_valid else 'Invalid ISBN format',
        'book_details': book_details
    }
    
    if request.is_json:
        return jsonify(results), 200
    
    return render_template('tools/isbn_validator.html', results=results, isbn=isbn)
