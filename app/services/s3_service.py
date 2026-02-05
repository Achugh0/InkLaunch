"""AWS S3 service for file uploads."""
import boto3
from botocore.exceptions import ClientError
import logging
import uuid
import os
from werkzeug.utils import secure_filename
from flask import current_app

logger = logging.getLogger(__name__)


class S3Service:
    """Service for handling S3 file operations."""
    
    def __init__(self):
        """Initialize S3 client."""
        self.s3_client = None
        self.bucket_name = None
        self.region = None
    
    def _ensure_client(self):
        """Ensure S3 client is initialized."""
        if self.s3_client is None:
            access_key = current_app.config.get('AWS_ACCESS_KEY_ID')
            secret_key = current_app.config.get('AWS_SECRET_ACCESS_KEY')
            self.bucket_name = current_app.config.get('AWS_S3_BUCKET_NAME')
            self.region = current_app.config.get('AWS_REGION', 'us-east-1')
            
            if not access_key or not secret_key or not self.bucket_name:
                logger.warning("AWS credentials not configured, falling back to local storage")
                return False
            
            try:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                    region_name=self.region
                )
                return True
            except Exception as e:
                logger.error(f"Failed to initialize S3 client: {e}")
                return False
        return True
    
    def upload_file(self, file, folder='uploads'):
        """
        Upload a file to S3.
        
        Args:
            file: FileStorage object from Flask request
            folder: Folder path in S3 bucket
            
        Returns:
            str: Public URL of uploaded file, or None if upload failed
        """
        if not self._ensure_client():
            return None
        
        try:
            # Generate secure filename
            original_filename = secure_filename(file.filename)
            file_extension = os.path.splitext(original_filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{file_extension}"
            s3_key = f"{folder}/{unique_filename}"
            
            # Upload file to S3
            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                s3_key,
                ExtraArgs={
                    'ACL': 'public-read',
                    'ContentType': file.content_type or 'application/octet-stream'
                }
            )
            
            # Generate public URL
            url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{s3_key}"
            logger.info(f"Successfully uploaded file to S3: {url}")
            return url
            
        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error uploading to S3: {e}")
            return None
    
    def delete_file(self, url):
        """
        Delete a file from S3 given its URL.
        
        Args:
            url: Full S3 URL of the file
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        if not self._ensure_client():
            return False
        
        try:
            # Extract S3 key from URL
            # URL format: https://bucket-name.s3.region.amazonaws.com/key
            if self.bucket_name not in url:
                logger.warning(f"URL does not match bucket name: {url}")
                return False
            
            # Extract the key (path after bucket URL)
            key = url.split(f"{self.bucket_name}.s3.{self.region}.amazonaws.com/")[1]
            
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            logger.info(f"Successfully deleted file from S3: {key}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to delete file from S3: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting from S3: {e}")
            return False
    
    def is_s3_configured(self):
        """Check if S3 is properly configured."""
        return self._ensure_client()


# Global service instance
s3_service = S3Service()
