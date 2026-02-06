from flask import Blueprint, render_template, request, flash
from app.services.metadata_service import get_metadata, update_metadata

metadata_editor_bp = Blueprint('metadata_editor', __name__, url_prefix='/tools')

@metadata_editor_bp.route('/metadata-editor', methods=['GET', 'POST'])
def metadata_editor():
    metadata = get_metadata()
    if request.method == 'POST':
        new_metadata = {
            'isbn': request.form.get('isbn', ''),
            'author': request.form.get('author', ''),
            'title': request.form.get('title', ''),
            'description': request.form.get('description', ''),
        }
        update_metadata(new_metadata)
        flash('Metadata updated!', 'success')
        metadata = new_metadata
    return render_template('tools/metadata_editor.html', metadata=metadata)
