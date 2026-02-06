from flask import Blueprint, render_template, request, flash, send_file
from app.services.epub_validator_service import validate_epub
import os

epub_validator_bp = Blueprint('epub_validator', __name__, url_prefix='/tools')

@epub_validator_bp.route('/epub-validator', methods=['GET', 'POST'])
def epub_validator():
    report = None
    if request.method == 'POST':
        file = request.files.get('epub_file')
        if file and file.filename.endswith('.epub') and file.content_length <= 50 * 1024 * 1024:
            # Save file temporarily
            temp_path = f'/tmp/{file.filename}'
            file.save(temp_path)
            report = validate_epub(temp_path)
            os.remove(temp_path)
        else:
            flash('Invalid file. Please upload a valid EPUB file under 50MB.', 'danger')
    return render_template('tools/epub_validator.html', report=report)
