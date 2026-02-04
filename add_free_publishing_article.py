"""Add free publishing guidelines article."""
from app import create_app, mongo
from app.models import User, Article

app = create_app()

article_data = {
    'title': 'How to Publish Your Book for FREE: No Vanity Press, No Hidden Fees',
    'category': 'Publishing Tips',
    'excerpt': 'Learn how to publish your book completely free using Amazon KDP, PublishDrive, and Draft2Digital. Skip the expensive vanity presses and keep 100% of your rights.',
    'content': '''# How to Publish Your Book for FREE: No Vanity Press, No Hidden Fees

**Stop paying thousands of dollars to vanity presses!** You can publish your book professionally and reach millions of readers without spending a single penny. Here's exactly how to do it.

## The Truth About Vanity Presses

Many companies market themselves as "self-publishing services" and charge authors $500, $1,000, or even $5,000+ for packages that include:
- ISBN assignment
- Cover design
- Formatting
- Distribution
- Marketing

**The reality?** You can do all of this yourself for free (or very cheap), and you'll keep 100% of your rights and significantly higher royalties.

## Free Publishing Platforms: Your Best Options

### 1. Amazon KDP (Kindle Direct Publishing)

**Cost:** $0 (100% FREE)  
**Website:** kdp.amazon.com

**What You Get:**
- Publish ebooks and paperbacks
- FREE ISBN (or use your own)
- Access to Amazon's massive marketplace
- Up to 70% royalty on ebooks ($2.99-$9.99)
- 60% royalty on paperbacks (minus printing costs)
- Print-on-demand (no inventory needed)
- Global distribution to Amazon stores worldwide

**Pros:**
- Largest book marketplace in the world
- Easy to use platform
- Fast approval (24-72 hours)
- Kindle Unlimited program (earn from page reads)
- Free promotional tools
- Real-time sales reporting

**Cons:**
- Amazon-only distribution (if you choose KDP Select)
- You compete with millions of books
- Limited formatting options for ebooks

**How to Get Started:**
1. Create free account at kdp.amazon.com
2. Format your manuscript (DOC, DOCX, or PDF)
3. Design or upload your cover (or use Amazon's free cover creator)
4. Upload your files and fill in metadata
5. Set your price
6. Publish! (Goes live within 72 hours)

**Pro Tips:**
- Use all 7 keyword boxes
- Select up to 10 categories (2 during upload, request more via support)
- Price strategically: $2.99-$4.99 is sweet spot for most genres
- Use Amazon's preview tool to check formatting
- Join KDP Select for first 90 days to test Kindle Unlimited

---

### 2. PublishDrive

**Cost:** $0 for basic plan (commission-based)  
**Website:** publishdrive.com

**What You Get:**
- Distribute to 400+ online stores and libraries
- One upload, multiple platforms
- Apple Books, Google Play, Kobo, and more
- Real-time analytics across all stores
- Automated royalty collection
- Marketing tools included
- Free ISBN options

**Pricing Models:**
- **Free Plan:** 10% commission on sales (no upfront cost)
- **Pro Plan:** $149/year (0% commission, unlimited books)

**Pros:**
- Widest distribution network
- Single dashboard for all platforms
- Great for international reach
- Excellent analytics
- Handles all technical requirements for each platform
- Free marketing opportunities

**Cons:**
- 10% commission on free plan
- Slight delay in publishing (platform approval times vary)
- Learning curve for dashboard

**How to Get Started:**
1. Sign up for free account
2. Upload your EPUB and cover
3. Select distribution channels
4. Fill in metadata once (applies to all stores)
5. Choose pricing and territories
6. Submit for review
7. Goes live on multiple platforms within 1-2 weeks

**Pro Tips:**
- Start with free plan to test the waters
- Select all available stores (more exposure = more sales)
- Use their metadata optimizer
- Take advantage of free promotional campaigns
- Upgrade to Pro plan once you're making consistent sales

---

### 3. Draft2Digital

**Cost:** $0 (commission-based)  
**Website:** draft2digital.com

**What You Get:**
- Distribute to major retailers (Apple Books, Kobo, Barnes & Noble, etc.)
- Automatic formatting from Word docs
- Free cover designer tool
- Free ISBN for each retailer
- Universal Book Links (smart links that detect reader's location)
- Author dashboard with consolidated reporting

**Commission:** 10% of net royalties (after retailer takes their cut)

**Pros:**
- Super easy to use (easiest of the three)
- Excellent formatting tool
- Free ISBNs
- No upfront costs
- Great customer support
- Clean, simple dashboard
- Universal Book Links are incredibly useful

**Cons:**
- 10% commission always applies
- Smaller distribution network than PublishDrive
- No exclusive deals available

**How to Get Started:**
1. Create free account
2. Upload Word document (they format it automatically)
3. Use their cover creator or upload your own
4. Select retailers
5. Set pricing (or let them optimize per market)
6. Publish to all selected platforms at once

**Pro Tips:**
- Use their formatting tool (saves hours of work)
- Test the free cover designer (surprisingly good)
- Enable all retailers for maximum reach
- Use Universal Book Links in all marketing
- Let them handle pricing optimization

---

## Comparison: Which Platform Should You Use?

### Use Amazon KDP If:
- You want the simplest, fastest path to publication
- Amazon is your primary market (US, UK, etc.)
- You want to test Kindle Unlimited
- You're writing in popular genres (romance, thriller, sci-fi)
- You want maximum royalties (70% on ebooks)

### Use PublishDrive If:
- You want global distribution
- Libraries are important to you
- You're willing to manage more complexity for wider reach
- International markets are significant for your book
- You plan to publish multiple books (Pro plan becomes worth it)

### Use Draft2Digital If:
- You want easy, hands-off distribution
- You don't want to deal with formatting
- You need ISBNs for multiple retailers
- Simplicity is more important than control
- You're new to self-publishing

### The Best Strategy: Use All Three!

Here's what savvy authors do:
1. **Amazon KDP:** Publish ebook and paperback directly
2. **PublishDrive or Draft2Digital:** Distribute ebook to all OTHER stores (Apple, Kobo, Google Play, etc.)
3. Keep your options open and maximize reach

**Important:** If you enroll in KDP Select (for Kindle Unlimited), your ebook must be exclusive to Amazon for 90 days. You can still publish paperback and distribute through other platforms for non-Amazon stores.

---

## What About ISBNs?

**Do you need one?** It depends.

**For ebooks:**
- Amazon assigns a free ASIN (Amazon Standard Identification Number)
- PublishDrive and Draft2Digital provide free ISBNs
- You don't need to buy your own unless you want your name as publisher

**For paperbacks:**
- Amazon provides free ISBN
- You can buy your own from Bowker ($125+ per ISBN, or $295 for 10)
- Only buy if you want your own publishing imprint

**Bottom Line:** Use free ISBNs unless you're building a publishing business.

---

## The Complete Free Publishing Workflow

### Step 1: Prepare Your Manuscript
- Write in Microsoft Word or Google Docs
- Use standard formatting (12pt, Times New Roman or similar)
- Include chapter breaks
- Run through Grammarly or similar editing tool
- Get beta readers to review (free!)

### Step 2: Format Your Book
**For Ebook:**
- Use Draft2Digital's free formatting tool, OR
- Use Vellum ($249.99, Mac only) for pro results, OR
- Use Atticus ($147 one-time, cross-platform)
- Free option: Reedsy Book Editor (reedsy.com/write-a-book)

**For Paperback:**
- Use Amazon's free templates
- Or Canva (free) with KDP templates
- Or Reedsy Book Editor

### Step 3: Create Your Cover
**Free Options:**
- Canva (free plan has tons of templates)
- Amazon Cover Creator (basic but functional)
- Draft2Digital Cover Creator
- PhotoPea (free Photoshop alternative)

**Paid Options (if you want professional quality):**
- Fiverr: $50-$150
- Reedsy marketplace: $200-$500+
- 99designs contests: $300+

**Important:** Don't skimp on your cover! It's your #1 marketing tool. If you can't design, invest the $50-$150 on Fiverr for a pro cover.

### Step 4: Write Your Book Description
- Hook them in first sentence
- Explain what the book is about (don't give away ending!)
- Create desire/curiosity
- Use HTML formatting (<b>, <i>, <ul>, <li>)
- End with call-to-action
- Study bestsellers in your genre

### Step 5: Research Keywords and Categories
- Use Publisher Rocket ($97 one-time, worth it)
- Or free: Amazon search suggestions
- Look at similar successful books
- Choose specific, not broad categories
- Use all 7 keyword slots

### Step 6: Publish!
- Upload to Amazon KDP first
- Test the file, check preview carefully
- Once approved, upload to PublishDrive or Draft2Digital
- Wait 1-2 weeks for wide distribution approval

### Step 7: Market (Also Free!)
- Build email list (Mailchimp free up to 500 subscribers)
- Share on social media
- Join Facebook groups in your genre
- Post on BookTok, Bookstagram
- Request reviews from readers
- Submit to BookBub (free submissions)
- Use Amazon Ads (start with $5/day)

---

## Costs Breakdown: Free vs Vanity Press

### Vanity Press Package ($2,000-$5,000):
- ISBN: $0 (but under their name)
- Cover design: Templated
- Formatting: Basic
- Distribution: Limited
- Marketing: Minimal
- **Rights:** They keep some rights
- **Royalties:** 20-40% (after their cut)

### DIY Free Publishing:
- Amazon KDP: $0
- PublishDrive/Draft2Digital: $0 upfront
- Free ISBNs: $0
- Cover (Canva): $0 (or $50-150 on Fiverr)
- Formatting tools: $0
- Distribution: Worldwide
- **Rights:** You keep 100%
- **Royalties:** 60-70% (direct to you)

**Savings:** $2,000-$5,000+  
**Control:** Complete  
**Rights:** All yours forever

---

## Red Flags: Avoid These "Publishing Services"

Watch out for companies that:
- Require upfront fees for "publishing"
- Keep rights to your work
- Take majority of royalties
- Lock you into long contracts
- Charge for "marketing packages"
- Promise bestseller status
- Require minimum purchases from you
- Don't let you set your own prices

**Legitimate services charge $0 upfront and take a small commission (10-15%) or let you keep everything.**

---

## Success Tips for Free Publishing

1. **Quality Matters:** Free publishing doesn't mean unprofessional. Edit thoroughly, design well, format properly.

2. **Multiple Books Win:** One book rarely makes a living. Plan a series or write multiple books.

3. **Marketing is Everything:** The best book won't sell without marketing. Spend time learning marketing basics.

4. **Build Your Email List:** This is your most valuable asset. Start from day one.

5. **Be Patient:** Success takes time. Most successful self-published authors took 2-3 years to build sustainable income.

6. **Keep Learning:** Join author communities, read blogs, take free courses, stay updated.

7. **Reinvest:** Once you make money, invest in better covers, editing, and ads.

---

## Frequently Asked Questions

**Q: Is free publishing really professional?**  
A: Yes! Many bestselling authors use these exact platforms. It's not the platform—it's the quality of your work.

**Q: Can I make money with free publishing?**  
A: Absolutely. Many indie authors earn 6-figures+ annually. Your success depends on your book quality and marketing efforts.

**Q: Do I need an LLC or business entity?**  
A: Not required, but beneficial once you're earning significant income. Consult a tax professional.

**Q: What about audiobooks?**  
A: Use ACX.com (free) to create audiobooks for Audible. PublishDrive also distributes audiobooks.

**Q: Should I copyright my book?**  
A: Your book is copyrighted the moment you write it. Formal registration ($65) is optional but recommended for legal protection.

**Q: Can I publish under a pen name?**  
A: Yes! All these platforms support pen names.

**Q: What about libraries?**  
A: PublishDrive distributes to OverDrive and library networks. Draft2Digital partners with library distributors too.

---

## Resources

**Free Tools:**
- Canva (cover design)
- Grammarly (editing)
- Reedsy Book Editor (formatting)
- Hemingway App (readability)
- ProWritingAid (free version)

**Learning Resources:**
- KDP University (free courses)
- The Creative Penn podcast (free)
- Alliance of Independent Authors (membership)
- Self-Publishing Formula podcast (free)
- Kindlepreneur blog (free)

**Helpful Books:**
- "Let's Get Digital" by David Gaughran
- "Write. Publish. Repeat." by Sean Platt & Johnny B. Truant
- "Your First 1000 Copies" by Tim Grahl

---

## Final Thoughts

Publishing your book for free is not only possible—it's the smart choice for most authors. You maintain complete control, keep more money, and have the flexibility to experiment and grow.

**The vanity press model is outdated.** The tools to publish professionally are available to everyone at no cost. Use them.

Start with Amazon KDP to learn the basics, then expand to wide distribution with PublishDrive or Draft2Digital once you're comfortable. Build your author platform, write great books, and market consistently.

**Your publishing journey starts today. For free.**

---

## Quick Start Checklist

- [ ] Finish manuscript (edited and proofread)
- [ ] Create Amazon KDP account
- [ ] Format book for ebook and paperback
- [ ] Design or commission cover
- [ ] Write compelling book description
- [ ] Research keywords and categories
- [ ] Upload to Amazon KDP
- [ ] Create PublishDrive or Draft2Digital account
- [ ] Distribute to wide retailers
- [ ] Build author website (optional but recommended)
- [ ] Start email list
- [ ] Plan marketing strategy
- [ ] Launch!

**Remember:** Every successful self-published author started exactly where you are now. The only difference? They published their book instead of waiting. You can do this. And you can do it for free.'''
}

with app.app_context():
    # Get first admin user
    admin = mongo.db.users.find_one({'role': 'admin'})
    
    if not admin:
        print("No admin user found. Please create an admin user first.")
    else:
        print(f"Found admin: {admin['full_name']}")
        
        # Check if article already exists
        existing = mongo.db.articles.find_one({'title': article_data['title']})
        if existing:
            print(f"Article already exists: {article_data['title']}")
        else:
            article_id = Article.create(
                author_id=str(admin['_id']),
                title=article_data['title'],
                content=article_data['content'],
                category=article_data['category'],
                excerpt=article_data['excerpt'],
                status='published'
            )
            
            print(f"✅ Created article: {article_data['title']}")
            print("Article ID:", article_id)
