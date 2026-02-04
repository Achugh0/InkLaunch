"""Add Amazon publishing articles to the database."""
from app import create_app, mongo
from app.models import User, Article

app = create_app()

articles = [
    {
        'title': 'Amazon KDP Cover Requirements: Complete Guide for Ebook and Paperback',
        'category': 'Publishing Tips',
        'excerpt': 'Master Amazon KDP cover specifications for both ebook and paperback formats to ensure your book looks professional and passes review.',
        'content': '''# Amazon KDP Cover Requirements: Complete Guide

Getting your book cover right is crucial for success on Amazon. Here's everything you need to know about Amazon KDP cover specifications.

## Ebook Cover Requirements

### Dimensions and Resolution
- **Ideal dimensions**: 2560 x 1600 pixels (1.6:1 ratio)
- **Minimum dimensions**: 1000 x 625 pixels
- **Maximum file size**: 50 MB
- **Resolution**: 72 DPI minimum (300 DPI recommended)
- **Format**: JPEG or TIFF (JPEG preferred)

### Best Practices for Ebook Covers
1. Use high-contrast colors that stand out in thumbnail size
2. Keep text large and readable when scaled down
3. Avoid clutter - simple, bold designs work best
4. Ensure the cover is legible at 50x80 pixels (thumbnail size)

## Paperback Cover Requirements

Paperback covers are more complex because they include the front cover, spine, and back cover.

### Calculating Your Cover Dimensions

**Formula**: (Trim width × 2) + Spine width + 0.25" bleed = Total width
**Height**: Trim height + 0.125" bleed top + 0.125" bleed bottom

### Common Trim Sizes and Spine Widths

**6" x 9" (Most popular)**
- 100 pages: 12.25" x 9.25" total (0.22" spine)
- 200 pages: 12.44" x 9.25" total (0.42" spine)
- 300 pages: 12.67" x 9.25" total (0.65" spine)
- 400 pages: 12.89" x 9.25" total (0.87" spine)

**5" x 8"**
- 100 pages: 10.25" x 8.25" total (0.22" spine)
- 200 pages: 10.44" x 8.25" total (0.42" spine)
- 300 pages: 10.67" x 8.25" total (0.65" spine)

**5.5" x 8.5"**
- 100 pages: 11.25" x 8.75" total (0.22" spine)
- 200 pages: 11.44" x 8.75" total (0.42" spine)
- 300 pages: 11.67" x 8.75" total (0.65" spine)

### Paper Type Affects Spine Width

Amazon offers two paper types:
- **White paper**: Standard weight, thinner spine
- **Cream paper**: Slightly thicker, wider spine

Use Amazon's cover calculator tool to get exact spine width for your page count and paper type.

### Cover Template Requirements

- **Bleed**: 0.125" on all sides (except spine)
- **Safe zone**: Keep text and important elements 0.125" inside trim lines
- **Spine**: Keep spine text at least 0.0625" from spine edges
- **Resolution**: 300 DPI minimum
- **Color mode**: RGB (not CMYK)
- **Format**: PDF (single file for entire cover)

### Barcode Placement

Amazon automatically adds the ISBN barcode. Reserve a 2" x 1.2" space on the back cover, bottom right corner (within safe zone).

## Cover Design Tips

1. **Professional appearance**: Invest in professional design or use quality templates
2. **Genre conventions**: Study bestselling books in your genre
3. **Typography**: Use readable fonts, especially for titles
4. **Color psychology**: Choose colors that evoke the right emotion
5. **Test at thumbnail size**: Your cover must work at small sizes

## Common Mistakes to Avoid

- Low resolution images (causes rejection)
- Text too close to trim lines (gets cut off)
- Ignoring spine text margins (text wraps to front/back)
- Wrong color mode (use RGB, not CMYK)
- Forgetting bleed area
- Not leaving space for barcode

## Using Amazon's Cover Creator

Amazon provides a free cover creator tool that:
- Automatically calculates dimensions
- Ensures correct bleed and margins
- Provides templates
- Handles ISBN barcode placement

While convenient for beginners, professional covers typically require design software like Adobe InDesign, Photoshop, or free alternatives like Canva Pro or GIMP.

## Final Checklist

Before uploading your cover:
- [ ] Correct dimensions with bleed
- [ ] 300 DPI resolution
- [ ] RGB color mode
- [ ] Text in safe zone
- [ ] Barcode space reserved (paperback)
- [ ] Spelled correctly (title, author name)
- [ ] Professional appearance
- [ ] Readable at thumbnail size

A well-designed cover following these specifications will pass Amazon's review process and attract readers to your book.'''
    },
    {
        'title': 'Amazon KDP Publishing: Complete Step-by-Step Guide for First-Time Authors',
        'category': 'Publishing Tips',
        'excerpt': 'Everything you need to know to publish your first book on Amazon Kindle Direct Publishing, from manuscript to marketplace.',
        'content': '''# Amazon KDP Publishing: Your Complete Guide

Publishing on Amazon Kindle Direct Publishing (KDP) has revolutionized the book industry, allowing authors to reach millions of readers worldwide. Here's your complete guide to getting started.

## What is Amazon KDP?

Kindle Direct Publishing is Amazon's self-publishing platform that allows authors to publish ebooks and paperbacks directly to Amazon's marketplace. You retain control over your book's rights, set your own prices, and earn up to 70% royalties.

## Getting Started: Account Setup

1. **Create a KDP account** at kdp.amazon.com
2. **Provide tax information** (W-9 for US, W-8 for international)
3. **Set up payment method** for receiving royalties
4. **Complete your author profile**

## Preparing Your Manuscript

### Formatting Requirements

**Ebook (Kindle):**
- Accept formats: DOC, DOCX, HTML, MOBI, EPUB, TXT
- Recommended: DOC or DOCX with proper formatting
- Include table of contents with hyperlinks
- Remove headers/footers (except page numbers)
- Use standard fonts (Times New Roman, Arial, Garamond)

**Paperback:**
- Accept formats: PDF, DOC, DOCX
- Must be print-ready PDF for best results
- Margins: Minimum 0.25" outside, 0.375" inside
- Bleed: 0.125" if your design extends to edge
- Recommended fonts: Readable serif fonts for body text

### Content Guidelines

Your book must:
- Be at least 24 pages for paperback
- Have proper copyright page
- Include disclaimer if necessary
- Follow Amazon's content guidelines (no prohibited content)
- Be properly edited and proofread

## Creating Your Cover

You have three options:

1. **Amazon Cover Creator**: Free, basic tool within KDP
2. **Professional designer**: Best for quality, costs vary
3. **DIY with templates**: Canva, BookBrush, or similar tools

Ensure covers meet specifications (see our complete cover guide for details).

## Setting Up Your Book Details

### Required Information

1. **Language**: Primary language of your book
2. **Book title and subtitle**: Exactly as they appear on cover
3. **Author name**: Can be pen name or real name
4. **Contributors**: Editors, illustrators, etc. (optional)
5. **Description**: 4000 characters max, use HTML formatting
6. **Publishing rights**: You own or have publishing rights
7. **Keywords**: Up to 7 keywords for discoverability
8. **Categories**: Choose 2 (can add more via Amazon Author Central)
9. **Age and grade range**: If applicable (children's books)

### Writing an Effective Book Description

Your description is crucial for sales. Use this structure:

1. **Hook**: Grab attention in first sentence
2. **What the book is about**: 2-3 paragraphs
3. **Who it's for**: Target audience
4. **Call to action**: Encourage purchase
5. **HTML formatting**: Use bold, italics, bullets for readability

Example HTML tags:
```html
<b>Bold text</b>
<i>Italic text</i>
<br> Line break
<ul><li>Bullet point</li></ul>
```

## Choosing Your Keywords

Keywords help readers find your book. Best practices:

- Use all 7 keyword slots
- Be specific (not just "fiction")
- Include genre variations ("psychological thriller", "mystery thriller")
- Add phrases readers might search ("strong female protagonist")
- Avoid words already in your title/subtitle
- Research competitor keywords
- Don't use trademarked terms

## Selecting Categories

Categories determine where your book appears in Amazon's store:

- Choose relevant, specific categories
- Start with 2 during setup
- Add up to 8 more through Amazon Author Central
- Browse bestseller lists to find less competitive categories
- Subcategories are easier to rank in than main categories

## Pricing Strategy

### Ebook Pricing

**70% Royalty Option:**
- Price between $2.99 - $9.99
- Book must be available in all territories
- File size fee applies (delivery costs)
- Best for most authors

**35% Royalty Option:**
- Price $0.99 - $200
- Good for loss leaders or premium pricing
- No delivery fees

### Paperback Pricing

Calculate minimum price based on:
- Printing costs (varies by page count, trim size, paper type)
- Amazon's cut
- Your desired royalty

Formula: Printing cost + Amazon cut + your royalty = list price

### Pricing Tips

- Research competitor pricing in your genre
- Consider promotional pricing for launch
- $2.99 is popular for debut novels
- $0.99 can boost visibility but reduces royalties
- Higher prices can signal quality

## Pre-Order Strategy

Set up pre-orders to:
- Build anticipation
- Improve launch day rankings
- Gather early reviews
- Test marketing strategies

Pre-orders available 90 days before release (ebook) or 270 days (paperback).

## Publishing and Review Process

1. **Upload your files**: Manuscript and cover
2. **Preview your book**: Use online previewer or download file
3. **Check for errors**: Formatting issues, missing images, etc.
4. **Submit for review**: Usually 24-72 hours
5. **Go live**: Once approved, book appears on Amazon

## After Publishing: Marketing

### Essential Marketing Steps

1. **Amazon Author Central**: Claim and complete your profile
2. **Share your launch**: Social media, email list, blog
3. **Request reviews**: Ask readers to leave honest reviews
4. **Run promotions**: Price drops, free days (KDP Select)
5. **Continue writing**: More books = more visibility

### KDP Select vs. Wide Distribution

**KDP Select (Exclusive to Amazon):**
- Earn from Kindle Unlimited page reads
- Access to promotional tools (Free Book Promotion, Countdown Deals)
- Higher visibility in Amazon ecosystem
- 90-day commitment required

**Wide Distribution:**
- Publish on multiple platforms (Draft2Digital, Apple Books, etc.)
- Reach more readers
- Not limited to Amazon ecosystem
- No page read bonuses

## Understanding Royalties

Royalties are paid approximately 60 days after the end of the month of sale.

**Payment threshold**: $100 minimum (US), varies by country

**Report access**: Real-time sales data in KDP dashboard

## Common Mistakes to Avoid

1. Poor cover design
2. Inadequate editing/proofreading
3. Weak book description
4. Ignoring keywords and categories
5. Wrong pricing strategy
6. Not building an author platform
7. Expecting instant success
8. Forgetting to market

## Success Tips

- **Write multiple books**: Series sell better
- **Build an email list**: Own your audience
- **Learn marketing**: Essential for self-publishing success
- **Join author communities**: Facebook groups, forums
- **Keep learning**: Industry changes constantly
- **Be patient**: Success takes time
- **Focus on quality**: Content is still king

## Resources

- **KDP Help**: kdp.amazon.com/help
- **KDP Community**: kdpcommunity.amazon.com
- **Cover Calculator**: kdp.amazon.com/cover-calculator
- **Preview Tool**: Built into KDP dashboard
- **Amazon Author Central**: author.amazon.com

Publishing on Amazon KDP is accessible to anyone with a story to tell. Focus on creating quality content, professional presentation, and strategic marketing. Your first book is just the beginning of your publishing journey.'''
    },
    {
        'title': 'Amazon Book Marketing Strategies: Boost Your Sales in 2026',
        'category': 'Marketing Strategies',
        'excerpt': 'Proven marketing strategies to increase your book visibility and sales on Amazon, including advertising, promotions, and organic tactics.',
        'content': '''# Amazon Book Marketing Strategies That Actually Work

Getting your book seen on Amazon requires more than just publishing it. Here are proven marketing strategies to boost your visibility and sales.

## Optimize Your Book Listing

### Title and Subtitle Optimization
Your title is your first impression. Make it count:
- Include genre indicators or key themes
- Use subtitles to clarify what the book offers
- Keep it memorable and searchable
- Check if your title is unique or overused

### Description Mastery
Your book description has two audiences:
1. **Amazon's algorithm**: Needs keywords
2. **Human readers**: Needs persuasion

**Winning description formula:**
- Hook in first line
- Establish stakes
- Introduce protagonist (fiction) or benefits (non-fiction)
- Create curiosity
- End with call-to-action
- Use HTML formatting (bold, bullets, line breaks)

### Keyword Research
Keywords are how readers find your book:
- Use all 7 keyword boxes
- Research using Publisher Rocket or similar tools
- Analyze competitor keywords
- Include long-tail phrases ("cozy mystery with cats")
- Update keywords based on performance
- Avoid keyword stuffing

### Category Strategy
Categories determine your competition:
- Select 2 during upload
- Add up to 8 more via Author Central or by contacting Amazon
- Target less competitive subcategories
- Aim for #1 in subcategories rather than top 100 in main categories
- Browse bestseller lists to find opportunities

## Amazon Advertising (AMS)

### Sponsored Products Ads
The most effective Amazon ad type:

**Campaign Types:**
- **Automatic targeting**: Amazon chooses keywords
- **Manual targeting**: You choose specific keywords

**Budget recommendations:**
- Start with $5-10/day
- Monitor daily for first week
- Adjust based on ACoS (Advertising Cost of Sale)

**Targeting strategies:**
- ASIN targeting: Show ads on competitor book pages
- Keyword targeting: Appear in search results
- Category targeting: Reach broader audience

### Optimizing Your Ads
- Target ACoS: Under 70% for profit
- Negative keywords: Exclude non-performing searches
- Bid optimization: Start low, increase for winners
- A/B test ad copy
- Use compelling book covers
- Monitor click-through rate (CTR)

### Lockscreen Ads
- Available in KDP Select
- Appear when Kindle wakes up
- Lower cost per click
- Good for brand awareness

## Pricing Strategies

### Launch Pricing
**Option 1: Low price launch**
- $0.99 for first week
- Builds momentum and reviews
- Lower profit but higher visibility

**Option 2: Standard pricing**
- $2.99-4.99 from day one
- Better profit margins
- Signal quality with pricing

### Countdown Deals (KDP Select)
- Limited-time discount shown with timer
- Creates urgency
- Doesn't affect price history significantly
- Can run once every 30 days

### Free Book Promotions (KDP Select)
- Make book free for 1-5 days
- Great for visibility and reviews
- Often followed by sales bump
- Can run once per 90-day KDP Select period

## Building Your Email List

Email list is your most valuable asset:

**Why email matters:**
- You own the list (platform-independent)
- Direct communication with fans
- Announce new releases
- Run exclusive promotions
- Build relationships

**How to build:**
- Offer free book (lead magnet)
- Include link in back matter
- Landing page on your website
- Social media promotion
- Reader magnets in your genre

**Email service providers:**
- BookFunnel or StoryOrigin (author-specific)
- Mailchimp, ConvertKit, MailerLite
- Automate welcome sequence

## Review Strategy

Reviews are social proof that sells books:

### Getting Reviews
- Include gentle request in back matter
- Use Amazon's "Request a Review" button
- Share on social media
- Email list announcements
- ARC (Advance Review Copy) team
- NetGalley or BookSirens

### Review Guidelines
- Never buy reviews (violation)
- Don't pressure friends/family
- No review swaps on Amazon
- Request honest reviews only
- Don't respond negatively to bad reviews

## Social Media Marketing

### Amazon Author Central
Must-have profile setup:
- Professional author photo
- Compelling bio
- Link to blog/website
- Follow button
- Editorial reviews section

### Platform-Specific Strategies

**Facebook:**
- Join genre reader groups
- Share behind-the-scenes content
- Run giveaways
- Consider Facebook Ads
- Engage authentically

**Instagram:**
- Bookstagram community
- Visual content (book photos, quotes)
- Use relevant hashtags
- Collaborate with bookstagrammers
- Stories for engagement

**TikTok (BookTok):**
- Huge potential for viral growth
- Short video reviews drive massive sales
- Send free copies to BookTokers
- Create your own content
- Trends move fast

**Twitter:**
- Writing community active here
- Share updates and thoughts
- Network with other authors
- Participate in writing hashtags (#WritingCommunity)

## Content Marketing

### Author Website
Essential for professional presence:
- Book pages with buy links
- About page
- Blog for SEO
- Email signup form
- Contact information

### Blogging
- Drives organic traffic
- Establishes authority
- Supports email list growth
- Long-term investment

### Guest Posting
- Write for sites in your niche
- Link back to your books
- Build authority and backlinks

## Book Promotion Sites

Submit to promotional newsletters:

**Free sites:**
- BookBub (hardest to get accepted)
- Freebooksy
- Robin Reads
- Bargain Booksy
- Many Books

**Paid sites:**
- BookBub Featured Deals ($500+, best ROI)
- Written Word Media
- BookGorilla
- eReader News Today

**Tips:**
- Best results with 10+ reviews
- Free or $0.99 books perform best
- Submit weeks in advance
- Track results by source

## Series Strategy

Series outsell standalone books:
- Hook readers with book 1
- Price book 1 lower (loss leader)
- Release books close together
- Include preview of next book
- Consider box sets later

## Amazon Algorithms

Understand what Amazon rewards:

### Sales Velocity
- Sales concentrated in short time period
- Better than same sales spread out
- Launch strategies capitalize on this

### Also-Bought
- Appears when books are purchased together
- Cross-promotion opportunity
- Takes time to develop

### Popular Highlights
- Kindle readers highlighting your text
- Signals engagement
- Can attract new readers

## Launch Strategy

A strong launch sets up long-term success:

### Pre-Launch (30-90 days):
- Build email list
- Line up ARC readers
- Create marketing materials
- Set up pre-order
- Plan launch promotions

### Launch Week:
- Heavy promotional push
- Email list announcement
- Social media blitz
- Paid ads
- Promotion sites
- Request reviews

### Post-Launch (30+ days):
- Maintain advertising
- Monitor and adjust keywords
- Respond to reviews
- Continue marketing
- Start next book

## Measuring Success

Track these metrics:
- **Sales rank**: Lower is better
- **Page reads**: KDP Select only
- **Review count**: Social proof
- **ACoS**: Ad efficiency
- **Conversion rate**: Visits to sales
- **Email list growth**: Long-term asset

## Common Marketing Mistakes

1. **No marketing plan**: Publishing without promotion
2. **Giving up too soon**: Marketing takes time
3. **Poor targeting**: Wrong audience for ads
4. **Neglecting back matter**: Missing CTA for next book
5. **One-book author**: Hard to build momentum
6. **Ignoring email**: Relying only on Amazon
7. **Not testing**: Failing to A/B test
8. **Inconsistent effort**: Sporadic marketing

## Advanced Tactics

### Amazon A+ Content
Premium book descriptions available to authors in Brand Registry

### Book Bundling
Package multiple books at discounted price

### Audiobook Strategy
Expand to ACX (Audible) for additional revenue stream

### International Markets
Use Amazon's expanded distribution to reach global readers

## Budget-Friendly Marketing

You don't need a huge budget:
- Focus on organic strategies first
- Start ads small and scale what works
- Leverage social media (free)
- Network with other authors (cross-promotion)
- Write more books (best marketing is next book)

## The Long Game

Remember:
- Success builds over time
- Multiple books multiply success
- Quality content is foundation
- Community matters (readers and writers)
- Consistency beats intensity
- Learn and adapt constantly

Marketing your book on Amazon is both art and science. Test different strategies, measure results, and double down on what works for your specific book and audience. The authors who succeed are those who persistently market their books while continuously writing new ones.'''
    },
    {
        'title': 'Book Description Writing: Hook Readers and Boost Conversions',
        'category': 'Writing Craft',
        'excerpt': 'Master the art of writing compelling book descriptions that convert browsers into buyers with proven formulas and examples.',
        'content': '''# Writing Book Descriptions That Sell

Your book description is your sales pitch. It appears on your Amazon page, in promotions, and anywhere readers discover your book. A great description can dramatically increase your conversion rate from browsers to buyers.

## The Purpose of Book Descriptions

Your description has two jobs:
1. **Convince readers** this book is for them
2. **Include keywords** for Amazon's algorithm

Don't write a synopsis. Write a promise.

## The Hook Formula

### Fiction Book Description Structure

**Paragraph 1: The Hook (1-3 sentences)**
- Introduce protagonist
- Establish stakes
- Create intrigue

**Paragraph 2: The Conflict (2-4 sentences)**
- What's the problem?
- What must the protagonist do?
- What stands in their way?

**Paragraph 3: The Stakes (2-3 sentences)**
- What happens if they fail?
- Raise questions
- Create emotional connection

**Final Line: Call to Action**
- "Scroll up and buy now"
- "Get your copy today"
- "Start reading now"

### Non-Fiction Book Description Structure

**Paragraph 1: The Problem**
- What pain point does your book address?
- Why should readers care?
- Establish relevance

**Paragraph 2: The Solution**
- What will readers learn?
- What transformation will they experience?
- How is your approach unique?

**Paragraph 3: The Benefits (Bullet Points)**
- Specific outcomes
- Skills they'll gain
- Problems they'll solve

**Paragraph 4: Authority**
- Why are you qualified?
- Social proof (if you have it)

**Final Line: Call to Action**
- "Start your transformation today"
- "Buy now to discover..."

## HTML Formatting

Amazon supports HTML in descriptions. Use it:

```html
<b>Bold text</b> - Emphasize key points
<i>Italic text</i> - Titles, emphasis
<br> - Line break
<ul><li>Bullet point</li></ul> - Lists
```

**Example formatted description:**
```html
<b>She thought her secrets were safe. She was wrong.</b><br>
<br>
When Sarah discovers her husband's hidden past, she has 48 hours to decide: protect her family or expose the truth.<br>
<br>
<b>This psychological thriller will keep you up all night...</b><br>
<ul>
<li>Unexpected twists you won't see coming</li>
<li>Complex characters you'll love (and love to hate)</li>
<li>A ending that will leave you breathless</li>
</ul>
```

## Power Words That Sell

Use emotionally charged words:
- **Mystery/Thriller**: deadly, explosive, terrifying, shocking, brutal
- **Romance**: passionate, heartbreaking, sizzling, forbidden, irresistible
- **Fantasy**: epic, magical, legendary, dark, powerful
- **Self-Help**: transform, discover, master, breakthrough, proven

## Comparison Hook

Reference popular books (without being specific):
- "For fans of Gillian Flynn and Paula Hawkins"
- "If you loved The Silent Patient"
- "Readers of Stephen King will devour this"

**Legal note**: Don't use exact titles or trademark names

## Common Mistakes to Avoid

1. **Too long**: Readers skim, keep it concise
2. **Giving away plot**: Mystery sells better than spoilers
3. **Boring opening**: First sentence must grab attention
4. **List of events**: "First this happens, then that..."
5. **No formatting**: Wall of text is overwhelming
6. **Missing call-to-action**: Tell them what to do next
7. **Generic language**: "Amazing journey", "incredible adventure"
8. **No urgency**: Create FOMO (fear of missing out)

## Examples: Before and After

### Before (Weak):
*"This is a story about John, who goes on an adventure. He faces many challenges and has to make difficult decisions. Will he succeed? Read to find out."*

### After (Strong):
**John has 24 hours to stop a conspiracy that will change the world forever.**

**The problem? No one believes him.**

**When a routine investigation uncovers a plot that reaches the highest levels of government, John must race against time, trust no one, and risk everything to expose the truth before it's too late.**

**His enemies are powerful. His resources are limited. And the clock is ticking.**

**A heart-pounding thriller that will keep you on the edge of your seat. Scroll up and grab your copy now.**

## Genre-Specific Tips

### Mystery/Thriller
- Emphasize danger and stakes
- Use questions to create curiosity
- Short, punchy sentences
- Create urgency

### Romance
- Focus on emotional connection
- Hint at conflict keeping them apart
- Promise satisfying ending (genre expectation)
- Use sensory language

### Science Fiction/Fantasy
- Establish unique world elements
- Make stakes clear (world-ending?)
- Introduce magic system or tech briefly
- Appeal to genre fans specifically

### Self-Help/Non-Fiction
- Lead with transformation promise
- Use numbers (7 steps, 5 strategies)
- Include bullets for scannability
- Establish credentials
- Show, don't tell (results, not process)

## Testing Your Description

Ask yourself:
- Would I buy this book based on this description?
- Does it create curiosity?
- Are the stakes clear?
- Does it target my ideal reader?
- Is it skimmable?

**Test it**: Change your description and monitor conversion rates. Amazon allows updates anytime.

## Keywords in Descriptions

Include relevant search terms naturally:
- Genre descriptors
- Themes
- Similar author names (general, not specific)
- Reader search phrases

Don't keyword stuff. Natural language that includes keywords is ideal.

## Length Guidelines

**Sweet spot**: 150-300 words for fiction, 300-500 for non-fiction

Readers decide quickly. Respect their time.

## Social Proof

If you have it, include:
- Awards or bestseller status
- Number of reviews/ratings
- Reader testimonials (not full reviews)
- Media mentions

Place at the beginning or end for maximum impact.

## Call-to-Action Best Practices

End with clear direction:
- "Scroll up and click 'Buy Now'"
- "Get your copy today"
- "Start reading now"
- "Join thousands of readers who..."

Create urgency without being pushy.

## Updating Your Description

Your description isn't set in stone:
- Update when you get reviews
- Improve based on reader feedback
- Test different approaches
- Add awards or achievements
- Refine as you learn

Check competitors' descriptions regularly for inspiration (don't copy).

## Final Checklist

Before publishing your description:
- [ ] Compelling hook in first sentence
- [ ] Clear conflict/problem
- [ ] Emotional stakes established
- [ ] Genre-appropriate tone
- [ ] HTML formatting applied
- [ ] Keywords included naturally
- [ ] Call-to-action at end
- [ ] Proofread (typos kill credibility)
- [ ] Length appropriate
- [ ] Would YOU buy based on this?

Your book description is often the deciding factor between a browse and a buy. Invest time in crafting it well, and you'll see the difference in your conversion rate.'''
    },
    {
        'title': 'Platform Updates: Latest Amazon KDP Features and Changes',
        'category': 'Platform Updates',
        'excerpt': 'Stay current with the newest Amazon KDP features, policy updates, and tools available to authors in 2026.',
        'content': '''# Amazon KDP Platform Updates 2026

Amazon continuously updates its Kindle Direct Publishing platform. Staying informed helps you leverage new features and adapt to changes.

## Recent Major Updates

### Enhanced Content Tools (2026)

**A+ Content for All Authors**
Previously limited to vendors, now available to all KDP authors:
- Premium book description layouts
- Image galleries
- Comparison charts
- Enhanced formatting options
- Better mobile display

**How to access:**
1. Go to your KDP Bookshelf
2. Click the ellipsis (…) next to your book
3. Select "A+ Content"
4. Choose from templates
5. Submit for approval

**Benefits:**
- Higher conversion rates
- Better visual presentation
- Enhanced storytelling
- Professional appearance

### AI-Generated Cover Variations (New)

Amazon now tests multiple cover variations:
- Automatic A/B testing
- Shows different covers to different customers
- Measures which converts better
- Authors can opt-in or create variations manually

**How it works:**
- Upload 2-3 cover variations
- Amazon rotates them automatically
- Analytics show performance
- Keep the winner

### Improved Royalty Reporting

Real-time updates now include:
- Hour-by-hour sales data
- Page read tracking by title
- International sales breakdown
- Ad spend vs. royalty dashboard
- Conversion rate metrics

**New dashboard features:**
- Visual graphs and trends
- Export to CSV
- Custom date ranges
- Comparison tools

### Expanded Distribution

**New territories added:**
- Additional European markets
- Southeast Asian markets
- African markets via partnerships

**Improved print-on-demand:**
- Faster shipping times
- Better quality control
- More paper options
- Additional trim sizes

### Enhanced Advertising Platform

**New ad types:**
- Video ads (beta)
- Sponsored Brands for authors
- Cross-device targeting
- Lookalike audiences

**Improved targeting:**
- Genre-based audiences
- Reader interest categories
- Purchase behavior targeting
- Seasonal campaign templates

## Policy Changes to Note

### Review Guidelines (Updated)

**Stricter enforcement on:**
- Review swaps (prohibited)
- Incentivized reviews (except ARC)
- Family and friend reviews (discouraged)
- Fake reviews (immediate removal)

**New requirement:**
- Amazon verified purchase badge carries more weight
- Editorial reviews section expanded

### Content Guidelines

**Clarifications on:**
- AI-generated content (must be disclosed)
- Public domain content (must add substantial value)
- Translated works (proper attribution required)
- Sensitive content (better categorization)

### Pricing Flexibility

**New pricing tools:**
- Schedule price changes in advance
- Seasonal pricing automation
- Market-based pricing suggestions
- Countdown deal improvements

## New Tools and Resources

### Cover Calculator Update

The cover calculator now includes:
- Hardcover specifications
- More trim sizes
- Better spine width accuracy
- Automatic template generation

### Preview Tool Enhancement

**3D book preview:**
- See how your book appears in 3D
- Multiple angle views
- Realistic page flip animation
- Share on social media

### Metadata Optimizer (Beta)

AI-powered suggestions for:
- Keyword opportunities
- Category recommendations
- Description improvements
- Pricing optimization

**Access**: Available in "Marketing" tab

### Series Management

New series tools:
- Link books in a series officially
- Series page on Amazon
- Reading order display
- Series promotion options

**How to set up:**
1. Go to bookshelf
2. Click "Add to series"
3. Name your series
4. Set reading order
5. Amazon creates series page

## Mobile App Updates

### KDP Mobile App Features

**New capabilities:**
- Upload books from mobile
- Edit book details
- Monitor sales on-the-go
- Respond to reviews (coming soon)
- Run ad campaigns
- Price updates

**Available**: iOS and Android

## International Author Support

### Expanded Language Support

KDP now supports:
- 20+ interface languages
- Improved translation tools
- Better international payment options
- Local currency pricing

### Regional Marketing Tools

**Country-specific campaigns:**
- Target individual markets
- Localized ad copy
- Currency-based pricing
- Regional bestseller tracking

## Kindle Unlimited Updates

### Page Read Improvements

**Better tracking:**
- More accurate page reads
- Faster reporting
- Bonus pool adjustments
- Genre-based rates (testing)

### KDP Select Benefits

**New promotional tools:**
- Extended Free Book Promotion periods
- Better Countdown Deal scheduling
- Pre-order promotion options
- Exclusive launch features

## Audiobook Integration

### ACX Connection

Seamless integration with ACX:
- Link Kindle and audiobook editions
- Whispersync for Voice
- Bundle pricing options
- Cross-promotion tools

## Author Central Improvements

**Enhanced profile features:**
- Video author message
- Upcoming events calendar
- Newsletter signup integration
- Podcast linking
- Enhanced analytics

## Print-on-Demand Enhancements

### Quality Improvements

**New options:**
- Premium color printing
- Expanded paper choices
- Better cover finishes (gloss, matte, silk)
- Hardcover availability (expanding)

### Trim Size Additions

New sizes available:
- 7" x 10" (perfect for textbooks)
- 8.25" x 6" (pocket size)
- Custom sizes (select accounts)

## Coming Soon

### Announced Features (2026 Roadmap)

**Q2 2026:**
- Enhanced analytics dashboard
- Author messaging system (connect with readers)
- Improved recommendation algorithm
- Better international royalty payments

**Q3 2026:**
- NFT collectibles for books (pilot program)
- Advanced A/B testing for pricing
- Author subscription platform
- Live events integration

**Q4 2026:**
- Virtual book launch tools
- Enhanced social media integration
- AI writing assistant (beta)
- Reader engagement metrics

## How to Stay Updated

**Official sources:**
- KDP Blog: kdp.amazon.com/blog
- KDP Help: Check "What's New" section
- Email notifications: Enable in settings
- KDP Community Forums: kdpcommunity.amazon.com

**Third-party resources:**
- Publishing newsletters
- Author Facebook groups
- Industry blogs and podcasts
- Author conferences

## Adapting to Changes

**Best practices:**
- Review updates quarterly
- Test new features on backlist first
- Join beta programs when available
- Network with other authors
- Stay flexible in your strategy

## Feature Requests

Amazon listens to author feedback:
- Submit via KDP Support
- Vote in community forums
- Participate in surveys
- Join focus groups (when offered)

## Impact on Your Strategy

**Regular review checklist:**
- [ ] Check for new advertising options
- [ ] Update book metadata with new tools
- [ ] Explore new promotional features
- [ ] Review policy changes
- [ ] Test new pricing tools
- [ ] Utilize improved analytics
- [ ] Update cover if new options available
- [ ] Link series properly
- [ ] Optimize for new algorithms

## Conclusion

Amazon KDP evolves constantly. Successful authors stay informed and adapt quickly. Bookmark this guide and check back quarterly for updates. The authors who leverage new features early often gain competitive advantages.

Set a reminder to review KDP updates monthly. Small changes can lead to significant improvements in your book's performance.'''
    }
]

with app.app_context():
    # Get first admin user
    admin = mongo.db.users.find_one({'role': 'admin'})
    
    if not admin:
        print("No admin user found. Please create an admin user first.")
    else:
        print(f"Found admin: {admin['full_name']}")
        
        for article_data in articles:
            # Check if article already exists
            existing = mongo.db.articles.find_one({'title': article_data['title']})
            if existing:
                print(f"Article already exists: {article_data['title']}")
                continue
            
            article_id = Article.create(
                author_id=str(admin['_id']),
                title=article_data['title'],
                content=article_data['content'],
                category=article_data['category'],
                excerpt=article_data['excerpt'],
                status='published'
            )
            
            print(f"Created article: {article_data['title']}")
        
        print(f"\nSuccessfully added {len(articles)} articles!")
