from flask import Blueprint, render_template
from app.services.pulse_analysis_service import get_pulse_metrics

pulse_bp = Blueprint('pulse', __name__, url_prefix='/analytics')

@pulse_bp.route('/pulse')
def pulse_dashboard():
    # Placeholder: Fetch pulse analysis metrics
    metrics = get_pulse_metrics()
    return render_template('analytics/pulse_dashboard.html', metrics=metrics)
