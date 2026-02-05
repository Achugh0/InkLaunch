# Using Image URLs Without S3

If you prefer not to set up AWS S3, you can use external image URLs for book covers. This guide shows you how.

## How It Works

When creating or editing a book, you'll see two tabs:
- **Upload File**: Traditional file upload (requires S3 in production)
- **Use URL**: Paste a direct link to your image (works anywhere!)

## Free Image Hosting Options

### 1. **Imgur** (Recommended)
- **Website**: https://imgur.com
- **Free**: Yes
- **Sign-up**: Optional (but recommended)
- **Direct Links**: Yes
- **How to use**:
  1. Go to Imgur.com
  2. Click "New Post"
  3. Upload your book cover
  4. Right-click the image and select "Copy Image Address"
  5. Paste into InkLaunch's "Use URL" field

**Pros**: Fast, reliable, no account needed, no bandwidth limits
**Cons**: Images may be visible publicly on Imgur

### 2. **Dropbox**
- **Website**: https://dropbox.com
- **Free**: 2GB storage
- **Sign-up**: Required
- **How to use**:
  1. Upload image to Dropbox
  2. Click "Share" → "Create Link"
  3. Copy the link and change `?dl=0` to `?raw=1` at the end
  4. Paste into InkLaunch

**Example**: 
- Original: `https://www.dropbox.com/s/abc123/cover.jpg?dl=0`
- Use: `https://www.dropbox.com/s/abc123/cover.jpg?raw=1`

**Pros**: Professional, secure, good for multiple files
**Cons**: Requires account, 2GB limit on free plan

### 3. **Google Drive**
- **Website**: https://drive.google.com
- **Free**: 15GB storage
- **Sign-up**: Required (Google account)
- **How to use**:
  1. Upload image to Google Drive
  2. Right-click → "Get link" → Set to "Anyone with the link"
  3. Copy the file ID from the URL
  4. Use this format: `https://drive.google.com/uc?export=view&id=FILE_ID`

**Example**:
- Original link: `https://drive.google.com/file/d/1ABC123XYZ/view?usp=sharing`
- File ID: `1ABC123XYZ`
- Use: `https://drive.google.com/uc?export=view&id=1ABC123XYZ`

**Pros**: Generous storage, integrated with Google account
**Cons**: URL conversion needed, somewhat complex

### 4. **GitHub** (For Tech-Savvy Users)
- **Website**: https://github.com
- **Free**: Unlimited for public repos
- **Sign-up**: Required
- **How to use**:
  1. Create a public repository
  2. Upload image to the repo
  3. View the image in GitHub
  4. Right-click and "Copy Image Address"
  5. Use the raw.githubusercontent.com URL

**Pros**: Version control, unlimited storage for public repos
**Cons**: Requires GitHub knowledge, images must be public

### 5. **ImageBB**
- **Website**: https://imgbb.com
- **Free**: Yes
- **Sign-up**: Optional
- **How to use**:
  1. Go to ImageBB
  2. Click "Start Uploading"
  3. Upload your image
  4. Copy the "Direct Link"
  5. Paste into InkLaunch

**Pros**: Simple, no account needed, made for image hosting
**Cons**: Images may be deleted after inactivity

## Using Your Own Website

If you have your own website with hosting:

1. Upload the image to your website's server (via FTP, cPanel, etc.)
2. Note the full URL (e.g., `https://yourwebsite.com/images/book-cover.jpg`)
3. Paste into InkLaunch

**Pros**: Full control, professional domain
**Cons**: Requires your own hosting

## Best Practices

### Image Requirements
- **Format**: JPG, PNG, or GIF
- **Size**: Under 5MB for fast loading
- **Dimensions**: At least 1600x2400 pixels for best quality
- **Aspect Ratio**: 2:3 (typical book cover ratio)

### URL Tips
1. **Use direct image links**: The URL should end in `.jpg`, `.png`, or `.gif`
2. **Test the URL**: Paste it in a browser's address bar - you should see ONLY the image
3. **Use HTTPS**: Secure URLs (https://) are preferred
4. **Avoid temporary links**: Some services create temporary links that expire
5. **Keep it public**: The image must be publicly accessible

### Common URL Issues

**Problem**: Image doesn't appear
- **Check**: Is the URL a direct link to the image file?
- **Solution**: Make sure the URL ends with an image extension

**Problem**: "This content is no longer available"
- **Check**: Has the image hosting service deleted it?
- **Solution**: Use a reliable service like Imgur or your own hosting

**Problem**: Slow loading
- **Check**: Is the image file too large?
- **Solution**: Compress the image or resize it before uploading

## Comparison Table

| Service | Free Storage | Account Required | Reliability | Ease of Use |
|---------|-------------|------------------|-------------|-------------|
| **Imgur** | Unlimited | No (optional) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Dropbox** | 2GB | Yes | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Google Drive** | 15GB | Yes | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **GitHub** | Unlimited* | Yes | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **ImageBB** | Unlimited | No (optional) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Own Website** | Varies | N/A | Varies | ⭐⭐⭐ |

\* For public repositories

## Recommended Workflow

For most users, we recommend:

1. **Use Imgur** for quick and easy hosting
2. **Resize your image** to 1600x2400 pixels before uploading
3. **Compress** the image to under 1MB using tools like TinyPNG
4. **Upload to Imgur** (no account needed)
5. **Copy the direct image link**
6. **Paste into InkLaunch** using the "Use URL" tab

## Example: Step-by-Step with Imgur

1. Go to https://imgur.com
2. Click "New Post" (top right)
3. Drag and drop your book cover, or click "Browse" to select it
4. Wait for upload to complete
5. Once uploaded, right-click the image
6. Select "Copy Image Address" (or "Copy Image Location")
7. Go back to InkLaunch's book creation/edit page
8. Click the "Use URL" tab
9. Paste the URL (should look like: `https://i.imgur.com/ABC123.jpg`)
10. Continue filling out the book form
11. Submit!

## Still Want S3?

If you need S3 for other features (profile images, manuscripts, etc.), see the [S3 Setup Guide](S3_SETUP_GUIDE.md).

## Hybrid Approach

You can mix both methods:
- Use **URLs** for book covers (easy, no S3 needed)
- Set up **S3** for user-uploaded profile pictures and manuscripts

This gives you flexibility while minimizing infrastructure complexity.

---

**Questions?** Open an issue on GitHub or check the main [README](README.md) for more help.
