"""
Publish the February 2026 competition and fix it to show on the competitions page
"""

from datetime import datetime
from app import create_app
from app.models import Competition

app = create_app()

with app.app_context():
    competition_id = '6982bf76dc8a51a38f6c1951'
    
    # Update status to accepting_submissions
    Competition.update_status(competition_id, 'accepting_submissions')
    
    print(f"✅ Competition published successfully!")
    print(f"   Status changed from 'draft' to 'accepting_submissions'")
    print(f"   Competition is now visible on the public competitions page")
    print(f"   Authors can submit starting Feb 10, 2026")
