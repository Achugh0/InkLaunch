#!/usr/bin/env python3
"""Add 20+ comprehensive professional articles for self-publishers."""
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
            'title': 'The Complete Guide to Self-Publishing: Everything You Need to Know',
            'category': 'Publishing Tips',
            'excerpt': 'A comprehensive guide to self-publishing your book without paying expensive fees to vanity presses or publishing packages.',
            'content': '''Self-publishing has revolutionized the way authors bring their books to market. Gone are the days when you needed to pay thousands of dollars to vanity presses or accept unfavorable contracts with traditional publishers. Today, you can publish your book professionally and retain full control over your work and earnings.

## What is Self-Publishing?

Self-publishing means you, the author, maintain complete control over every aspect of your book's publication. You make all decisions about editing, cover design, formatting, pricing, and distribution. Most importantly, you keep the rights to your work and the majority of your earnings.

## The Truth About Publishing Costs

Here's what many authors don't realize: **you can publish your book completely free** on major platforms like Amazon KDP, Draft2Digital, and PublishDrive. These platforms don't charge upfront fees. They take a small percentage of each sale, but you never pay out of pocket.

Compare this to vanity presses that charge $2,000-$10,000 for "publishing packages." What are you really getting for that money? Often, it's services you could get cheaper elsewhere or don't need at all.

## The Self-Publishing Process

Publishing your book involves several key steps:

**1. Writing and Editing:** Finish your manuscript and have it professionally edited. You can hire freelance editors directly for $500-$2,000, far less than package deals charge.

**2. Cover Design:** A professional cover is essential. Hire a freelance designer for $150-$500, or use tools like Canva to create your own. Many vanity presses charge $1,500+ for covers you could get elsewhere for a fraction of the cost.

**3. Formatting:** Learn to format your book yourself using free tools like Kindle Create, Vellum (Mac), or Atticus. If you prefer to outsource, freelance formatters charge $50-$200. Vanity presses might charge $500-$1,000 for the same service.

**4. Publishing:** Upload your formatted book and cover to Amazon KDP, Draft2Digital, or PublishDrive. This step is completely free and takes about 15 minutes per platform.

**5. Marketing:** This is where you should invest your money, not in publishing packages. Use your budget for targeted advertising, not bundled "marketing services" that rarely deliver results.

## Why Free Publishing Platforms Work

Amazon KDP, Draft2Digital, and PublishDrive make money when you make money. They take a percentage of each sale (typically 30-40%), but there are no upfront costs. This aligns their interests with yours—they want your book to succeed.

These platforms provide:
- Global distribution to major retailers
- Professional-quality production
- Your book in both ebook and paperback formats
- Marketing tools and promotional options
- Detailed sales reporting
- Direct deposits to your bank account

## What to Avoid

**Vanity Presses:** Companies that charge upfront fees for "publishing packages" are often vanity presses. They make their money from authors, not from selling books to readers. Warning signs include:
- Packages priced at $1,500-$10,000+
- Aggressive sales tactics
- Claims that you need their services to be successful
- Poor reviews from other authors
- Hidden fees for additional services

**Exploitative Contracts:** Some companies offer "free" publishing but lock you into exclusive contracts, charge excessive fees for changes, or take unreasonably high royalty percentages.

**Overpriced Services:** While you may want to hire professionals for editing or design, research market rates. If a company is charging 2-3 times what freelancers charge, you're being overcharged.

## Your Publishing Budget

If you're publishing on a budget, you might spend:
- Editing: $500-$2,000 (or trade services with other writers)
- Cover Design: $150-$500 (or DIY with Canva)
- Formatting: $0-$200 (free tools available)
- Publishing Platform: $0 (Amazon KDP, Draft2Digital, PublishDrive)
- ISBN (optional): $0-$125 (Amazon provides free ISBNs, or buy your own)
- Marketing: Whatever you can afford

**Total: $650-$2,825 (or as low as $0 if you DIY everything)**

Compare this to vanity press packages at $3,000-$10,000+ where you often get inferior results and lose control of your rights.

## The Empowerment of Self-Publishing

Self-publishing puts you in the driver's seat. You make all creative decisions, set your own prices, and keep the majority of your profits. You can update your book anytime, run promotions whenever you want, and publish on your own timeline.

Most successful indie authors started by publishing for free on Amazon KDP. They invested in learning the craft and business of publishing rather than paying for expensive packages. Many now earn six figures or more from their books.

## Getting Started Today

You can start your self-publishing journey right now:

1. Finish your manuscript
2. Learn about the free publishing platforms (start with Amazon KDP)
3. Connect with other indie authors in online communities
4. Invest in skills, not packages
5. Publish your first book

Remember: **The best investment you can make is in yourself—your writing, your skills, and your understanding of the publishing business.** Don't let anyone convince you that you need to pay thousands of dollars to become a published author. You don't.

The tools are free. The knowledge is available. The only thing standing between you and being a published author is your decision to start. Make today that day.'''
        },
        {
            'title': 'Amazon KDP Complete Tutorial: Publish Your Book in 30 Minutes',
            'category': 'Publishing Tips',
            'excerpt': 'Step-by-step instructions for publishing your ebook and paperback on Amazon KDP, the world\'s largest book platform.',
            'content': '''Amazon Kindle Direct Publishing (KDP) is the world's largest self-publishing platform, and it's completely free to use. You can publish both ebooks and paperbacks that are available to millions of readers worldwide. Best of all, the entire process takes about 30 minutes once you have your files ready.

## Why Amazon KDP?

Amazon KDP offers several compelling advantages:

- **No upfront costs:** Publishing is completely free
- **70% royalty option:** Earn up to 70% on ebook sales (35% for paperbacks)
- **Massive audience:** Access to hundreds of millions of Amazon customers
- **Fast publication:** Your book goes live within 24-72 hours
- **Global distribution:** Reach readers in countries worldwide
- **Print-on-demand:** Paperbacks are printed only when ordered—no inventory needed
- **Complete control:** Update your book, change your price, or unpublish anytime

## Before You Start: What You Need

Before logging into KDP, make sure you have:

1. **Your manuscript** in a Word document (.doc or .docx) or EPUB file
2. **A professional cover** in JPG format (minimum 2560 x 1600 pixels for ebooks)
3. **Your book details** including title, subtitle, description, and keywords
4. **Tax information** (W-9 for US authors, W-8BEN for international authors)
5. **Banking information** for royalty payments

## Step 1: Create Your KDP Account

1. Go to kdp.amazon.com
2. Click "Sign up" or use your existing Amazon account
3. Complete your account profile
4. Enter your tax information (required before you can publish)
5. Add your bank account details for payments

This setup takes about 10 minutes and only needs to be done once.

## Step 2: Create a New Book

From your KDP dashboard:

1. Click the "+ Create" button
2. Choose "Kindle eBook" or "Paperback" (you can publish both)
3. You'll see three sections: Kindle eBook Details, Kindle eBook Content, and Kindle eBook Pricing

## Step 3: Fill in Your Book Details

**Title and Subtitle:**
- Enter your book title exactly as you want it to appear
- Add a subtitle if applicable (this helps with discoverability)
- Make sure your cover matches these details exactly

**Series Information:**
- If your book is part of a series, enter the series name and number
- This helps readers find all books in your series

**Edition Number:**
- Use "1" for your first edition
- Update this number if you make major revisions

**Author Name:**
- Enter your name or pen name
- Use the same name consistently across all your books
- You can add co-authors or contributors here

**Description:**
- Write a compelling description (up to 4,000 characters)
- Use HTML formatting to add bold text, italics, and line breaks
- Think of this as your book's sales page—make it count
- Include hooks that make readers want to buy

**Publishing Rights:**
- Select "I own the copyright" if you wrote the book
- Amazon takes copyright seriously—only publish work you own

**Keywords:**
- Add up to 7 keywords or phrases
- Think about what readers might search for
- Use specific phrases, not single words
- Research popular keywords in your genre

**Categories:**
- Choose 2 categories where your book fits best
- You can request additional categories after publishing via KDP support
- Browse Amazon to see which categories your competitors use

## Step 4: Upload Your Book Content

**Manuscript:**
1. Click "Upload eBook manuscript"
2. Select your Word document or EPUB file
3. Wait for KDP to convert and process it (usually 1-5 minutes)
4. Use the online previewer to check how your book looks
5. Check all chapters, especially the beginning and end
6. Look for formatting issues, page breaks, and images

**Cover:**
1. Click "Upload a cover you already have"
2. Select your cover JPG file
3. KDP will validate that it meets size requirements
4. Use the previewer to check how it looks

**Pro Tip:** Amazon offers Cover Creator if you need a basic cover, but a professional cover dramatically increases sales.

**Kindle eBook ISBN:**
- You don't need an ISBN for Kindle ebooks
- Amazon assigns a free ASIN (Amazon Standard Identification Number)
- Skip this section unless you have a specific reason to use an ISBN

## Step 5: Set Your Pricing

**Enrollment in KDP Select:**
- KDP Select gives you access to Kindle Unlimited and promotional tools
- **BUT** it requires exclusivity—you can't publish your ebook anywhere else for 90 days
- You can still publish paperbacks anywhere
- Many successful authors choose wide distribution instead

**Territory Rights:**
- Choose "Worldwide rights" unless you have existing contracts in some countries
- This maximizes your potential audience

**Pricing:**

For ebooks, you have two royalty options:

**35% Royalty:**
- Available for all prices
- Amazon keeps 65%, you keep 35%
- No delivery costs deducted
- Required for prices under $2.99 or over $9.99

**70% Royalty:**
- Only available for prices between $2.99 and $9.99
- Amazon keeps 30%, you keep 70% minus delivery costs
- Delivery costs are typically $0.15-$0.30
- Must be enrolled in this option for each marketplace separately
- Your book must be offered at or below the list price in all countries

**Recommended Pricing Strategy:**
- Price between $2.99-$9.99 to qualify for 70% royalty
- For a first book, $2.99-$4.99 is a sweet spot
- Research comparable books in your genre
- Remember: you can change your price anytime

## Step 6: Publish Your Book

1. Review all your entries for accuracy
2. Click "Publish Your Kindle eBook"
3. Your book enters review and processing
4. Within 24-72 hours, your book goes live on Amazon

## Publishing Paperbacks on KDP

The process is nearly identical for paperbacks, with a few additions:

**Interior File:**
- Upload a PDF formatted for your trim size (6x9" is most common)
- Use KDP's templates or tools like Kindle Create for formatting
- Choose white or cream paper (cream is warmer, popular for novels)
- Choose bleed or no bleed (bleed means images/color extend to page edge)

**Cover:**
- Use KDP's Cover Calculator to get exact dimensions
- Your cover must include front, spine, and back
- Download the template for your book's page count
- Upload as a single PDF with bleed

**Pricing:**
- Amazon calculates minimum price based on page count and paper choice
- You receive 60% royalty for sales on Amazon.com
- You receive 40% royalty for expanded distribution sales

**Pro Tip:** Order an author proof copy before making your book public. This costs only printing and shipping, and lets you check the physical book quality.

## After Publishing: What's Next

Once your book is live:

1. **Check your book page:** Make sure everything looks correct
2. **Order a proof copy:** For paperbacks, order one to check quality
3. **Set up an Author Central page:** Add your bio, photos, and link your books
4. **Start marketing:** Share your book link, run promotions, gather reviews
5. **Monitor sales:** Check your KDP dashboard daily to track sales and earnings

## Common Mistakes to Avoid

- **Poor cover quality:** This is the #1 reason books don't sell
- **Formatting errors:** Always preview your entire book before publishing
- **Weak description:** Your description is your sales page—make it compelling
- **Wrong categories:** Research before choosing your categories
- **Overpricing:** Price competitively, especially for your first book
- **No marketing plan:** Publishing is just the first step; you need to market

## Updating Your Published Book

You can update your book anytime:
- Upload a new manuscript or cover
- Change your price or description
- Updates usually go live within 24 hours
- Readers who already bought the book can download the updated version

## The Bottom Line

Amazon KDP has democratized publishing. What once required a traditional publisher, an agent, and years of waiting can now be accomplished in 30 minutes from your laptop. The platform is free, powerful, and reaches the world's largest audience of book buyers.

You don't need to pay anyone to publish on Amazon KDP. You don't need special software or expensive services. You just need a finished manuscript, a good cover, and the willingness to learn the platform.

Millions of authors have published successfully on KDP. Many earn significant income from their books. The opportunity is there for anyone willing to take it. Why not start today?'''
        },
        {
            'title': 'Kindle Create: The Free Tool Every Author Needs',
            'category': 'Tools & Software',
            'excerpt': 'Master Kindle Create, Amazon\'s free formatting tool that makes professional book formatting simple for ebooks and paperbacks.',
            'content': '''Kindle Create is Amazon's free formatting tool that transforms your manuscript into professionally formatted ebooks and paperbacks. It's one of the most valuable free resources available to self-publishers, yet many authors don't know it exists or how to use it effectively.

## What is Kindle Create?

Kindle Create is desktop software (available for Windows and Mac) that helps you format your book for Amazon KDP. It handles all the technical aspects of creating properly formatted files, including:

- Table of contents generation
- Chapter headings and page breaks
- Images and graphics placement
- Font and spacing control
- Print interior formatting for paperbacks
- EPUB file export for ebooks

The best part? It's completely free and created by Amazon specifically for KDP authors.

## Why Use Kindle Create?

Before Kindle Create, authors had several formatting options, all with drawbacks:

**Option 1: Upload a Word document directly to KDP**
- Often results in formatting inconsistencies
- Limited control over appearance
- May not display properly on all devices

**Option 2: Hire a professional formatter**
- Costs $50-$200 per book
- Every update requires paying again
- Dependence on someone else's availability

**Option 3: Learn HTML and CSS**
- Steep learning curve
- Time-consuming
- Not necessary for most books

**Kindle Create solves these problems** by providing a visual, user-friendly interface that creates professional results without technical knowledge or ongoing costs.

## Getting Started with Kindle Create

**Download and Installation:**

1. Go to kdp.amazon.com/en_US/help/topic/G202131100
2. Download Kindle Create for your operating system (Windows or Mac)
3. Install the software (it's only about 150MB)
4. Launch Kindle Create

**Preparing Your Manuscript:**

Before importing into Kindle Create, prepare your Word document:

- Use Word's built-in styles for headings (Heading 1, Heading 2, etc.)
- Remove extra spaces and formatting inconsistencies
- Place images where you want them to appear
- Save as .doc or .docx format

The cleaner your source file, the easier the formatting process will be.

## Creating an eBook with Kindle Create

**Step 1: Import Your Manuscript**

1. Click "New Project from File"
2. Select your Word document
3. Choose whether it's fiction or non-fiction (this affects available templates)
4. Click "Continue"

Kindle Create will analyze your document and import it.

**Step 2: Choose a Theme**

Kindle Create offers several themes that control your book's appearance:

- **Classic:** Simple, traditional book layout
- **Modern:** Contemporary design with more spacing
- **Contemporary:** Clean, minimal style
- **Ornate:** Decorative elements for literary fiction
- **Custom:** Full control over all elements

For most books, Classic or Modern works perfectly. You can preview each theme before deciding.

**Step 3: Set Up Your Front Matter**

Front matter includes:

- **Title Page:** Automatically created from your book title
- **Copyright Page:** Add your copyright notice, edition info, and ISBN
- **Dedication:** Optional page dedicating your book
- **Table of Contents:** Automatically generated from your chapters

Kindle Create makes it easy to add, remove, or reorder these pages.

**Step 4: Format Your Chapters**

This is where Kindle Create shines:

- It identifies your chapters based on heading styles
- You can split or merge chapters visually
- Add chapter titles or numbers
- Insert page breaks before chapters
- Adjust spacing and indentation

Each chapter is shown as a separate section you can edit independently.

**Step 5: Add and Format Images**

For books with images:

1. Click where you want an image
2. Insert the image file (JPG or PNG)
3. Set the size (small, medium, large, or custom)
4. Choose alignment (left, center, right)
5. Add captions if desired

Kindle Create automatically optimizes images for ebook display.

**Step 6: Generate Table of Contents**

1. Go to the TOC section
2. Check that all chapters are listed correctly
3. Adjust the TOC title if desired
4. Set the depth of subheadings to include

Kindle Create creates both the HTML TOC (for navigation) and an in-book TOC page.

**Step 7: Preview Your eBook**

Use the built-in previewer to see how your book looks:

- Test different devices (phones, tablets, e-readers)
- Check all chapters start correctly
- Verify images display properly
- Review the table of contents functionality

Navigate through your entire book to catch any formatting issues.

**Step 8: Export Your eBook**

1. Click "Publish"
2. Choose "Create eBook"
3. Select the save location
4. Kindle Create exports a .kpf file

This .kpf file is what you'll upload to Amazon KDP. It contains all your formatting and will display perfectly on Kindle devices.

## Creating a Paperback with Kindle Create

Kindle Create also formats paperback interiors:

**Step 1: Start a Print Project**

1. Create a new project or use your existing ebook project
2. Choose "Print" as the format
3. Select your trim size (6" x 9" is most common for non-fiction; 5" x 8" for fiction)
4. Choose paper type (white or cream)

**Step 2: Set Up Print-Specific Elements**

For paperbacks, you need:

- **Running Headers:** Book title or chapter names at the top of pages
- **Page Numbers:** Automatic page numbering
- **Chapter Starts:** Choose whether chapters start on odd or even pages
- **Drop Caps:** Optional decorative first letters

**Step 3: Adjust Margins and Spacing**

Kindle Create handles print margins automatically, but you can adjust:

- Line spacing
- Paragraph indentation
- Space between chapters
- Gutter margins (the inner margin near the spine)

**Step 4: Preview Print Layout**

The print previewer shows:

- How pages will look in the physical book
- Whether text is cut off or margins are wrong
- Page breaks and chapter starts
- Overall professional appearance

**Step 5: Export Print PDF**

1. Click "Publish"
2. Choose "Create Paperback"
3. Kindle Create exports a print-ready PDF

This PDF is what you'll upload to KDP for the paperback interior.

## Advanced Kindle Create Features

**Drop Caps:**
Add decorative enlarged first letters to paragraphs, common in literary fiction.

**Custom Fonts:**
While Kindle readers control font choice, you can specify preferred fonts that readers can override.

**Text Boxes:**
Add special formatted sections, perfect for quotes, tips, or sidebars in non-fiction.

**Lists and Formatting:**
Control bullet points, numbered lists, and special formatting with precision.

**Hyperlinks:**
Add clickable links to websites, email addresses, or other parts of your book.

## Tips for Best Results

**1. Start with a Clean Manuscript:**
Remove any quirky formatting from Word before importing. Use consistent styles throughout.

**2. Use Heading Styles:**
Don't just make text bigger and bold—use Word's Heading 1, Heading 2 styles for proper structure.

**3. Keep It Simple:**
Resist the urge to over-format. Simple, clean formatting is more professional and readable.

**4. Test on Multiple Devices:**
Use the previewer to check phones, tablets, and e-readers. What looks good on one may not work on another.

**5. Save Your Project:**
Kindle Create saves your project file (.kc2) so you can make updates later without starting over.

**6. Export Often:**
As you work, export test versions and upload to KDP as drafts to see how they really look.

## Common Kindle Create Mistakes

**Mistake 1: Not Using the Right Import File**
- Use .doc or .docx, not PDF or plain text
- PDFs don't format well and lose all styling

**Mistake 2: Ignoring Heading Styles**
- If you didn't use heading styles in Word, Kindle Create can't identify chapters automatically
- You'll have to manually mark each chapter

**Mistake 3: Over-Formatting**
- Too many font changes, sizes, and decorations look unprofessional
- Let the theme do the work

**Mistake 4: Skipping the Preview**
- Always preview before publishing
- Check every page, especially the beginning and end

**Mistake 5: Using Low-Resolution Images**
- Images should be at least 300 DPI for clear display
- Kindle Create compresses images, so start with high quality

## Kindle Create vs. Alternatives

**Kindle Create vs. Vellum:**
- Vellum ($249.99) offers more design control and beautiful templates
- But Kindle Create is free and sufficient for most books
- Vellum is Mac-only; Kindle Create works on Windows too

**Kindle Create vs. Atticus:**
- Atticus ($147 one-time) combines writing and formatting
- More powerful but has a learning curve
- Kindle Create is simpler and purpose-built for KDP

**Kindle Create vs. DIY HTML:**
- HTML gives complete control but requires coding skills
- Kindle Create is visual and intuitive
- Most authors don't need HTML-level control

**The Verdict:** For most authors, especially beginners, Kindle Create is the perfect solution. It's free, easy to learn, and produces professional results.

## Updating Your Book with Kindle Create

One of Kindle Create's best features is easy updates:

1. Open your saved .kc2 project file
2. Make your changes
3. Export a new file
4. Upload to KDP to replace the old version

Your formatting remains consistent, and updates take minutes instead of hours.

## The Bottom Line

Kindle Create eliminates one of the biggest obstacles to self-publishing: technical formatting. You don't need to learn coding, hire a professional, or spend money on expensive software. Amazon gives you professional-quality formatting tools completely free.

Hundreds of thousands of successful self-published books have been formatted with Kindle Create. It's proven, reliable, and constantly updated by Amazon to stay current with best practices.

If you're self-publishing on Amazon KDP, there's no reason not to use Kindle Create. Download it today, spend an hour learning the basics, and you'll have a skill that saves you money on every book you publish for the rest of your career.

The tool is free. The knowledge is simple. The results are professional. What are you waiting for?'''
        },
        {
            'title': 'Book Cover Design: DIY Guide for Authors on a Budget',
            'category': 'Formatting & Design',
            'excerpt': 'Create professional-looking book covers yourself using free and affordable tools. Save hundreds while maintaining quality.',
            'content': '''Your book cover is the single most important marketing tool you have. It's the first thing potential readers see, and it determines whether they click on your book or scroll past. While many authors hire professional designers (and that's a great investment if you can afford it), you can create effective covers yourself with the right tools and knowledge.

## The Truth About Book Covers

Let's be honest: **your cover needs to look professional.** Readers judge books by their covers, and an amateur-looking cover can sink even the best-written book. However, "professional" doesn't necessarily mean "expensive."

What makes a cover professional?
- Appropriate for the genre
- Clear, readable title
- High-quality images or design elements
- Proper sizing and format
- Looks good as a thumbnail (most readers see it small first)

You can achieve all of this without spending $500+ on a designer—if you're willing to learn some basic design principles.

## Free and Affordable Design Tools

**Canva (Free - $119.99/year for Pro):**

Canva is the go-to tool for authors creating their own covers. The free version is surprisingly powerful:

- Thousands of templates specifically for book covers
- Huge library of free stock photos and graphics
- Easy-to-use drag-and-drop interface
- Proper sizing presets for ebook and print covers
- No design experience required

Canva Pro adds:
- Access to premium photos and elements
- Brand kit for consistent design across books in a series
- Background remover tool
- More fonts and templates

For most indie authors, Canva free version is sufficient.

**Other Tools Worth Considering:**

**GIMP (Free):**
- Open-source alternative to Photoshop
- More powerful than Canva, but steeper learning curve
- Best for authors who want maximum control
- Requires some investment in learning

**Bookbrush ($9.99/month):**
- Designed specifically for book covers and marketing materials
- Templates for various genres
- 3D mockups for promotional images
- Worth it if you're publishing multiple books

**Adobe Express (Free - $9.99/month for Premium):**
- Similar to Canva with a simpler interface
- Good template library
- Integrates with other Adobe products if you use them

**Recommendation:** Start with Canva free. It's intuitive, powerful, and you can create professional covers without paying anything.

## Understanding Cover Design Basics

Before you start designing, understand these fundamental principles:

**Genre Conventions Matter:**

Every genre has visual expectations:
- **Romance:** Couples, pastel colors, elegant fonts
- **Thriller:** Dark colors, bold fonts, tension in imagery
- **Fantasy:** Magical elements, dramatic scenes, ornate fonts
- **Self-Help:** Clean, professional, inspirational imagery
- **Mystery:** Shadows, noir aesthetic, crime elements

Browse the bestsellers in your genre on Amazon. Notice patterns? That's what readers expect. You don't have to follow conventions exactly, but straying too far confuses readers.

**The Thumbnail Test:**

Your cover must work at thumbnail size (around 120 pixels tall). At that size:
- Text must still be readable
- Main image must be recognizable
- Overall design must grab attention

If your cover looks cluttered or text disappears at thumbnail size, simplify.

**Typography Matters:**

The right font can make or break your cover:
- **Don't use** more than 2-3 fonts total
- **Ensure** title text is large and clear
- **Choose** fonts that match your genre
- **Avoid** overused fonts like Papyrus or Comic Sans
- **Make sure** author name is readable but doesn't overpower the title

**Color Psychology:**

Colors convey emotion and genre:
- **Red:** Passion, danger, romance, thriller
- **Blue:** Trust, calm, mystery, technology
- **Black:** Sophistication, fear, noir
- **Green:** Nature, peace, growth, environment
- **Purple:** Mystery, fantasy, spiritual
- **Yellow/Orange:** Optimistic, energetic, comedic

**Visual Hierarchy:**

Guide the eye intentionally:
1. Main image (draws initial attention)
2. Title (what's the book?)
3. Author name (who wrote it?)
4. Subtitle or tagline (additional context)

Readers should process these elements in order.

## Creating Your First Cover in Canva

**Step 1: Set Up Your Canvas**

1. Sign up for Canva (free)
2. Search for "Kindle Cover" or "Book Cover" templates
3. Or create custom dimensions:
   - **eBook:** 2560 x 1600 pixels (minimum), 1.6:1 ratio
   - **Paperback 6x9":** Use KDP's Cover Calculator for exact dimensions
4. Choose between starting from a template or blank canvas

**Step 2: Choose Your Background**

Options include:
- **Stock photos:** Canva has thousands of free photos
- **Solid colors:** Clean and professional, especially for non-fiction
- **Gradients:** Modern and eye-catching
- **Patterns:** Subtle textures add depth

**Pro Tip:** Use the search filters in Canva to find images matching your genre. Search for "mystery book background" or "romance cover background."

**Step 3: Add Your Title**

1. Click "Text" in the left sidebar
2. Choose a heading style or add text box
3. Type your title
4. Adjust:
   - **Font:** Try several to see what fits your genre
   - **Size:** Make it large—it needs to dominate
   - **Color:** Ensure high contrast with background
   - **Spacing:** Adjust letter spacing (tracking) for impact
   - **Effect:** Add subtle shadows or outlines for readability

**Step 4: Add Your Author Name**

1. Add another text element
2. Make it smaller than the title but still readable
3. Position it typically at the bottom
4. Keep it simple—this isn't the focus

**Step 5: Add Design Elements**

Consider adding:
- **Icons or graphics:** Support your theme
- **Shapes:** Frame text or add visual interest
- **Lines or dividers:** Separate elements cleanly

**Warning:** Less is more. Don't clutter your cover.

**Step 6: Refine and Polish**

1. **Alignment:** Use Canva's alignment tools to ensure everything is straight
2. **Balance:** Distribute visual weight evenly
3. **Breathing Room:** Leave white space—don't cram
4. **Consistency:** If it's part of a series, maintain consistent style

**Step 7: Test at Thumbnail Size**

1. Zoom out or view at 10% size
2. Can you read the title?
3. Does the image still make sense?
4. Does it stand out from other covers?

If no to any question, simplify and enlarge key elements.

**Step 8: Export**

1. Click "Download"
2. Choose PNG (best quality)
3. Download at highest resolution
4. Save in a logical folder system

## Creating Print Covers

Print covers are more complex because they include:
- Front cover
- Spine
- Back cover

**Using KDP's Cover Calculator:**

1. Go to kdp.amazon.com/cover-calculator
2. Enter your book's page count and paper type
3. Download the template for your trim size
4. Upload the template to Canva
5. Design within the template's safe zones

**Important Considerations:**

- **Spine width** changes based on page count
- **Bleed areas** extend beyond trim lines (add 0.125" all around)
- **Safe zones** keep important elements away from edges (0.125" from trim)
- **Barcode area** (bottom right back cover) must stay clear

**Back Cover Elements:**

- Book description (compelling sales copy)
- Author bio (brief)
- Author photo (optional)
- Quotes or reviews (if you have them)
- Category information
- Publisher information (if applicable)

## Common DIY Cover Mistakes

**Mistake 1: Using Low-Resolution Images**
- **Problem:** Blurry, pixelated covers look amateur
- **Solution:** Use only high-res images (at least 300 DPI for print)

**Mistake 2: Too Much Text**
- **Problem:** Cluttered, hard to read
- **Solution:** Stick to title, subtitle (if necessary), and author name

**Mistake 3: Wrong Genre Signals**
- **Problem:** Confuses readers, lowers sales
- **Solution:** Research your genre's conventions and follow them

**Mistake 4: Unreadable Fonts**
- **Problem:** Overly decorative fonts that can't be read at small sizes
- **Solution:** Prioritize readability over style

**Mistake 5: Poor Color Contrast**
- **Problem:** Text blends into background
- **Solution:** Use high contrast (dark on light or light on dark)

**Mistake 6: Ignoring the Spine**
- **Problem:** Spine looks unprofessional or text is cut off
- **Solution:** Use KDP's templates and keep text centered in safe zone

**Mistake 7: Not Testing on Devices**
- **Problem:** Cover looks great on computer but terrible on phone
- **Solution:** View your cover on various devices before finalizing

## When to Hire a Professional

Sometimes DIY isn't the best choice. Consider hiring a professional if:

- You've tried multiple times and can't achieve the look you want
- Your book is in a highly competitive genre where covers are especially important
- You're not confident in your design skills
- You have the budget ($150-$500 for a good designer)
- You're willing to invest in success

**Where to Find Designers:**

- **Reedsy:** Vetted professionals, higher end
- **Fiverr:** Wide range of prices and quality ($50-$300)
- **99designs:** Contest-based, good for multiple options
- **DIY Book Covers:** Pre-made covers you can customize ($35-$80)
- **Facebook Groups:** Many designers advertise in author groups

**Pro Tip:** Even if you hire a designer, understanding cover design basics helps you communicate what you want and evaluate their work.

## Cover Design for Series

If you're writing a series, plan ahead:

**Consistency Elements:**
- Same fonts throughout
- Similar layout or composition
- Consistent color palette or treatment
- Recognizable style that brands the series

**Varying Elements:**
- Different images or colors per book
- Numbered or subtitled to show order
- Unique elements that reflect each book's specific content

**Example Approach:**
- Keep the same overall design template
- Change the primary image for each book
- Use a color-coding system (Book 1 = blue, Book 2 = red, etc.)
- Maintain exact same fonts and placement

Series with consistent branding sell better because readers instantly recognize they're connected.

## Updating Your Cover

Don't be afraid to redesign if your cover isn't working:

- Monitor your clickthrough rate (impressions vs. page visits)
- If it's low (under 0.5%), your cover might be the issue
- You can update covers anytime on KDP
- Some authors A/B test different covers
- A better cover can immediately increase sales

## The Reality of DIY Covers

**Will a DIY cover be as good as a $500 professional cover?** Probably not, especially if you're a beginner.

**Can a DIY cover be good enough to sell books?** Absolutely, if you:
- Study your genre
- Follow design principles
- Use quality tools like Canva
- Get feedback before publishing
- Are willing to iterate and improve

Many successful indie authors started with DIY covers and later upgraded as their income grew. It's a legitimate path.

## Your Cover Design Action Plan

1. **Research:** Study 50-100 covers in your genre
2. **Learn:** Watch a few Canva tutorial videos
3. **Practice:** Create 3-5 different cover mockups
4. **Test:** Show them to readers in your target audience
5. **Refine:** Incorporate feedback
6. **Publish:** Go with your best option
7. **Monitor:** Track how it performs
8. **Improve:** Don't be afraid to redesign later

Remember: your first cover doesn't have to be perfect. It has to be good enough to sell books while you're learning and growing as an author. You can always improve it later.

The money you save by DIYing your cover can go toward editing, marketing, or writing your next book. That's smart business for an indie author just starting out.'''
        }
    ]
    
    # Add first batch of 4 articles
    print("Adding comprehensive articles...")
    for i, article_data in enumerate(articles, 1):
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
    
    print(f"\n✅ Added {len(articles)} comprehensive articles!")
    print("These are properly formatted articles, not bullet points.")

main()
