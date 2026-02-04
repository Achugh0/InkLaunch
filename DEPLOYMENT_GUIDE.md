# InkLaunch Deployment Guide

## ✅ Fixes Applied

The following deployment configurations have been added to fix the Railway build:

1. **nixpacks.toml** - System dependencies configuration
2. **Procfile** - Specifies how to run the app with Gunicorn
3. **runtime.txt** - Python version specification
4. **railway.json** - Railway-specific configuration
5. **.railwayignore** - Optimizes build by excluding unnecessary files
6. **requirements.txt** - Added Gunicorn, temporarily disabled Pillow

## 🚀 Railway Deployment Steps

### 1. Railway should auto-detect the changes
   - The new commit will trigger an automatic rebuild
   - Check the build logs in Railway dashboard

### 2. Required Environment Variables

Add these in Railway Settings → Variables:

```bash
# Required
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/inklaunch?retryWrites=true&w=majority
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-key-change-this-min-32-chars
FLASK_ENV=production
DEBUG=False

# Optional (for full features)
OPENAI_API_KEY=sk-your-openai-api-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET_NAME=inklaunch-book-covers
AWS_REGION=us-east-1

# Email (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@inklaunch.com

# Admin
ADMIN_EMAILS=your-admin-email@example.com
```

### 3. MongoDB Setup (If Not Done)

**Option A: MongoDB Atlas (Free Tier)**
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create free cluster
3. Create database user
4. Whitelist IP: 0.0.0.0/0 (allow all)
5. Get connection string
6. Add to Railway as MONGODB_URI

**Option B: Railway MongoDB Template**
1. In Railway dashboard
2. New → Database → MongoDB
3. Copy connection string
4. Add as MONGODB_URI variable

### 4. Generate Secret Keys

Run these commands to generate secure keys:

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Custom Domain Setup

In Railway:
1. Go to Settings → Domains
2. Click "Custom Domain"
3. Enter your domain (e.g., inklaunch.com)
4. Copy the CNAME target provided
5. Add CNAME record in your DNS provider:
   ```
   Type: CNAME
   Name: @ (or your subdomain)
   Value: [Railway CNAME target]
   TTL: Auto
   ```

### 6. Verify Deployment

Once deployed, test these URLs:
- https://your-app.railway.app (or your custom domain)
- https://your-app.railway.app/books
- https://your-app.railway.app/marketing
- https://your-app.railway.app/writing

### 7. Initialize Database

After first deployment, you may want to seed some data:

SSH into Railway or use Railway CLI:
```bash
railway run python seed_data.py
railway run python seed_marketing_writing_tools.py
```

## 🔧 Troubleshooting

### Build Still Failing?
1. Check Railway build logs for specific errors
2. Verify all environment variables are set
3. Make sure MongoDB URI is correct and accessible

### App Not Starting?
1. Check Deploy Logs in Railway
2. Verify PORT environment variable is being used
3. Check MongoDB connection string format

### Database Connection Issues?
1. Whitelist 0.0.0.0/0 in MongoDB Atlas
2. Check MongoDB URI format
3. Verify database user has read/write permissions

### Need More Memory?
1. Upgrade Railway plan if needed
2. Or optimize by adding pagination
3. Add caching for frequent queries

## 📊 Post-Deployment Checklist

- [ ] App loads successfully
- [ ] Can create user account
- [ ] Can login
- [ ] Can create a book
- [ ] Marketing tools accessible
- [ ] Writing tools accessible
- [ ] Custom domain working
- [ ] SSL certificate active
- [ ] MongoDB backups enabled
- [ ] Error monitoring set up (optional: Sentry)

## 🎉 Success!

Your InkLaunch platform should now be live!

Visit your app and create your first admin account to get started.

## 💡 Next Steps

1. **Add Analytics**: Google Analytics or Plausible
2. **Set Up Monitoring**: Use Railway metrics or add Sentry
3. **Enable Backups**: Set up MongoDB Atlas automated backups
4. **Add CI/CD**: Already automatic with Railway!
5. **Scale**: Adjust worker count in railway.json as traffic grows

## 📞 Need Help?

If deployment issues persist:
1. Check Railway documentation
2. Share the error logs
3. Verify environment variables match the format above
