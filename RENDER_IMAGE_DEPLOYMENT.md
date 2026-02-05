# Deploy Actual Book Cover Images to Render

## The Problem
Your actual book cover images are currently stored in the local `/uploads/` folder. Render uses an **ephemeral file system**, meaning these files will be deleted when:
- The service restarts
- A new deployment occurs
- The instance scales

## The Solution
Upload the images to AWS S3 (permanent storage) and update your production database to reference the S3 URLs.

---

## Step 1: Set Up AWS S3

If you haven't already, follow the complete guide in [S3_SETUP_GUIDE.md](S3_SETUP_GUIDE.md).

**Quick checklist:**
- [ ] Create an S3 bucket (e.g., `inklaunch-book-covers`)
- [ ] Set bucket to allow public read access
- [ ] Configure bucket policy for public GetObject
- [ ] Create IAM user with S3 access
- [ ] Get Access Key ID and Secret Access Key

---

## Step 2: Set Environment Variables

### In Your Local Terminal:

```bash
export AWS_ACCESS_KEY_ID='your_access_key_here'
export AWS_SECRET_ACCESS_KEY='your_secret_key_here'
export AWS_S3_BUCKET_NAME='inklaunch-book-covers'
export AWS_REGION='us-east-1'
export MONGODB_URI='your_mongodb_atlas_connection_string'
```

**Get your MongoDB Atlas URI from:**
- MongoDB Atlas Dashboard → Connect → Drivers
- Format: `mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/inklaunch`

---

## Step 3: Run the Deployment Script

```bash
cd /workspaces/InkLaunch
python deploy_images_to_s3.py
```

**What this does:**
1. ✅ Uploads your actual book cover images to S3
   - `The Weight of Wings` → `book-covers/the-weight-of-wings.jpg`
   - `The Day We Die` → `book-covers/the-day-we-die.png`
2. ✅ Updates your **production** MongoDB Atlas database with S3 URLs
3. ✅ Verifies images are publicly accessible

---

## Step 4: Configure Render Environment Variables

1. Go to your Render dashboard
2. Select your InkLaunch service
3. Go to **Environment** tab
4. Add these variables:

```
AWS_ACCESS_KEY_ID = your_access_key
AWS_SECRET_ACCESS_KEY = your_secret_key
AWS_S3_BUCKET_NAME = inklaunch-book-covers
AWS_REGION = us-east-1
```

**Security Note:** Render encrypts environment variables at rest.

---

## Step 5: Push to GitHub (Optional)

If you made any code changes, push them:

```bash
git add .
git commit -m "Configure S3 image storage for production"
git push origin main
```

Render will automatically deploy.

---

## Step 6: Verify on Render

1. Wait for deployment to complete
2. Visit your Render URL: `https://your-app.onrender.com/books`
3. Confirm the actual book covers are displaying

---

## What You Should See

After deployment, your books page should show:
- ✅ "The Weight of Wings" - Professional cover with person silhouette and wings
- ✅ "The Day We Die" - Professional cover with person at window overlooking city

Both images will load from S3 (not local uploads).

---

## Troubleshooting

### Images not showing?

**Check 1: S3 Upload**
```bash
# Test S3 access directly
curl -I https://your-bucket.s3.us-east-1.amazonaws.com/book-covers/the-weight-of-wings.jpg
# Should return: HTTP/2 200
```

**Check 2: Database URLs**
```python
from pymongo import MongoClient
client = MongoClient('your_mongodb_uri')
db = client.inklaunch
books = list(db.books.find({}))
for book in books:
    print(f"{book['title']}: {book['cover_image_url']}")
```

Should show S3 URLs starting with `https://your-bucket.s3...`

**Check 3: Bucket Policy**
Ensure your S3 bucket has public read access:
- Bucket → Permissions → Bucket Policy
- Should allow `s3:GetObject` for `Principal: *`

**Check 4: Render Environment Variables**
- Render Dashboard → Environment
- Verify all AWS_* variables are set correctly

---

## For Future Book Uploads

Once S3 is configured in Render, any new books uploaded through the app will automatically:
1. Upload images directly to S3
2. Store S3 URLs in the database
3. Display from S3 (no ephemeral storage issues)

Your existing S3 service (`app/services/s3_service.py`) already handles this!

---

## Cost Estimate

AWS S3 costs are minimal for a book platform:
- **Storage**: ~$0.023 per GB/month
- **Requests**: First 1,000 free, then $0.005 per 1,000
- **Data transfer**: First 1 GB free/month

**Example:** 100 books with 1 MB covers = 100 MB = **< $0.01/month**

---

## Summary

✅ Images stored permanently in S3  
✅ Database references S3 URLs  
✅ Works across Render restarts/deployments  
✅ Fast, reliable image delivery  
✅ Professional production setup  

Your actual book covers will now display on Render! 🚀
