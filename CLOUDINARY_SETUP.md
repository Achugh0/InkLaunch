# Cloudinary Setup Guide (FREE S3 Alternative)

## Why Cloudinary?

- ✅ **25 GB free storage** + 25 GB bandwidth/month
- ✅ Built specifically for images (automatic optimization)
- ✅ Free CDN for fast worldwide delivery
- ✅ No AWS complexity
- ✅ Auto image resizing, format conversion
- ✅ Perfect for book covers and profile images

---

## Step 1: Create Free Cloudinary Account

1. Go to [cloudinary.com](https://cloudinary.com)
2. Click "Sign Up" → Choose free plan
3. Verify your email
4. Access your dashboard

---

## Step 2: Get Your Credentials

In Cloudinary Dashboard:
1. Go to Dashboard (home page)
2. You'll see:
   - **Cloud Name**: `dxxxxxx`
   - **API Key**: `123456789012345`
   - **API Secret**: `xxxxxxxxxxxx` (click "👁️" to reveal)

---

## Step 3: Install Python Package

```bash
pip install cloudinary
```

Add to requirements.txt:
```
cloudinary==1.36.0
```

---

## Step 4: Set Environment Variables

**Local Development:**
```bash
export CLOUDINARY_CLOUD_NAME='your_cloud_name'
export CLOUDINARY_API_KEY='your_api_key'
export CLOUDINARY_API_SECRET='your_api_secret'
```

**Render Dashboard:**
1. Go to your service → Environment
2. Add:
   ```
   CLOUDINARY_CLOUD_NAME = your_cloud_name
   CLOUDINARY_API_KEY = your_api_key
   CLOUDINARY_API_SECRET = your_api_secret
   ```

---

## Step 5: Upload Your Book Covers

```bash
cd /workspaces/InkLaunch
python upload_to_cloudinary.py
```

This will:
- Upload both book cover images to Cloudinary
- Update your production database with Cloudinary URLs
- Verify images are accessible

---

## Step 6: Update Your App

The app will automatically use Cloudinary when credentials are set.

In `config.py`, the service checks for Cloudinary first, falls back to S3.

---

## Usage Limits (Free Tier)

- Storage: 25 GB
- Bandwidth: 25 GB/month
- Transformations: 25 credits/month
- Perfect for small to medium projects!

---

## Cost Comparison

| Service | Free Tier | After Free |
|---------|-----------|------------|
| **Cloudinary** | 25GB storage, 25GB bandwidth | $0.12/GB storage |
| **AWS S3** | 5GB for 12 months | $0.023/GB storage |
| **ImgBB** | Unlimited | Free forever |
| **Imgur** | Unlimited | Free with ads |

---

## Advantages Over S3

✅ No bucket policies to configure  
✅ No IAM user setup  
✅ Built-in image optimization  
✅ Automatic CDN  
✅ Simpler API  
✅ Better free tier  

---

## Next Steps

1. Create Cloudinary account
2. Get credentials
3. Run: `python upload_to_cloudinary.py`
4. Add environment variables to Render
5. Done! Images persist across deployments
