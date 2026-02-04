"""Tool routes."""
from flask import Blueprint, request, jsonify, render_template, session, flash, redirect, url_for

bp = Blueprint('tools', __name__, url_prefix='/tools')


@bp.route('/')
def list_tools():
    """List available tools."""
    tools = [
        {
            'id': 'cover-designer',
            'name': 'Cover Size Calculator',
            'description': 'Calculate exact cover dimensions for Amazon KDP ebooks and paperbacks',
            'url': url_for('tools.cover_designer')
        },
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
    """Enhanced metadata checker with EPUB analysis."""
    if request.method == 'GET':
        return render_template('tools/metadata_checker.html')
    
    # Check if file upload or form data
    if 'epub_file' in request.files:
        file = request.files['epub_file']
        if file and file.filename.endswith('.epub'):
            return analyze_epub_metadata(file)
    
    # Regular form-based checking
    data = request.get_json() if request.is_json else request.form
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    author = data.get('author', '').strip()
    keywords = data.get('keywords', '').strip()
    categories = data.get('categories', '').strip()
    
    report = generate_metadata_report(title, description, author, keywords, categories)
    
    return render_template('tools/metadata_checker.html', report=report)


def analyze_epub_metadata(file):
    """Analyze EPUB file metadata comprehensively."""
    import zipfile
    import xml.etree.ElementTree as ET
    from io import BytesIO
    
    report = {
        'file_uploaded': True,
        'filename': file.filename,
        'issues': [],
        'warnings': [],
        'successes': [],
        'recommendations': [],
        'metadata': {},
        'scores': {}
    }
    
    try:
        # Read EPUB (it's a ZIP file)
        epub_data = BytesIO(file.read())
        with zipfile.ZipFile(epub_data, 'r') as epub:
            # Find and parse OPF file (contains metadata)
            opf_path = None
            
            # Read container.xml to find OPF location
            try:
                container = epub.read('META-INF/container.xml').decode('utf-8')
                root = ET.fromstring(container)
                ns = {'container': 'urn:oasis:names:tc:opendocument:xmlns:container'}
                rootfile = root.find('.//container:rootfile', ns)
                if rootfile is not None:
                    opf_path = rootfile.get('full-path')
            except:
                # Fallback: search for .opf file
                for name in epub.namelist():
                    if name.endswith('.opf'):
                        opf_path = name
                        break
            
            if not opf_path:
                report['issues'].append("Could not find metadata file (OPF) in EPUB. Your file may be corrupted.")
                return render_template('tools/metadata_checker.html', report=report)
            
            # Parse OPF metadata
            opf_content = epub.read(opf_path).decode('utf-8')
            opf_root = ET.fromstring(opf_content)
            
            # Define namespaces
            ns = {
                'opf': 'http://www.idpf.org/2007/opf',
                'dc': 'http://purl.org/dc/elements/1.1/'
            }
            
            # Extract metadata
            metadata_elem = opf_root.find('.//opf:metadata', ns)
            if metadata_elem is None:
                metadata_elem = opf_root.find('.//metadata')
            
            # Extract all metadata fields
            title = metadata_elem.findtext('.//dc:title', '', ns) if metadata_elem else ''
            creator = metadata_elem.findtext('.//dc:creator', '', ns) if metadata_elem else ''
            description = metadata_elem.findtext('.//dc:description', '', ns) if metadata_elem else ''
            publisher = metadata_elem.findtext('.//dc:publisher', '', ns) if metadata_elem else ''
            language = metadata_elem.findtext('.//dc:language', '', ns) if metadata_elem else ''
            isbn = metadata_elem.findtext('.//dc:identifier', '', ns) if metadata_elem else ''
            
            # Extract subjects/keywords
            subjects = []
            if metadata_elem:
                for subj in metadata_elem.findall('.//dc:subject', ns):
                    if subj.text:
                        subjects.append(subj.text)
            
            report['metadata'] = {
                'title': title,
                'author': creator,
                'description': description,
                'publisher': publisher,
                'language': language,
                'isbn': isbn,
                'keywords': ', '.join(subjects) if subjects else ''
            }
            
            # Analyze metadata quality
            report = analyze_metadata_quality(report, title, creator, description, subjects, language, isbn)
            
    except zipfile.BadZipFile:
        report['issues'].append("The uploaded file is not a valid EPUB file. Please make sure you're uploading a proper EPUB.")
    except Exception as e:
        report['issues'].append(f"Error reading EPUB file: {str(e)}")
    
    return render_template('tools/metadata_checker.html', report=report)


def analyze_metadata_quality(report, title, author, description, keywords, language, isbn):
    """Perform comprehensive metadata analysis."""
    
    # Initialize scores
    score_total = 0
    score_max = 0
    
    # TITLE ANALYSIS
    score_max += 20
    if not title:
        report['issues'].append("Missing Title: Your book must have a title. This is required by all platforms.")
    else:
        title_len = len(title)
        report['metadata']['title_length'] = title_len
        
        if title_len < 10:
            report['warnings'].append(f"Short Title: Your title is only {title_len} characters. Consider making it more descriptive (optimal: 30-80 characters).")
            score_total += 5
        elif title_len > 200:
            report['warnings'].append(f"Very Long Title: Your title is {title_len} characters. Amazon KDP limits titles to 200 characters. Consider shortening it.")
            score_total += 10
        elif 30 <= title_len <= 80:
            report['successes'].append(f"Great Title Length: Your title is {title_len} characters, which is perfect for visibility and readability.")
            score_total += 20
        else:
            report['successes'].append(f"Good Title Length: Your title is {title_len} characters.")
            score_total += 15
    
    # AUTHOR ANALYSIS
    score_max += 15
    if not author:
        report['issues'].append("Missing Author: Your book must have an author name. This is required by all platforms.")
    else:
        report['successes'].append(f"Author Name Present: {author}")
        score_total += 15
    
    # DESCRIPTION ANALYSIS
    score_max += 30
    if not description:
        report['issues'].append("Missing Description: A book description is essential for selling your book. Readers need to know what your book is about.")
        report['recommendations'].append("Add a compelling description that hooks readers in the first sentence and clearly explains what your book offers.")
    else:
        desc_len = len(description)
        report['metadata']['description_length'] = desc_len
        
        if desc_len < 150:
            report['warnings'].append(f"Short Description: Your description is only {desc_len} characters. Aim for at least 300 characters to effectively describe your book and improve SEO.")
            report['recommendations'].append("Expand your description to include: what the book is about, who it's for, and what makes it unique.")
            score_total += 10
        elif desc_len < 300:
            report['warnings'].append(f"Description Could Be Longer: Your description is {desc_len} characters. Consider expanding it to 300-500 characters for better engagement.")
            score_total += 20
        elif desc_len > 4000:
            report['warnings'].append(f"Very Long Description: Your description is {desc_len} characters. Amazon KDP limits descriptions to 4,000 characters.")
            score_total += 25
        else:
            report['successes'].append(f"Excellent Description Length: Your description is {desc_len} characters, which is ideal for engaging readers.")
            score_total += 30
        
        # Check for HTML or special formatting
        if '<' in description or '>' in description:
            report['recommendations'].append("Your description contains HTML tags. Make sure to use proper HTML formatting when uploading to Amazon (use <b>, <i>, <br>, <ul>, <li> tags).")
    
    # KEYWORDS ANALYSIS
    score_max += 15
    if not keywords:
        report['warnings'].append("No Keywords Found: Keywords help readers discover your book. Add relevant keywords to your metadata.")
        report['recommendations'].append("Include 5-7 relevant keywords that describe your book's genre, themes, and content. Think about what readers might search for.")
    else:
        keyword_count = len(keywords)
        report['metadata']['keyword_count'] = keyword_count
        
        if keyword_count < 3:
            report['warnings'].append(f"Few Keywords: You only have {keyword_count} keywords. Amazon allows up to 7 keyword phrases - use them all!")
            report['recommendations'].append("Add more specific keywords related to your genre, themes, and content.")
            score_total += 5
        elif keyword_count > 7:
            report['warnings'].append(f"Too Many Keywords: You have {keyword_count} keywords. Amazon KDP allows 7 keyword boxes. Focus on the most important ones.")
            score_total += 10
        else:
            report['successes'].append(f"Good Keyword Count: You have {keyword_count} keywords, which is excellent for discoverability.")
            score_total += 15
    
    # LANGUAGE ANALYSIS
    score_max += 10
    if not language:
        report['warnings'].append("Missing Language: Specify your book's language for proper categorization on publishing platforms.")
    else:
        report['successes'].append(f"Language Specified: {language}")
        score_total += 10
    
    # ISBN ANALYSIS
    score_max += 10
    if isbn:
        # Basic ISBN validation
        isbn_clean = isbn.replace('-', '').replace(' ', '')
        if len(isbn_clean) in [10, 13]:
            report['successes'].append(f"ISBN Present: {isbn}")
            score_total += 10
        else:
            report['warnings'].append(f"ISBN Format Issue: Your ISBN ({isbn}) doesn't appear to be valid (should be 10 or 13 digits).")
            score_total += 5
    else:
        report['recommendations'].append("ISBN: If you're publishing on Amazon KDP, you can use their free ISBN. For wider distribution, consider purchasing your own ISBN.")
    
    # Calculate overall score
    score_percentage = int((score_total / score_max) * 100) if score_max > 0 else 0
    report['scores'] = {
        'total': score_total,
        'max': score_max,
        'percentage': score_percentage,
        'grade': get_grade(score_percentage)
    }
    
    # Platform-specific recommendations
    add_platform_recommendations(report)
    
    return report


def generate_metadata_report(title, description, author, keywords, categories):
    """Generate metadata report from form input."""
    report = {
        'file_uploaded': False,
        'issues': [],
        'warnings': [],
        'successes': [],
        'recommendations': [],
        'metadata': {
            'title': title,
            'author': author,
            'description': description,
            'keywords': keywords,
            'categories': categories
        },
        'scores': {}
    }
    
    # Convert keywords and categories to lists
    keyword_list = [k.strip() for k in keywords.split(',') if k.strip()] if keywords else []
    
    # Analyze
    report = analyze_metadata_quality(report, title, author, description, keyword_list, '', '')
    
    return report


def get_grade(percentage):
    """Convert percentage to letter grade."""
    if percentage >= 90:
        return 'A'
    elif percentage >= 80:
        return 'B'
    elif percentage >= 70:
        return 'C'
    elif percentage >= 60:
        return 'D'
    else:
        return 'F'


def add_platform_recommendations(report):
    """Add platform-specific recommendations."""
    report['platform_tips'] = {
        'amazon_kdp': [
            "Use all 7 keyword boxes - they're free marketing!",
            "Select up to 10 categories (2 during upload, request more via KDP support)",
            "Keep your title under 200 characters including subtitle",
            "Use HTML formatting in your description (<b>, <i>, <ul>, <li>)",
            "Update your metadata regularly based on what works"
        ],
        'apple_books': [
            "Apple Books has a 2,700 character limit for descriptions",
            "Use clear, descriptive category selections",
            "Ensure your EPUB validates with no errors",
            "Include an appealing cover that works in grayscale"
        ],
        'kobo': [
            "Kobo allows up to 4,000 characters for descriptions",
            "Use relevant tags and categories",
            "Consider Kobo's Plus subscription program",
            "Localize metadata for international markets"
        ],
        'general': [
            "Keep your metadata consistent across all platforms",
            "Update keywords based on search trends and performance",
            "Use A/B testing for descriptions when possible",
            "Monitor your conversion rate (views to sales)",
            "Include series information if applicable"
        ]
    }
    
    return report


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


@bp.route('/cover-designer', methods=['GET', 'POST'])
def cover_designer():
    """Cover size calculator tool for Amazon KDP."""
    if request.method == 'GET':
        return render_template('tools/cover_designer.html')
    
    data = request.get_json() if request.is_json else request.form
    
    book_type = data.get('book_type', 'ebook')
    
    results = {}
    
    if book_type == 'ebook':
        # Ebook cover specifications
        results = {
            'book_type': 'Ebook (Kindle)',
            'recommended_size': '2560 x 1600 pixels',
            'minimum_size': '1000 x 625 pixels',
            'aspect_ratio': '1.6:1 (width:height)',
            'resolution': '300 DPI recommended (72 DPI minimum)',
            'max_file_size': '50 MB',
            'format': 'JPEG or TIFF (JPEG preferred)',
            'color_mode': 'RGB',
            'notes': [
                'Cover must be readable at thumbnail size (50x80 pixels)',
                'Use high contrast colors',
                'Keep text large and bold',
                'Avoid fine details that disappear when scaled down'
            ]
        }
    else:
        # Paperback cover calculations
        trim_size = data.get('trim_size', '6x9')
        page_count = int(data.get('page_count', 100))
        paper_type = data.get('paper_type', 'white')
        interior_type = data.get('interior_type', 'black')
        
        # Trim dimensions
        trim_sizes = {
            '5x8': (5.0, 8.0),
            '5.5x8.5': (5.5, 8.5),
            '6x9': (6.0, 9.0),
            '7x10': (7.0, 10.0),
            '8x10': (8.0, 10.0),
            '8.5x11': (8.5, 11.0)
        }
        
        trim_width, trim_height = trim_sizes.get(trim_size, (6.0, 9.0))
        
        # Calculate spine width based on page count and paper type
        # Formula from Amazon KDP
        if interior_type == 'black':
            if paper_type == 'white':
                pages_per_inch = 442
            else:  # cream
                pages_per_inch = 392
        else:  # color
            pages_per_inch = 444
        
        spine_width = page_count / pages_per_inch
        
        # Total cover dimensions (with bleed)
        bleed = 0.125
        total_width = (trim_width * 2) + spine_width + (bleed * 2)
        total_height = trim_height + (bleed * 2)
        
        # Convert to pixels at 300 DPI
        width_pixels = int(total_width * 300)
        height_pixels = int(total_height * 300)
        
        # Safe zones
        safe_zone = 0.125
        spine_safe_zone = 0.0625
        
        results = {
            'book_type': 'Paperback',
            'trim_size': f'{trim_width}" x {trim_height}"',
            'page_count': page_count,
            'paper_type': paper_type.title(),
            'interior_type': interior_type.title(),
            'spine_width': f'{spine_width:.3f}"',
            'total_dimensions': f'{total_width:.3f}" x {total_height:.3f}"',
            'dimensions_pixels': f'{width_pixels} x {height_pixels} pixels',
            'resolution': '300 DPI (required)',
            'format': 'PDF (recommended)',
            'color_mode': 'RGB',
            'bleed': f'{bleed}" on all sides',
            'safe_zone': f'{safe_zone}" from trim line',
            'spine_safe_zone': f'{spine_safe_zone}" from spine edges',
            'barcode_space': '2" x 1.2" (bottom right, back cover)',
            'notes': [
                'Keep all text and important elements within safe zone',
                'Spine text must stay within spine safe zone',
                'Background/images should extend to bleed edges',
                'Reserve space for ISBN barcode on back cover',
                'Use 300 DPI for professional print quality',
                'Export as single PDF file (not separate front/back)',
                'Test print a proof copy before publishing'
            ],
            'cover_layout': {
                'back_cover_width': f'{trim_width + bleed:.3f}"',
                'spine_width': f'{spine_width:.3f}"',
                'front_cover_width': f'{trim_width + bleed:.3f}"',
                'total_width': f'{total_width:.3f}"',
                'height': f'{total_height:.3f}"'
            }
        }
    
    if request.is_json:
        return jsonify(results), 200
    
    return render_template('tools/cover_designer.html', results=results)
