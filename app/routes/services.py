"""Paid services routes."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models import User
from app import mongo
from bson import ObjectId
from datetime import datetime
from flask_login import login_required, current_user

bp = Blueprint('services', __name__, url_prefix='/services')

# Service catalog with pricing
SERVICES_CATALOG = {
    'cover_design': {
        'name': 'Professional Cover Design',
        'description': 'Eye-catching book covers that sell',
        'icon': '🎨',
        'price': 75,
        'features': [
            '3 unique design concepts',
            'Unlimited revisions',
            'Print & digital formats',
            'Social media graphics included',
            '7-day delivery'
        ],
        'delivery_days': 7
    },
    'editing': {
        'name': 'Professional Book Editing',
        'description': 'Comprehensive editing to polish your manuscript',
        'icon': '✏️',
        'price': 75,
        'price_tiers': [
            {'range': 'Up to 200 pages', 'price': 75},
            {'range': '201-400 pages', 'price': 150},
            {'range': '401-600 pages', 'price': 225},
            {'range': '601-800 pages', 'price': 300},
            {'range': '801+ pages', 'price': 375}
        ],
        'features': [
            'Line editing & copyediting',
            'Grammar & punctuation',
            'Style consistency',
            'Detailed feedback report',
            '14-day delivery per 200 pages'
        ],
        'delivery_days': 14
    },
    'proofreading': {
        'name': 'Proofreading Service',
        'description': 'Final polish before publication',
        'icon': '🔍',
        'price': 50,
        'features': [
            'Spelling & grammar check',
            'Punctuation corrections',
            'Formatting consistency',
            'Quick 5-day turnaround',
            'Track changes document'
        ],
        'delivery_days': 5
    },
    'ghostwriting': {
        'name': 'Ghost Writing Services',
        'description': 'Professional writers bring your ideas to life',
        'icon': '👻',
        'price': 750,
        'features': [
            'Complete manuscript from outline',
            'Up to 80,000 words',
            'Your voice & style',
            '2 rounds of revisions',
            '60-day delivery'
        ],
        'delivery_days': 60
    },
    'formatting': {
        'name': 'Book Formatting',
        'description': 'Professional interior layout for print & digital',
        'icon': '📐',
        'price': 37,
        'features': [
            'Print-ready PDF',
            'eBook formats (ePub, MOBI)',
            'Chapter headings & page numbers',
            'Professional typography',
            '3-day delivery'
        ],
        'delivery_days': 3
    },
    'marketing': {
        'name': 'Book Marketing Package',
        'description': 'Get your book in front of readers',
        'icon': '📢',
        'price': 200,
        'features': [
            'Social media campaign (30 days)',
            'Press release writing & distribution',
            'Book trailer video',
            'Amazon optimization',
            'Email marketing template'
        ],
        'delivery_days': 30
    },
    'isbn': {
        'name': 'ISBN & Registration',
        'description': 'Complete publishing setup assistance - FREE!',
        'icon': '📚',
        'price': 0,
        'features': [
            'ISBN acquisition guidance',
            'Copyright registration guidance',
            'Distribution setup help',
            'Metadata optimization',
            '2-day delivery',
            'Completely FREE service'
        ],
        'delivery_days': 2
    },
    'beta_readers': {
        'name': 'Beta Reader Panel',
        'description': 'Get feedback from real readers',
        'icon': '👥',
        'price': 62,
        'features': [
            '10 dedicated beta readers',
            'Detailed feedback forms',
            'Reading preferences matched',
            'Compiled feedback report',
            '14-day reading period'
        ],
        'delivery_days': 14
    },
    'query_letter': {
        'name': 'Query Letter Writing',
        'description': 'Compelling pitch to agents & publishers',
        'icon': '✉️',
        'price': 37,
        'features': [
            'Professional query letter',
            'Synopsis writing',
            'Agent research (top 10)',
            '2 revisions included',
            '5-day delivery'
        ],
        'delivery_days': 5
    },
    'manuscript_critique': {
        'name': 'Manuscript Critique',
        'description': 'In-depth analysis of your work',
        'icon': '📝',
        'price': 100,
        'features': [
            'Detailed 10-page report',
            'Plot & character analysis',
            'Pacing & structure feedback',
            'Marketability assessment',
            '10-day delivery'
        ],
        'delivery_days': 10
    },
    'blurb_writing': {
        'name': 'Book Blurb Writing',
        'description': 'Compelling back cover copy',
        'icon': '💬',
        'price': 25,
        'features': [
            'Compelling book description',
            'Hook that captures attention',
            'SEO-optimized for retailers',
            '3 variations to choose from',
            '3-day delivery'
        ],
        'delivery_days': 3
    },
    'author_website': {
        'name': 'Author Website',
        'description': 'Professional author platform',
        'icon': '🌐',
        'price': 150,
        'features': [
            'Custom website design',
            'Blog setup',
            'Mailing list integration',
            'Book showcase',
            'Mobile responsive'
        ],
        'delivery_days': 14
    }
}


@bp.route('/')
def list_services():
    """List all available paid services."""
    return render_template('services/list.html', services=SERVICES_CATALOG)


@bp.route('/<service_id>')
def service_detail(service_id):
    """Show details of a specific service."""
    service = SERVICES_CATALOG.get(service_id)
    if not service:
        flash('Service not found.', 'error')
        return redirect(url_for('services.list_services'))
    
    service_data = {**service, 'id': service_id}
    return render_template('services/detail.html', service=service_data)


@bp.route('/<service_id>/request', methods=['GET', 'POST'])
@login_required
def request_service(service_id):
    """Request a paid service."""
    service = SERVICES_CATALOG.get(service_id)
    if not service:
        flash('Service not found.', 'error')
        return redirect(url_for('services.list_services'))
    
    if request.method == 'POST':
        try:
            service_request = {
                'user_id': ObjectId(session['user_id']),
                'service_id': service_id,
                'service_name': service['name'],
                'price': service['price'],
                'details': request.form.get('details', ''),
                'contact_email': request.form.get('contact_email'),
                'contact_phone': request.form.get('contact_phone', ''),
                'urgency': request.form.get('urgency', 'standard'),
                'status': 'pending',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            result = mongo.db.service_requests.insert_one(service_request)
            
            flash(f'Service request submitted successfully! We\'ll contact you within 24 hours. Request ID: {result.inserted_id}', 'success')
            return redirect(url_for('users.profile'))
            
        except Exception as e:
            flash(f'Error submitting request: {str(e)}', 'error')
    
    service_data = {**service, 'id': service_id}
    return render_template('services/request.html', service=service_data)


@bp.route('/my-requests')
@login_required
def my_requests():
    """View user's service requests."""
    try:
        requests_list = list(mongo.db.service_requests.find({
            'user_id': ObjectId(session['user_id'])
        }).sort('created_at', -1))
        
        return render_template('services/my_requests.html', requests=requests_list)
    except Exception as e:
        flash(f'Error loading requests: {str(e)}', 'error')
        return redirect(url_for('main.dashboard'))
