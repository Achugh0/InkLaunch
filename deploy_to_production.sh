#!/bin/bash
# Quick deploy script for book cover images to production

echo "======================================================================"
echo " DEPLOY BOOK COVERS TO PRODUCTION (S3 + MongoDB Atlas)"
echo "======================================================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if AWS credentials are set
if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ] || [ -z "$AWS_S3_BUCKET_NAME" ]; then
    echo -e "${RED}❌ AWS credentials not set!${NC}"
    echo ""
    echo "Please run these commands first:"
    echo ""
    echo "  export AWS_ACCESS_KEY_ID='your_access_key'"
    echo "  export AWS_SECRET_ACCESS_KEY='your_secret_key'"
    echo "  export AWS_S3_BUCKET_NAME='your_bucket_name'"
    echo "  export AWS_REGION='us-east-1'  # optional"
    echo ""
    echo "See S3_SETUP_GUIDE.md for help setting up AWS S3."
    exit 1
fi

# Check if MongoDB URI is set
if [ -z "$MONGODB_URI" ]; then
    echo -e "${RED}❌ MongoDB URI not set!${NC}"
    echo ""
    echo "Please run:"
    echo "  export MONGODB_URI='mongodb+srv://username:password@cluster.mongodb.net/inklaunch'"
    exit 1
fi

# Check if boto3 is installed
if ! python -c "import boto3" 2>/dev/null; then
    echo -e "${YELLOW}⚠ boto3 not installed. Installing...${NC}"
    pip install boto3 pymongo
fi

echo -e "${GREEN}✓ Credentials configured${NC}"
echo -e "${GREEN}✓ Bucket: $AWS_S3_BUCKET_NAME${NC}"
echo ""
echo "======================================================================"
echo " STEP 1: Upload Images to S3"
echo "======================================================================"

# Run the Python deployment script
python deploy_images_to_s3.py

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================================================"
    echo " STEP 2: Configure Render Environment Variables"
    echo "======================================================================"
    echo ""
    echo "Go to your Render dashboard and add these environment variables:"
    echo ""
    echo "  AWS_ACCESS_KEY_ID = $AWS_ACCESS_KEY_ID"
    echo "  AWS_SECRET_ACCESS_KEY = (your secret key)"
    echo "  AWS_S3_BUCKET_NAME = $AWS_S3_BUCKET_NAME"
    echo "  AWS_REGION = ${AWS_REGION:-us-east-1}"
    echo ""
    echo "======================================================================"
    echo " DEPLOYMENT COMPLETE! 🚀"
    echo "======================================================================"
    echo ""
    echo "✓ Images uploaded to S3"
    echo "✓ Production database updated"
    echo "✓ Ready for Render deployment"
    echo ""
    echo "Visit your Render app to see the actual book covers!"
else
    echo ""
    echo -e "${RED}❌ Deployment failed. Check the errors above.${NC}"
    exit 1
fi
