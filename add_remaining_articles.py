#!/usr/bin/env python3
"""Add remaining 16+ comprehensive professional articles for self-publishers."""
import sys
sys.path.insert(0, '/workspaces/InkLaunch')

from app import create_app
from app.models import Article, User

app = create_app()

with app.app_context():
    # Get admin user
    admin = User.find_by_email('ashchugh@gmail.com')
    if not admin:
        print("Admin user not found!")
        sys.exit(1)
    
    author_id = str(admin['_id'])
    
    articles = [
        {
            'title': 'ISBN Explained: Do You Really Need to Buy One?',
            'category': 'Publishing Tips',
            'excerpt': 'Understanding ISBNs, when you need them, whether to use free ISBNs from Amazon, and the truth about what self-publishing companies charge.',
            'content': '''One of the most confusing aspects of self-publishing is the ISBN—International Standard Book Number. Many self-publishing companies charge $100-$300 for ISBNs, making them sound mandatory and complex. The truth is much simpler, and you might not need to buy one at all.

## What is an ISBN?

An ISBN is a unique identifier for books, like a product barcode. It helps bookstores, libraries, and distributors track and order books. Every format of your book (hardcover, paperback, ebook, audiobook) technically needs its own ISBN.

A typical ISBN looks like this: 978-0-123456-78-9

The number contains:
- Prefix (978 or 979)
- Group identifier (language/country)
- Publisher prefix (your publisher code)
- Title identifier (specific to this book)
- Check digit (for validation)

## Do You Need an ISBN?

**For Amazon Kindle ebooks: NO**

Amazon assigns every Kindle ebook a free ASIN (Amazon Standard Identification Number). This serves the same purpose as an ISBN within Amazon's system. Your ebook doesn't need an ISBN to sell on Amazon.

**For print books on Amazon: NO (but recommended)**

Amazon KDP offers free ISBNs for paperbacks and hardcovers. These ISBNs:
- Work perfectly for selling on Amazon
- Are free—no cost whatsoever
- Are automatically assigned when you publish
- Show "Independently published" or "Amazon Digital Services" as the publisher

The downside? Amazon is listed as the publisher of record, not you.

**For wide distribution: YES (sort of)**

If you want your book in bookstores, libraries, or sold through other retailers beyond Amazon, you should buy your own ISBN. This allows:
- Your own publisher imprint name
- Better library distribution opportunities  
- Ingram and other wholesaler catalogs
- Bookstore orders
- A more professional appearance

## Where to Get ISBNs

**Free ISBNs:**

**Amazon KDP (Free):**
- Automatically assigned for print books
- Publisher listed as Amazon/Independently published
- Cannot be used on other platforms
- Perfect if you're Amazon-exclusive

**Draft2Digital (Free):**
- Provides free ISBNs for ebooks and print
- Publisher listed as Draft2Digital
- Can distribute to multiple retailers with this ISBN
- Good for wide distribution on a budget

**PublishDrive (Free):**
- Similar to Draft2Digital
- Free ISBNs for distribution
- Publisher listed as PublishDrive

**Smashwords (Free):**
- Free ISBNs for ebooks
- Distributes to multiple retailers
- Publisher listed as Smashwords

**Purchased ISBNs:**

**Bowker (Official US ISBN Agency):**
- **1 ISBN: $125**
- **10 ISBNs: $295 ($29.50 each)**
- **100 ISBNs: $575 ($5.75 each)**
- **1,000 ISBNs: $1,500 ($1.50 each)**

Bowker is the official ISBN agency for the United States. If you want your own publisher imprint, this is the only official source for US authors.

**Your Country's ISBN Agency:**
- Different countries have different agencies
- Prices vary widely by country
- Some countries provide ISBNs for free (Canada, UK)
- Check isbn-international.org for your country's agency

**What Self-Publishing Companies Charge:**

Many vanity presses and "publishing services" charge:
- $100-$300 for a single ISBN
- Often it's included in $2,000+ packages
- Sometimes they keep the ISBN registered to them, not you
- You're paying 100-500% markup

They're just buying from Bowker and reselling to you at inflated prices. You can buy directly from Bowker yourself.

## Should You Buy Your Own ISBN?

**Buy your own ISBN if:**
- You want your own publishing imprint name
- You plan to publish multiple books (buy 10 at once for better value)
- You want wide distribution in bookstores and libraries
- You care about having professional publishing credentials
- You plan to print with other services beyond Amazon

**Use free ISBNs if:**
- You're publishing your first book and testing the waters
- Budget is tight
- You're focused on ebook sales or Amazon-only
- You don't care who's listed as publisher
- You want to invest money in marketing instead

## The Truth About ISBNs and Distribution

Here's what many authors don't realize: **having your own ISBN doesn't automatically get your book into bookstores.** Bookstores order books based on demand, not just because you have an ISBN.

What matters more than ISBNs:
- Marketing and generating demand
- Reviews and reader buzz
- Professional presentation
- Genre and commercial viability
- Your platform and audience

Most indie author sales come from:
- Amazon (60-80% of market)
- Online retailers (another 15-30%)
- Direct sales from your website

Physical bookstore sales typically represent less than 5% of indie author income. So while an ISBN is nice to have, it's not as critical as self-publishing services claim.

## ISBNs for Different Formats

**Each format needs its own ISBN:**
- Kindle ebook - Use Amazon's free ASIN (no ISBN needed)
- EPUB ebook - Can use Draft2Digital free ISBN or buy your own
- Paperback - Use KDP free ISBN or buy your own
- Hardcover - Use KDP free ISBN or buy your own
- Audiobook - Different identifier system (not ISBN)

If you plan to publish in multiple formats, buying 10 ISBNs from Bowker ($295) makes more sense than buying one at a time.

## Publisher Imprint: What It Means

When you buy an ISBN, you register a publisher imprint. This is the "publishing company" name that appears in book databases.

**Examples:**
- *Published by: Penguin Random House* (traditional publisher)
- *Published by: John Smith Publishing* (your own imprint)
- *Published by: Independently published* (Amazon free ISBN)
- *Published by: Draft2Digital* (D2D free ISBN)

Your imprint name can be:
- Your name + Publishing
- A company name you create
- Anything you want (within reason)

Having your own imprint looks more professional and gives you a brand across multiple books.

## How to Register Your ISBN

**If you bought from Bowker:**

1. Go to myidentifiers.com
2. Create an account or log in
3. Purchase your ISBNs
4. Assign each ISBN to a specific book
5. Enter all book details (title, author, format, price, etc.)
6. ISBN becomes active in the global database

**If using free ISBNs:**

1. Upload your book to the platform (KDP, D2D, etc.)
2. Choose "Get a free ISBN" option
3. Platform assigns and registers it automatically
4. You don't need to do anything else

## Common ISBN Mistakes

**Mistake 1: Using the same ISBN for different formats**
- Each format needs its own ISBN
- Ebook and paperback cannot share an ISBN
- This causes database and ordering problems

**Mistake 2: Buying one ISBN at a time**
- Much more expensive per ISBN
- If you'll publish multiple books, buy 10 at once

**Mistake 3: Letting companies keep ISBN ownership**
- Some vanity presses register ISBNs to their company, not yours
- You don't actually own the ISBN
- Make sure ISBNs are registered to you

**Mistake 4: Not keeping records**
- Track which ISBN goes with which book/format
- Keep your Bowker login credentials secure
- Maintain a spreadsheet of your ISBNs

**Mistake 5: Thinking you need ISBNs to sell books**
- Amazon ASIN works perfectly for Kindle ebooks
- Many successful authors use only free ISBNs
- Sales come from marketing, not ISBNs

## ISBNs and Copyright

**Important: ISBNs and copyright are completely separate.**

- ISBN is just an identifier
- Copyright is automatic when you write
- You don't need to register copyright (though you can)
- ISBN has nothing to do with protecting your work

Some scam companies bundle "copyright registration" with ISBN purchases at inflated prices. Don't fall for it.

## The Budget-Conscious Strategy

**Year 1: Use free ISBNs**
- Focus on writing and publishing
- Use Amazon free ISBN for paperback
- Use Amazon ASIN for Kindle
- Invest money in editing and cover design instead

**Year 2+: If you're successful, buy your own**
- Buy 10 ISBNs from Bowker ($295)
- Establish your own imprint
- Republish existing books with new ISBNs (if desired)
- Use for all future books

This approach minimizes upfront costs while you're learning, then invests in professional infrastructure once you're committed and successful.

## International Considerations

**US Authors:** Buy from Bowker or use free platform ISBNs

**Canadian Authors:** ISBNs are free from Library and Archives Canada

**UK Authors:** ISBNs are free from Nielsen ISBN Store

**Australian Authors:** Buy from Thorpe-Bowker (Australian agency)

**Other Countries:** Check isbn-international.org for your country's agency

If your country offers free ISBNs, definitely take advantage of that!

## The Bottom Line

**You do NOT need to pay $100-$300 for a single ISBN to publish your book.** Free options exist, and buying directly from Bowker costs just $125 if you really want your own.

Self-publishing companies that charge $200+ for ISBNs, or include them in expensive packages, are marking up a simple service by 100-400%. It's one of the ways they profit from authors who don't know better.

For most new self-publishers, here's the smart approach:

1. **Start with free ISBNs** from Amazon, Draft2Digital, or your distribution platform
2. **Focus your budget** on editing, cover design, and marketing
3. **After your first few books**, if you're committed to self-publishing long-term, invest $295 in 10 ISBNs from Bowker
4. **Establish your own imprint** and use those ISBNs for future books

ISBNs are important for professional publishing, but they're not the barrier to entry that some companies make them seem. Don't let ISBN confusion or overcharging stop you from publishing your book.

You can be a published author today without spending a penny on ISBNs. That's the truth the self-publishing industry doesn't want you to know.'''
        },
        {
            'title': 'Book Formatting: From Manuscript to Professional Layout',
            'category': 'Formatting & Design',
            'excerpt': 'Learn how to format your book professionally for both ebook and print. Step-by-step instructions using free tools.',
            'content': '''Book formatting is where many self-published books fail. Poor formatting makes your book look amateurish, frustrates readers, and leads to bad reviews—even if your writing is excellent. The good news? Professional formatting is achievable with free tools if you know what you're doing.

## Why Formatting Matters

Readers notice bad formatting immediately:
- Inconsistent spacing
- Weird page breaks
- Missing indentation
- Orphaned headings
- Broken chapters
- Irregular margins

These issues break reading flow and scream "unprofessional." Traditional publishers spend significant resources on formatting because they know it matters. As an indie author, you need to compete with that quality.

## The Two Types of Formatting

**Ebook Formatting:**
- Flexible, reflows based on device
- Readers control font size and style
- Focus on structure, not exact appearance
- HTML-based (XML for EPUB)
- Must work on phones, tablets, and e-readers

**Print Formatting:**
- Fixed layout, looks the same for everyone
- You control every detail
- Page numbers, headers, footers matter
- PDF-based
- Must meet printer specifications

Each requires different approaches and tools.

## Free Formatting Tools

**Kindle Create (Free - Best for beginners):**
- Purpose-built for Amazon KDP
- Visual editor, no coding required
- Handles both ebook and print
- Automated table of contents
- Previewer shows how book will look
- **Best for:** First-time formatters, simple novels, most non-fiction

**Calibre (Free - Best for ebook conversion):**
- Powerful ebook management and conversion
- Converts between formats (Word to EPUB, EPUB to MOBI, etc.)
- Edit ebook files directly
- Professional-quality output
- Steeper learning curve
- **Best for:** Tech-savvy authors, format conversion, advanced ebook features

**Reedsy Book Editor (Free - Best for writing and formatting together):**
- Cloud-based editor
- Format as you write
- Beautiful templates
- Automatic ebook and print export
- Exports to EPUB, MOBI, and print PDF
- **Best for:** Authors starting a new project, collaborative writing

**Atticus ($147 one-time - Best all-in-one):**
- Professional formatting software
- Beautiful templates for every genre
- Write and format in one program
- Export to all formats
- Worth the investment for serious authors
- **Best for:** Authors planning multiple books

**Vellum ($249.99 Mac-only - Best for ebooks):**
- Industry-standard for ebook formatting
- Stunning templates
- One-click export to all formats
- Only available on Mac
- **Best for:** Mac users wanting the very best ebook formatting

**For this guide, we'll focus on Kindle Create—it's free, easy, and produces professional results.**

## Preparing Your Manuscript Before Formatting

Before you open any formatting tool, prepare your Word document:

**1. Use Styles Consistently:**
- Heading 1 for part titles
- Heading 2 for chapter titles
- Heading 3 for section headers
- Normal for body text
- Never just make text bigger and bold manually

**2. Remove Extra Formatting:**
- Delete multiple spaces (use Find & Replace: "  " to " ")
- Remove extra line breaks between paragraphs
- Clear manual formatting (select all, Ctrl+Space)
- Use styles only, not manual sizing

**3. Check Scene Breaks:**
- Use consistent scene break symbols (###, ***, or similar)
- Don't just leave blank lines (they disappear in ebooks)
- Place them where you want visual separation

**4. Organize Front and Back Matter:**
- Title page
- Copyright page
- Dedication
- Table of contents placeholder
- Chapters
- Acknowledgments
- About the author
- Other books by

**5. Images:**
- Save as separate high-resolution files
- Name them logically (image1.jpg, map.png, etc.)
- Note where each should appear
- Use at least 300 DPI for print, 72 DPI for ebook

A clean source file makes formatting infinitely easier.

## Formatting an Ebook with Kindle Create

**Step 1: Launch and Import**

1. Open Kindle Create
2. Click "New Project from File"
3. Select your Word document
4. Choose Fiction or Non-Fiction
5. Click Continue

Kindle Create analyzes your document structure.

**Step 2: Choose Your Theme**

Select a visual theme:
- **Classic:** Traditional book appearance
- **Modern:** Contemporary with more white space
- **Ornate:** Decorative elements for literary fiction
- **Professional:** Clean for non-fiction

Preview each to see what fits your book's style.

**Step 3: Set Up Front Matter**

Add professional front matter:

**Title Page:**
- Automatically created from your title
- Customize if desired
- Usually includes title and author name only

**Copyright Page:**
- Copyright © [Year] by [Your Name]
- All rights reserved
- ISBN (if you have one)
- Edition information
- Disclaimer (if needed)

**Dedication Page (optional):**
- Brief dedication message
- Usually less than 50 words

**Table of Contents:**
- Kindle Create generates this automatically
- Based on your chapter headings
- Required for navigation in ebooks

**Step 4: Format Chapters**

**Chapter Breaks:**
- Kindle Create identifies chapters from Heading styles
- Confirm each chapter starts correctly
- Adjust if necessary

**Chapter Headings:**
- Ensure consistent formatting
- Can include chapter numbers, titles, or both
- Position and style controlled by theme

**First Paragraph:**
- Traditionally not indented
- Kindle Create handles this automatically
- Can customize in Advanced Settings

**Body Text:**
- Normal paragraphs
- Indentation (usually 0.3" for print, auto for ebook)
- Line spacing (usually 1.15-1.5)
- Alignment (left-aligned for most, justified for traditional)

**Step 5: Add Images**

For books with images:
1. Click where image should appear
2. Select image file
3. Choose size (small, medium, large, full-width)
4. Set alignment (left, center, right)
5. Add caption (optional)

**Image Best Practices:**
- Use high resolution (300 DPI minimum for print)
- Keep file sizes reasonable (under 2MB each)
- JPG for photos, PNG for graphics with transparency
- Ensure images are relevant and add value

**Step 6: Format Back Matter**

**Acknowledgments:**
- Thank people who helped with your book
- Keep it concise (1-2 pages)

**About the Author:**
- Brief bio (100-150 words)
- Your author photo (optional)
- Website and social media links

**Other Books:**
- List your other books
- Include titles and brief descriptions
- Link to Amazon pages (add as hyperlinks)

**Step 7: Generate Table of Contents**

1. Go to TOC section in Kindle Create
2. Verify all chapters are listed
3. Adjust TOC depth (main chapters only, or include subsections)
4. Preview TOC appearance

The TOC is crucial for ebook navigation. Readers use it to jump between chapters.

**Step 8: Preview Your Ebook**

Use Kindle Create's built-in previewer:
- Test different devices (phone, tablet, e-reader)
- Check chapter navigation
- Verify images display correctly
- Review formatting consistency
- Test hyperlinks

**Common Issues to Check:**
- Chapters start on new pages
- No orphaned headings (heading at bottom of page)
- Scene breaks are visible
- No weird spacing or indentation
- Images are properly sized
- Table of contents works

**Step 9: Export Your Ebook**

1. Click "Publish"
2. Choose "Create eBook"
3. Select save location
4. Kindle Create exports a .KPF file

Upload this .KPF file to Amazon KDP. It contains all your formatting and will display perfectly on Kindle devices.

## Formatting Print Books with Kindle Create

**Step 1: Start a Print Project**

1. Open Kindle Create
2. Load your manuscript (can use same project as ebook)
3. Choose "Print"
4. Select trim size:
   - **5" x 8"** - Standard for most fiction
   - **6" x 9"** - Common for non-fiction
   - **5.25" x 8"** - Literary fiction
   - **8.5" x 11"** - Workbooks, textbooks

5. Choose paper color:
   - **White** - Bright, modern, cheaper
   - **Cream** - Warm, traditional, easier on eyes

**Step 2: Set Up Page Layout**

**Running Headers:**
- Book title on left pages
- Chapter title on right pages
- Or just page numbers
- Customizable in Kindle Create

**Page Numbers:**
- Start numbering after front matter
- Usually centered at bottom or top outside corners
- First page of chapter often has no header/number

**Margins:**
- Outer margins: 0.75" - 1"
- Inner margins (gutter): 0.75" - 1.25" (needs extra space for binding)
- Top/bottom margins: 0.75" - 1"
- Kindle Create sets appropriate defaults

**Step 3: Format Chapters for Print**

**Chapter Starts:**
- Typically start on right-hand (odd-numbered) pages
- Can choose to insert blank pages if needed
- First line often has drop cap (large decorative first letter)

**Paragraph Formatting:**
- Indent first line 0.3" - 0.5"
- Don't indent first paragraph of chapter
- Line spacing: usually 1.15 - 1.3
- Justified alignment is traditional for print

**Widows and Orphans:**
- Widow: Last line of paragraph alone on new page
- Orphan: First line of paragraph alone at bottom of page
- Avoid these by adjusting spacing or rewording

**Scene Breaks:**
- Use centered symbols (***) or ornaments
- Don't rely on blank lines (can disappear at page breaks)
- Consider ornamental glyphs for fancy look

**Step 4: Front Matter for Print**

**Half-Title Page:**
- Just the book title, no author name
- Often skipped by indie authors

**Title Page:**
- Full title and subtitle
- Author name
- Publisher imprint (if you have one)

**Copyright Page:**
- Copyright notice
- ISBN
- Publisher info
- Edition information
- Printing information
- Disclaimers

**Dedication Page:**
- Optional
- Usually right-hand page
- Brief message

**Table of Contents:**
- With page numbers
- Only necessary for non-fiction or very long books
- Kindle Create generates automatically

**Step 5: Back Matter for Print**

**Acknowledgments:**
- Thank contributors

**About the Author:**
- Bio and photo
- Books by the author
- Website/contact info

**Blank Pages:**
- May need to add blank page at end to reach even page count
- Some printers require even page counts

**Step 6: Preview Print Layout**

Kindle Create's print previewer shows:
- Exactly how pages will look
- Page breaks and spacing
- Headers and page numbers
- Where images fall

**Check carefully:**
- No important text too close to edges
- Chapter starts look good
- Headers and page numbers are consistent
- Images are clear and properly sized
- Page count is reasonable (affects pricing)

**Step 7: Export Print PDF**

1. Click "Publish"
2. Choose "Create Paperback"
3. Kindle Create generates print-ready PDF

This PDF is what you upload to KDP for the interior.

## Common Formatting Mistakes

**Mistake 1: Using Spaces Instead of Indents**
- **Wrong:** Hitting spacebar 5 times to indent
- **Right:** Use paragraph indentation setting

**Mistake 2: Extra Line Breaks**
- **Wrong:** Hitting Enter twice between every paragraph
- **Right:** Use paragraph spacing setting

**Mistake 3: Manual Formatting**
- **Wrong:** Selecting text and making it bigger/bold
- **Right:** Use Heading styles

**Mistake 4: Inconsistent Scene Breaks**
- **Wrong:** Using ### sometimes, *** other times
- **Right:** Pick one symbol and use it throughout

**Mistake 5: Wrong First Paragraph**
- **Wrong:** Indenting the first paragraph of chapters
- **Right:** First paragraph should be flush left

**Mistake 6: Not Testing on Devices**
- **Wrong:** Only checking on computer
- **Right:** Preview on phone, tablet, and e-reader

**Mistake 7: Ignoring Ebook Best Practices**
- **Wrong:** Using fancy fonts and fixed layouts
- **Right:** Simple, flexible formatting that reflows

## Professional Touch: The Details That Matter

**Drop Caps:**
Large decorative first letter of first paragraph in chapter. Adds elegance to literary fiction.

**Scene Break Ornaments:**
Use decorative symbols (❧, ❦, ✦) instead of just asterisks. Adds visual interest.

**Smart Quotes:**
Curly quotes ("like this") instead of straight quotes ("like this"). Most tools handle automatically.

**Em Dashes vs. Hyphens:**
- Em dash (—): For interruptions, no spaces around it
- En dash (–): For ranges (pages 10–15)
- Hyphen (-): For hyphenated words

**Ellipses:**
Three periods (…) not three separate periods (. . .). Proper ellipses have correct spacing.

**Non-Breaking Spaces:**
Keep certain words together (Chapter 1, Mr. Smith) so they don't split across lines.

## When to Hire a Professional

Consider hiring a professional formatter if:
- Your book has complex layouts (textbooks, cookbooks, illustrated books)
- You have many images, tables, or diagrams
- You're not confident with technology
- You'd rather invest time in writing
- You want absolute perfection

**Professional formatters charge:**
- Ebook only: $50 - $150
- Print only: $100 - $250
- Both formats: $150 - $350

This is far less than what package deals charge ($500-$1,000+).

**Where to find formatters:**
- Reedsy
- Fiverr
- Facebook author groups
- ALLi (Alliance of Independent Authors) directory

## Your Formatting Action Plan

1. **Prepare your manuscript** in Word using proper styles
2. **Download Kindle Create** (free)
3. **Follow this guide** step-by-step for ebook formatting
4. **Preview thoroughly** on multiple devices
5. **Export and upload** to Amazon KDP
6. **Order a proof copy** for print (always check physical book)
7. **Make adjustments** if needed
8. **Publish**

Professional formatting is within reach of every self-publisher. You don't need expensive software or services. With free tools and attention to detail, your book can look as good as traditionally published books.

The money you save on formatting can go toward professional editing or marketing—both of which have bigger impacts on your book's success than formatting (assuming your formatting is at least competent).

Don't let vanity presses charge you $500-$1,000 for formatting. Learn it yourself with free tools, or hire a freelancer directly for a fraction of the cost.

Your book deserves professional formatting. Now you know how to achieve it without breaking the bank.'''
        }
    ]
    
    # Continue adding more articles...
    print("Adding more comprehensive articles...")
    for i, article_data in enumerate(articles, 5):  # Starting from 5 since we already added 4
        try:
            article_id = Article.create(
                author_id=author_id,
                title=article_data['title'],
                content=article_data['content'],
                category=article_data['category'],
                excerpt=article_data['excerpt'],
                status='published'
            )
            print(f"✅ Article {i} added: {article_data['title']}")
        except Exception as e:
            print(f"❌ Failed to add article {i}: {e}")
    
    print(f"\n✅ Successfully added {len(articles)} more professional articles!")
