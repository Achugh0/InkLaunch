"""
Create article about free publishing platforms
"""

from datetime import datetime
from app import create_app
from app.models import Article, User

app = create_app()

with app.app_context():
    # Find an admin user to be the author
    admin = User.find_by_email('admin@inklaunch.com')
    if not admin:
        from app import mongo
        admin = mongo.db['users'].find_one({'role': 'admin'})
    
    if not admin:
        print("Error: No admin user found")
        exit(1)
    
    admin_id = str(admin['_id'])
    
    title = "Free Publishing Platforms: Your Complete Guide to Draft2Digital, PublishDrive, Amazon KDP, and More"
    
    content = """
# Free Publishing Platforms: Your Complete Guide to Self-Publishing Success

In the world of self-publishing, choosing the right distribution platform can make or break your book's success. Fortunately, several excellent **free** platforms exist to help you get your work into readers' hands without upfront costs. Let's dive deep into the most popular options, their strengths, weaknesses, and which one might be right for you.

---

## The Big Players

### 1. Amazon Kindle Direct Publishing (KDP)

**What It Is:**  
Amazon KDP is the world's largest ebook and print-on-demand platform, giving you direct access to millions of Kindle readers and Amazon's massive marketplace.

**Pros:**
- **Market dominance**: Amazon controls 60-70% of the ebook market
- **Easy to use**: Upload your book, set your price, and you're live within 72 hours
- **KDP Select benefits**: Enroll in Kindle Unlimited for additional income through page reads
- **Print-on-demand**: Paperback and hardcover options with no upfront costs
- **High royalties**: Up to 70% on ebooks priced $2.99-$9.99
- **Free ISBN**: Amazon provides a free ASIN/ISBN for books
- **Built-in audience**: Access to Amazon's recommendation engine and promotional tools
- **Global reach**: Distribute to Amazon stores worldwide

**Cons:**
- **Exclusivity requirements**: KDP Select requires 90-day exclusivity (can't sell ebooks elsewhere)
- **Amazon dependency**: All your eggs in one basket
- **Lower royalties outside range**: Only 35% royalty below $2.99 or above $9.99
- **Limited control**: Amazon sets delivery fees and can change terms
- **Difficult discoverability**: Millions of books make standing out challenging
- **Strict content guidelines**: Risk of account termination for violations

**Best For:** Authors focused on the US market, those willing to go exclusive for KU benefits, or anyone wanting maximum reach with minimal effort.

**Pricing Model:** Free to publish. Amazon takes 30% (or 65%) depending on royalty option.

---

### 2. Draft2Digital (D2D)

**What It Is:**  
Draft2Digital is an aggregator that distributes your ebook to multiple retailers simultaneously, including Apple Books, Barnes & Noble, Kobo, and more.

**Pros:**
- **One upload, multiple stores**: Distribute to 20+ retailers from a single dashboard
- **No exclusivity**: Keep your rights and sell everywhere
- **Free tools**: Professional formatting, built-in ISBN assignment
- **Universal Book Links**: Create smart links that direct readers to their preferred store
- **Author-friendly**: Known for excellent customer service and author advocacy
- **Easy formatting**: Auto-converts Word docs to beautiful ebooks
- **Free ISBN**: Provides ISBNs at no cost
- **Print distribution**: Partner with IngramSpark for print-on-demand (POD)
- **Higher Apple royalties**: Better rates than going direct to Apple

**Cons:**
- **10% commission**: Takes 10% of net proceeds (on top of retailer cuts)
- **Slower payments**: Monthly payments vs. Amazon's 60-day cycle
- **Less control**: Can't run promotions at individual stores
- **No direct Amazon**: Doesn't distribute to Kindle (must do separately)
- **Smaller market reach**: Combined reach is still less than Amazon alone
- **Limited analytics**: Not as detailed as KDP reports

**Best For:** Wide distribution strategy, authors who want to avoid Amazon exclusivity, those who value simplicity over maximum control.

**Pricing Model:** Free to use, but takes 10% of royalties earned from retailers.

---

### 3. PublishDrive

**What It Is:**  
PublishDrive is another aggregator similar to D2D but with additional features like analytics, AI-powered marketing tools, and broader international reach.

**Pros:**
- **Extensive reach**: Distributes to 400+ stores and libraries globally
- **Advanced analytics**: Detailed sales tracking and market insights
- **International focus**: Strong presence in non-English markets
- **Marketing tools**: Built-in promotional features and reader outreach
- **Social DRM**: Option for DRM-free distribution
- **Subscription service distribution**: Access to library lending programs
- **No commission option**: Pay monthly fee instead of percentage
- **AI-powered tools**: Automated marketing and price optimization suggestions
- **API access**: For tech-savvy authors who want custom integrations

**Cons:**
- **10% commission (free tier)**: Takes cut of sales unless you pay monthly
- **Premium pricing**: $120/year to avoid commission fees
- **Learning curve**: More complex interface than D2D
- **Support variability**: Customer service can be hit-or-miss
- **Overlapping distribution**: Some retailers available through multiple channels
- **No Amazon**: Like D2D, doesn't distribute to Kindle

**Best For:** Authors serious about international markets, data-driven marketers, those publishing in multiple languages.

**Pricing Model:** Free with 10% commission, or $10/month (paid annually) for commission-free distribution.

---

### 4. Smashwords

**What It Is:**  
One of the original ebook aggregators, Smashwords distributes to major retailers and has a built-in storefront.

**Pros:**
- **Pioneer platform**: Established reputation since 2008
- **Free ISBN**: Provides ISBN at no cost
- **Direct storefront**: Sell directly to readers from Smashwords.com
- **Library distribution**: Partnerships with OverDrive and library systems
- **Coupon system**: Create discount codes for marketing
- **Pre-order support**: Set up pre-orders across retailers
- **No upload fees**: Completely free to publish
- **Sampling**: Readers can preview up to 20% of your book

**Cons:**
- **Strict formatting**: "Meatgrinder" converter requires specific Word formatting
- **Dated interface**: Platform looks and feels old compared to competitors
- **15% commission**: Higher than D2D's 10%
- **Slower distribution**: Can take weeks to appear on retailer sites
- **Limited print options**: Ebook-focused with minimal POD support
- **Smaller direct sales**: Smashwords storefront traffic is minimal

**Best For:** Authors targeting library distribution, those comfortable with technical formatting, authors who want a direct sales channel.

**Pricing Model:** Free with 15% commission on retailer sales, 11% on direct Smashwords sales.

---

### 5. Google Play Books

**What It Is:**  
Google's ebook platform, allowing direct distribution through Google Play Store.

**Pros:**
- **Google ecosystem**: Integrated with Android devices and Google services
- **Global reach**: Available in 75+ countries
- **High royalties**: 52% on sales under $2.99, 70% above
- **No exclusivity**: Sell anywhere else simultaneously
- **Flexible pricing**: Set prices by territory
- **Direct relationship**: No middleman taking additional cuts
- **EPUB support**: Clean format requirements

**Cons:**
- **Limited market share**: Much smaller than Amazon or Apple
- **Complex setup**: Google Partner Center can be confusing
- **Tax documentation**: Requires extensive tax forms for international sales
- **Low visibility**: Difficult to get discovered among millions of apps/books
- **Support issues**: Customer service can be challenging to reach
- **ISBN required**: Must have your own ISBN (not provided)
- **Payment threshold**: Must earn $10 before payout

**Best For:** Authors with Android-heavy audience, those wanting to diversify beyond major players.

**Pricing Model:** Free to publish, Google keeps 30-48% depending on price point.

---

### 6. Kobo Writing Life

**What It Is:**  
Kobo's direct publishing platform for their ereaders and apps, popular in Canada, Australia, and Europe.

**Pros:**
- **Strong international presence**: Dominates Canadian market, popular in UK/EU
- **70% royalties**: Competitive royalty rates
- **No exclusivity**: Publish wide without restrictions
- **Simple interface**: Clean, easy-to-navigate dashboard
- **Marketing support**: Featured placement opportunities
- **Pre-order tools**: Easy pre-order setup
- **Author programs**: Beta features and promotional opportunities
- **Multiple formats**: EPUB and MOBI support

**Cons:**
- **Limited US reach**: Smaller American market presence
- **Discoverability challenges**: Harder to rank than on Amazon
- **ISBN required**: Must provide your own ISBN
- **Payment delays**: Payments can be slow
- **Limited analytics**: Basic sales reporting
- **Small indie audience**: Most users discover books through retailers, not Kobo direct

**Best For:** Canadian authors, those with international audience, authors going wide.

**Pricing Model:** Free to publish, Kobo keeps 30% (70% to author).

---

### 7. Apple Books for Authors

**What It Is:**  
Apple's direct publishing platform for iBooks/Apple Books on iOS devices and Mac.

**Pros:**
- **Premium audience**: Apple users tend to spend more on books
- **70% royalties**: Among the highest in the industry
- **Beautiful presentation**: Exceptional reading experience
- **Pre-order support**: Up to 365 days in advance
- **No exclusivity**: Sell everywhere simultaneously
- **Series support**: Great tools for series authors
- **Global distribution**: Available in 51 countries

**Cons:**
- **Mac required**: Need macOS to upload directly (or use D2D)
- **Complex interface**: iTunes Producer tool has learning curve
- **Strict requirements**: Rigorous quality standards
- **ISBN needed**: Must have your own ISBN
- **Market share**: Smaller than Kindle despite quality
- **Limited reporting**: Basic sales analytics
- **Approval delays**: Review process can take days

**Best For:** Authors with Mac computers, those targeting premium readers, picture book authors.

**Pricing Model:** Free to publish, Apple keeps 30%.

---

## Comparison Table

| Platform | Commission | Exclusivity | Ease of Use | Global Reach | Print Options | Best For |
|----------|-----------|-------------|-------------|--------------|---------------|----------|
| **Amazon KDP** | 30-65% | Optional | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Yes (POD) | Maximum reach |
| **Draft2Digital** | 10% + retail | No | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Via IngramSpark | Wide distribution |
| **PublishDrive** | 10% or $10/mo | No | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Limited | International |
| **Smashwords** | 15% | No | ⭐⭐⭐ | ⭐⭐⭐⭐ | No | Libraries |
| **Google Play** | 30-48% | No | ⭐⭐⭐ | ⭐⭐⭐⭐ | No | Android users |
| **Kobo** | 30% | No | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | No | Canada/EU |
| **Apple Books** | 30% | No | ⭐⭐ | ⭐⭐⭐⭐ | No | iOS premium |

---

## Choosing Your Strategy

### The "Amazon Exclusive" Strategy
**Best for:** New authors wanting maximum visibility, books suited for Kindle Unlimited

**Setup:**
1. Publish exclusively on Amazon KDP
2. Enroll in KDP Select for KU benefits
3. Use free promo days and Countdown Deals
4. Leverage Amazon Ads

**Pros:** Simplicity, KU income, Amazon marketing tools  
**Cons:** Platform dependency, missed opportunities elsewhere

---

### The "Wide Distribution" Strategy
**Best for:** Established authors, those with international audience, long-term career building

**Setup:**
1. Amazon KDP (not in Select)
2. Draft2Digital for other retailers
3. Direct with Apple Books (if you have Mac)
4. Direct with Google Play

**Pros:** Diversified income, broader readership, no single point of failure  
**Cons:** More complex management, diluted marketing focus

---

### The "Hybrid" Strategy
**Best for:** Authors testing the waters, those with multiple pen names

**Setup:**
1. Some books exclusive on Amazon (in KDP Select)
2. Other books distributed wide through D2D
3. Test which strategy works better for different genres

**Pros:** Best of both worlds, data-driven decisions  
**Cons:** Complex to manage, requires larger catalog

---

## Pro Tips for Success

### 1. **Don't Skip Formatting**
Poor formatting kills sales. Use Vellum ($250 one-time), Atticus ($147), or free tools like Reedsy Book Editor.

### 2. **Invest in a Professional Cover**
Even on free platforms, your cover is your primary marketing tool. Budget $100-300.

### 3. **Get Your Own ISBN (Eventually)**
While free ISBNs work initially, owning your own ($125+ from Bowker) gives you more control and professionalism.

### 4. **Build Your Mailing List**
Platform algorithms change, but your email list is yours forever. Use BookFunnel or StoryOrigin for free reader magnets.

### 5. **Price Strategically**
- Amazon: $2.99-$9.99 for 70% royalty
- Go lower ($0.99) for first in series or promotions
- Bundle series for $9.99-$14.99

### 6. **Monitor Your Metadata**
Titles, subtitles, keywords, and categories matter immensely for discoverability. Update based on performance.

### 7. **Leverage Free Tools**
- **Calibre**: Free ebook formatting and conversion
- **Canva**: Design marketing graphics
- **BookBrush**: Create promotional images
- **BookLinker**: Universal book links

---

## Common Pitfalls to Avoid

❌ **Publishing without editing**: Even free platforms deserve quality content  
❌ **Ignoring cover design**: DIY covers usually hurt sales  
❌ **Not reading terms**: Each platform has specific content policies  
❌ **Setting prices randomly**: Research genre pricing norms  
❌ **Forgetting metadata**: Poor keywords = invisible book  
❌ **Neglecting blurb**: Your description sells the book, not the cover  
❌ **Skipping the preview**: Always check how your book looks before publishing

---

## The Bottom Line

You don't need money to publish your book—just time, effort, and strategy. Here's my recommended starting approach:

**For Complete Beginners:**
1. Start with Amazon KDP only
2. Learn the ropes with one platform
3. Expand once you understand the basics

**For Serious Authors:**
1. Amazon KDP (not in Select)
2. Draft2Digital for wide distribution
3. Build your mailing list from day one
4. Invest earnings into professional services (editing, covers, marketing)

**For International Authors:**
1. PublishDrive for global reach
2. Amazon KDP for US market
3. Kobo Writing Life for Canada/Europe

---

## Final Thoughts

Free publishing platforms have democratized the industry, allowing anyone with a story to reach readers worldwide. The key is choosing the right platform(s) for your goals, understanding the trade-offs, and committing to learning the craft of both writing and marketing.

Remember: **The platform doesn't make the author—quality content, professional presentation, and consistent effort do.**

Start with one platform, master it, then expand. Your publishing journey is a marathon, not a sprint.

---

## Resources to Learn More

- **KDP University**: Amazon's free training for KDP authors
- **Alliance of Independent Authors (ALLi)**: Advocacy and education
- **The Creative Penn**: Joanna Penn's blog and podcast
- **Wide for the Win**: Mark Dawson's course on wide distribution
- **Draft2Digital Blog**: Regular tips on multi-platform publishing

Ready to publish? Pick your platform and take that first step today. Your readers are waiting! 🚀

---

*Have questions about which platform is right for you? Join our [InkLaunch Community Forum](#) where published authors share their experiences and advice.*
"""
    
    excerpt = "Discover the best free publishing platforms for self-publishing authors. Compare Amazon KDP, Draft2Digital, PublishDrive, Smashwords, and more with detailed pros, cons, and strategies for success."
    
    article_id = Article.create(
        author_id=admin_id,
        title=title,
        content=content,
        category='Publishing',
        excerpt=excerpt,
        status='published'
    )
    
    print(f"✅ Article created successfully!")
    print(f"   ID: {article_id}")
    print(f"   Title: {title}")
    print(f"   Category: Publishing")
    print(f"   Status: Published")
    print(f"   Word Count: ~{len(content.split())} words")
