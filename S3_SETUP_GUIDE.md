# AWS S3 Setup Guide for InkLaunch

## Why S3 is Required for Production

Render and similar platforms use **ephemeral file systems**, meaning:
- Uploaded files are deleted when instances restart
- Files aren't shared across multiple instances
- Images uploaded by users will disappear

**Solution**: Store all user-uploaded images (book covers, profile photos, banners) in AWS S3.

## Step 1: Create an S3 Bucket

1. Log in to [AWS Console](https://console.aws.amazon.com/)
2. Navigate to S3 service
3. Click "Create bucket"
4. Configure:
   - **Bucket name**: `inklaunch-book-covers` (or your preferred name)
   - **Region**: `us-east-1` (or your preferred region)
   - **Block Public Access**: Uncheck "Block all public access"
     - ⚠️ We need public read access for book covers
     - Check the acknowledgment box
   - Leave other settings as default
5. Click "Create bucket"

## Step 2: Configure Bucket Policy

1. Go to your bucket → Permissions tab
2. Scroll to "Bucket policy"
3. Click "Edit" and add this policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::inklaunch-book-covers/*"
        }
    ]
}
```

**Note**: Replace `inklaunch-book-covers` with your actual bucket name.

4. Save changes

## Step 3: Configure CORS (Optional but Recommended)

If you plan to upload files directly from the browser:

1. Go to your bucket → Permissions tab
2. Scroll to "Cross-origin resource sharing (CORS)"
3. Click "Edit" and add:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": []
    }
]
```

## Step 4: Create IAM User

1. Navigate to IAM service in AWS Console
2. Click "Users" → "Add users"
3. User details:
   - **User name**: `inklaunch-s3-user`
   - **Access type**: Programmatic access
4. Click "Next: Permissions"
5. Click "Attach existing policies directly"
6. Search and select: `AmazonS3FullAccess`
   - Or create a custom policy with only required permissions (see below)
7. Click through to "Create user"
8. **IMPORTANT**: Save the Access Key ID and Secret Access Key
   - You won't be able to see the secret again!

### Custom Policy (More Secure - Recommended)

Instead of full S3 access, create a custom policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:GetObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::inklaunch-book-covers/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": "arn:aws:s3:::inklaunch-book-covers"
        }
    ]
}
```

## Step 5: Configure Render Environment Variables

In your Render dashboard:

1. Go to your web service
2. Navigate to "Environment" tab
3. Add these variables:

```bash
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_S3_BUCKET_NAME=inklaunch-book-covers
AWS_REGION=us-east-1
```

Replace with your actual values.

4. Click "Save Changes"
5. Render will automatically redeploy with the new environment variables

## Step 6: Verify Setup

After deployment:

1. Try uploading a book with a cover image
2. Check your S3 bucket - you should see the file under `book-covers/`
3. The image should be visible on the website
4. The URL should look like: `https://inklaunch-book-covers.s3.us-east-1.amazonaws.com/book-covers/xxx.jpg`

## Troubleshooting

### Images still not appearing

1. Check Render logs for S3 errors:
   ```
   Dashboard → Logs → Look for "Failed to upload" or "S3" errors
   ```

2. Verify environment variables are set correctly in Render

3. Test S3 connection:
   - Go to your app's shell in Render
   - Run: `python -c "from app.services.s3_service import s3_service; print(s3_service.is_s3_configured())"`
   - Should return `True`

### Permission errors

- Ensure IAM user has correct permissions
- Verify bucket policy allows public read
- Check AWS credentials are correct

### Files uploading but not visible

- Check bucket policy (Step 2)
- Ensure files have public-read ACL
- Try accessing the S3 URL directly in browser

## Cost Estimates

AWS S3 Free Tier (First 12 months):
- **Storage**: 5 GB free
- **Requests**: 20,000 GET requests, 2,000 PUT requests per month

After free tier (approximate):
- **Storage**: $0.023 per GB/month
- **Requests**: $0.005 per 1,000 PUT requests, $0.0004 per 1,000 GET requests

**Example**: For a small app with 1,000 users and 5,000 book covers:
- Storage: ~2 GB = $0.05/month
- Requests: ~10,000/month = $0.05/month
- **Total**: ~$0.10/month

## Local Development

The app will automatically fall back to local storage if S3 is not configured. This allows you to develop locally without needing S3.

To test S3 in development, add the AWS variables to your `.env` file:

```bash
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_S3_BUCKET_NAME=inklaunch-book-covers
AWS_REGION=us-east-1
```

## Security Best Practices

1. **Never commit AWS credentials** to your repository
2. **Use IAM roles** if running on EC2 (not applicable for Render)
3. **Rotate credentials** periodically
4. **Monitor usage** in AWS CloudWatch to detect unusual activity
5. **Set up billing alerts** in AWS to avoid surprise charges

## Alternative: Cloudflare R2

If you prefer, you can use Cloudflare R2 (S3-compatible, no egress fees):

1. Create R2 bucket
2. Get API credentials
3. Use same environment variables
4. May need to adjust endpoint in `s3_service.py`

---

**Need help?** Check the main [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) or open an issue.
