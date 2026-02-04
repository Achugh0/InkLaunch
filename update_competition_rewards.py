"""
Update the February 2026 competition with non-monetary rewards
and add badge/achievement system
"""

from datetime import datetime
from app import create_app
from app.models import Competition, User
from bson import ObjectId

app = create_app()

with app.app_context():
    competition_id = '6982bf76dc8a51a38f6c1951'
    
    # New prize structure with non-monetary rewards
    new_prizes = {
        'first_place': '🏆 Featured on InkLaunch Homepage for 3 months + Professional Editing Service (up to 50,000 words) + Award Winner Badge + Featured Author Interview + Book Launch Promotion Package',
        'second_place': '🥈 Featured on InkLaunch Homepage for 1 month + Custom Cover Design + Runner-Up Badge + Author Spotlight Article + 6 Months Premium Membership',
        'third_place': '🥉 Featured in Newsletter + Professional Manuscript Critique + Finalist Badge + Social Media Promotion + 3 Months Premium Membership'
    }
    
    # Update description with new rewards
    new_description = '''Welcome to the February Fiction Excellence Award! 

This competition seeks to discover and celebrate exceptional fiction writing across all sub-genres. Whether you write romance, mystery, science fiction, fantasy, or literary fiction, we want to read your best work.

**What We're Looking For:**
- Original, compelling storytelling
- Well-developed characters that leap off the page
- Polished writing that demonstrates craft and skill
- Creative and unique voices

**Prizes & Recognition:**

🏆 **First Place Winner:**
- Featured placement on InkLaunch homepage for **3 months**
- Professional editing service (up to 50,000 words)
- Exclusive "Gold Winner" badge on your author profile
- Featured author interview published on our blog
- Comprehensive book launch promotion package
- Detailed AI evaluation report with improvement suggestions

🥈 **Second Place:**
- Featured on InkLaunch homepage for **1 month**
- Professional custom cover design ($200 value)
- "Silver Winner" badge on your author profile
- Author spotlight article in our monthly newsletter
- 6 months of Premium Membership (all features unlocked)
- Social media promotion across our channels

🥉 **Third Place:**
- Featured in our newsletter reaching 10,000+ authors
- In-depth professional manuscript critique session
- "Bronze Winner" badge on your author profile
- Social media shoutouts and promotions
- 3 months of Premium Membership
- Priority placement in book listings

**All Finalists Receive:**
- "Competition Finalist" badge
- Comprehensive AI evaluation report
- InkLaunch Book Club consideration
- Beta reader network access
- Inclusion in "Best of 2026" anthology (if selected)

**Submission Guidelines:**
- Fiction manuscripts only (all sub-genres welcome)
- Minimum 20,000 words, maximum 120,000 words
- Original work that you own the rights to
- One submission per author
- **FREE to enter** - No submission fees!

**Evaluation Criteria:**
All submissions will be evaluated by our advanced AI system across four key criteria:
- **Plot/Story Structure (25%)** - Pacing, narrative arc, conflict resolution
- **Character Development (25%)** - Depth, growth, believability, dialogue
- **Writing Quality/Style (25%)** - Prose, grammar, voice, technique
- **Originality/Creativity (25%)** - Fresh ideas, unique perspective, innovation

The top manuscripts will advance to our editorial board for final judging. Winners will be announced on **February 28, 2026**.

This is more than just a competition—it's your chance to gain visibility, improve your craft, and connect with thousands of readers!

Good luck and happy writing! 📚✨'''
    
    # Update the competition
    Competition.update(competition_id, {
        'prize_structure': new_prizes,
        'description': new_description,
        'entry_fee_amount': 0
    })
    
    print("✅ Competition updated with non-monetary rewards!")
    print("\nNew Prize Structure:")
    print(f"🥇 First Place: {new_prizes['first_place'][:80]}...")
    print(f"🥈 Second Place: {new_prizes['second_place'][:80]}...")
    print(f"🥉 Third Place: {new_prizes['third_place'][:80]}...")
    print("\n✅ Entry fee confirmed as FREE")
    print("✅ Description updated with detailed reward information")
