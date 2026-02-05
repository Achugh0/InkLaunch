#!/bin/bash
# Deploy actual book covers to S3 and production database

set -e  # Exit on error

echo "======================================================================"
echo " DEPLOY BOOK COVERS TO PRODUCTION"
echo "======================================================================"

# Check prerequisites
command -v python >/dev/null 2>&1 || { echo "Python required but not installed."; exit 1; }

# Check AWS credentials
if [ -z "$AWS_ACCESS_KEY_ID" ]; then
    echo "❌ AWS_ACCESS_KEY_ID not set"
    echo "Run: export AWS_ACCESS_KEY_ID='your_key'"
    exit 1
fi

if [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "❌ AWS_SECRET_ACCESS_KEY not set"
    exit 1
fi

if [ -z "$AWS_S3_BUCKET_NAME" ]; then
    echo "❌ AWS_S3_BUCKET_NAME not set"
    echo "Run: export AWS_S3_BUCKET_NAME='your_bucket'"
    exit 1
fi

if [ -z "$MONGODB_URI" ]; then
    echo "❌ MONGODB_URI not set"
    echo "Run: export MONGODB_URI='mongodb+srv://...'"
    exit 1
fi

echo "✓ All credentials configured"
echo ""

# Run deployment
python deploy_images_to_s3.py

echo ""
echo "======================================================================"
echo " NEXT: Configure Render"
echo "======================================================================"
echo "Add these environment variables in Render dashboard:"
echo ""
echo "  AWS_ACCESS_KEY_ID"
echo "  AWS_SECRET_ACCESS_KEY"
echo "  AWS_S3_BUCKET_NAME"
echo "  AWS_REGION (optional, default: us-east-1)"
echo ""
echo "Then redeploy or wait for auto-deploy from GitHub."
echo "======================================================================"
