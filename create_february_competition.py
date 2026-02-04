"""
Script to create a February 2026 Fiction Writing Competition
Starts: Feb 10, 2026
Ends: Feb 15, 2026
Winner Announcement: Feb 28, 2026
"""

from datetime import datetime
import sys

def create_competition():
    # Import inside function to ensure Flask app is initialized
    from app import create_app
    from app.models import Competition, User
    
    app = create_app()
    
    with app.app_context():
        try:
            # First, find an admin user to create the competition
            admin_user = User.find_by_email('admin@inklaunch.com')
            if not admin_user:
                # Try to find any admin user
                from app import mongo
                admin_user = mongo.db['users'].find_one({'role': 'admin'})
            
            if not admin_user:
                print("❌ Error: No admin user found. Please create an admin user first.")
                sys.exit(1)
            
            admin_id = str(admin_user['_id'])
            
            # Competition details
            title = 'February 2026 Fiction Excellence Award'
            description = '''Welcome to the February Fiction Excellence Award! 

This competition seeks to discover and celebrate exceptional fiction writing across all sub-genres. Whether you write romance, mystery, science fiction, fantasy, or literary fiction, we want to read your best work.

**What We're Looking For:**
- Original, compelling storytelling
- Well-developed characters that leap off the page
- Polished writing that demonstrates craft and skill
- Creative and unique voices

**Prizes:**
🥇 First Place: ₹25,000 + Featured placement on InkLaunch homepage for 1 month
🥈 Second Place: ₹15,000 + Featured in our monthly newsletter
🥉 Third Place: ₹10,000 + Author spotlight interview

**Submission Guidelines:**
- Fiction manuscripts only (all sub-genres welcome)
- Minimum 20,000 words, maximum 120,000 words
- Original work that you own the rights to
- One submission per author
- Free to enter

**Evaluation:**
All submissions will be evaluated by our advanced AI system across four key criteria:
- Plot/Story Structure (25%)
- Character Development (25%)
- Writing Quality/Style (25%)
- Originality/Creativity (25%)

The top manuscripts will advance to our editorial board for final judging. Winners will be announced on February 28, 2026.

Good luck and happy writing!'''
            
            genre_categories = ['Fiction', 'Romance', 'Mystery', 'Science Fiction', 'Fantasy', 'Literary Fiction']
            submission_start_date = datetime(2026, 2, 10, 0, 0, 0)
            submission_end_date = datetime(2026, 2, 15, 23, 59, 59)
            winner_announcement_date = datetime(2026, 2, 28, 12, 0, 0)
            max_submissions_per_author = 1
            entry_fee_amount = 0
            
            evaluation_criteria = {
                'plot_story_structure': 25,
                'character_development': 25,
                'writing_quality_style': 25,
                'originality_creativity': 25
            }
            
            prize_structure = {
                'first_place': '₹25,000 cash prize + Featured placement on InkLaunch homepage for 1 month + Winner certificate',
                'second_place': '₹15,000 cash prize + Featured in monthly newsletter + Winner certificate',
                'third_place': '₹10,000 cash prize + Author spotlight interview + Winner certificate'
            }
            
            # Create competition
            competition_id = Competition.create(
                title=title,
                description=description,
                genre_categories=genre_categories,
                submission_start_date=submission_start_date,
                submission_end_date=submission_end_date,
                evaluation_criteria=evaluation_criteria,
                max_submissions_per_author=max_submissions_per_author,
                entry_fee_amount=entry_fee_amount,
                prize_structure=prize_structure,
                created_by_admin_id=admin_id,
                winner_announcement_date=winner_announcement_date
            )
            
            print(f"✅ Competition created successfully!")
            print(f"   ID: {competition_id}")
            print(f"   Title: {title}")
            print(f"   Submission Period: Feb 10, 2026 - Feb 15, 2026")
            print(f"   Winner Announcement: Feb 28, 2026")
            print(f"   Status: draft (ready to be published)")
            print(f"   Entry Fee: Free")
            print(f"\nTo publish this competition:")
            print(f"   1. Log in as admin at http://localhost:5000/admin/login")
            print(f"   2. Go to Admin Dashboard > Competitions")
            print(f"   3. Click 'View' on the competition")
            print(f"   4. Click 'Publish Competition' button")
            print(f"\nOnce published, authors can start submitting on Feb 10, 2026!")
            
            return competition_id
            
        except Exception as e:
            print(f"❌ Error creating competition: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    print("Creating February 2026 Fiction Writing Competition...")
    print("-" * 60)
    create_competition()
