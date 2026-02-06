# Service for EPUB validation (EpubCheck integration)

def validate_epub(epub_path):
    # TODO: Integrate with EpubCheck (Java subprocess or API)
    # Return mock report for now
    return {
        'passed': True,
        'errors': [],
        'warnings': ['Missing accessibility metadata'],
        'metadata': {'title': 'Sample Book', 'author': 'Author Name'},
        'navigation': 'Valid',
        'file_size': 1.2,
        'report_download_url': '/static/reports/sample_report.txt'
    }
