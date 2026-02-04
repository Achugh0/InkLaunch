# Render Deployment Setup Guide

## Required Environment Variables

To deploy InkLaunch on Render, you **must** configure these environment variables:

### 1. MongoDB (REQUIRED)
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/inklaunch?retryWrites=true&w=majority
```

**How to get MongoDB URI:**
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Create a free account and cluster
3. Click "Connect" → "Connect your application"
4. Copy the connection string
5. Replace `<password>` with your database password
6. Replace `<dbname>` with `inklaunch`

### 2. Flask Configuration (REQUIRED)
```
SECRET_KEY=your-super-secret-random-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_ENV=production
DEBUG=False
```

Generate random keys with:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Admin Configuration
```
ADMIN_EMAILS=your-email@example.com
```

### 4. Optional Services

#### AWS S3 (for file uploads)
```
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_S3_BUCKET_NAME=your-bucket-name
AWS_REGION=us-east-1
```

#### OpenAI (for AI features)
```
OPENAI_API_KEY=sk-your-openai-api-key
AI_MODEL=gpt-4-turbo
```

#### Email (for notifications)
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
```

## Render Configuration

### Build Command
```bash
pip install -r requirements.txt
```

### Start Command
```bash
gunicorn app:app
```

## Troubleshooting

### Error: "Database connection error: 'NoneType' object is not subscriptable"
- **Cause:** MongoDB is not configured or connection failed
- **Solution:** 
  1. Make sure `MONGODB_URI` is set in Render environment variables
  2. Verify the MongoDB connection string is correct
  3. Check MongoDB Atlas allows connections from anywhere (0.0.0.0/0) or add Render IPs

### Error: "Internal Server Error" or "502 Bad Gateway"
- Check Render logs for specific error messages
- Verify all required environment variables are set
- Make sure MongoDB cluster is running

### App loads but shows 0 books/users
- Database might be empty - you need to seed data
- Or MongoDB connection is working but database name is different

## Initial Database Setup

After deploying, you may want to seed initial data:

1. Connect to your Render shell
2. Run the seed scripts:
```bash
python seed_data.py
python create_admin_users.py
```

## Monitoring

- Check Render logs regularly: Dashboard → Logs tab
- Monitor MongoDB usage in Atlas dashboard
- Set up alerts for app errors

## Security Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` and `JWT_SECRET_KEY` (random, 32+ characters)
- [ ] MongoDB connection uses authentication
- [ ] AWS credentials (if used) have minimal required permissions
- [ ] Email password is app-specific password, not account password
- [ ] HTTPS is enabled (Render does this automatically)
