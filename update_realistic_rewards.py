"""
Update the February 2026 competition with realistic rewards
(removing services that cannot be offered at this time)
"""

from datetime import datetime
from app import create_app
from app.models import Competition

app = create_app()

with app.app_context():
    competition_id = '6982bf76dc8a51a38f6c1951'
    
    # Simplified prize structure with realistic rewards
    new_prizes = {
        'first_place': '🏆 Featured on InkLaunch Homepage for 3 months + Gold Winner Badge + Featured Author Interview + Detailed AI Evaluation Report',
        'second_place': '🥈 Featured on InkLaunch Homepage for 1 month + Silver Winner Badge + Author Spotlight Article + Instagram Promotion',
        'third_place': '🥉 Featured in Newsletter + Bronze Winner Badge + Social Media Promotions + Priority Book Listings'
    }
    
    # Updated description with realistic rewards
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
- Exclusive "Gold Winner" badge on your author profile
- Featured author interview published on our blog
- Detailed AI evaluation report with improvement suggestions

🥈 **Second Place:**
- Featured on InkLaunch homepage for **1 month**
- "Silver Winner" badge on your author profile
- Author spotlight article in our monthly newsletter
- Instagram promotion across our channels

🥉 **Third Place:**
- Featured in our newsletter reaching 10,000+ authors
- "Bronze Winner" badge on your author profile
- Social media shoutouts and promotions
- Priority placement in book listings

**All Finalists Receive:**
- "Competition Finalist" badge
- Comprehensive AI evaluation report
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

This is your chance to gain visibility, improve your craft, and connect with thousands of readers!

Good luck and happy writing! 📚✨'''
    
    # Update the competition
    Competition.update(competition_id, {
        'prize_structure': new_prizes,
        'description': new_description
    })
    
    print("✅ Competition updated with realistic rewards!")
    print("\nRevised Prize Structure:")
    print(f"🥇 First Place: {new_prizes['first_place']}")
    print(f"🥈 Second Place: {new_prizes['second_place']}")
    print(f"🥉 Third Place: {new_prizes['third_place']}")
    print("\n✅ Removed services that cannot be offered at this time:")
    print("   - Professional editing service")
    print("   - Custom cover design")
    print("   - Premium memberships")
    print("   - Book launch promotion packages")
    print("   - Manuscript critique sessions")
    print("   - Book club consideration")
    print("   - Beta reader network access")
