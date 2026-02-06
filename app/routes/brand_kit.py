from flask import Blueprint, render_template, request
from app.services.brand_kit_service import get_brand_kit, create_brand_kit

brand_kit_bp = Blueprint('brand_kit', __name__, url_prefix='/tools')

@brand_kit_bp.route('/brand-kit', methods=['GET', 'POST'])
def brand_kit():
    brand_kit = None
    if request.method == 'POST':
        author_name = request.form.get('author_name', '')
        tagline = request.form.get('tagline', '')
        # Placeholder: create a new brand kit
        brand_kit = create_brand_kit(author_name, tagline)
    return render_template('tools/brand_kit.html', brand_kit=brand_kit)
