from flask import Blueprint, render_template
from app.services.analytics_service import get_reader_engagement

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics_bp.route('/reader')
def reader_dashboard():
    # Placeholder: Fetch analytics data
    engagement_data = get_reader_engagement()
    return render_template('analytics/reader_dashboard.html', engagement_data=engagement_data)
