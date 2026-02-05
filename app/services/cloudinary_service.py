"""Cloudinary image upload service - S3 alternative."""
import cloudinary
import cloudinary.uploader
from flask import current_app
import logging

logger = logging.getLogger(__name__)


class CloudinaryService:
    """Service for handling Cloudinary image uploads."""
    
    def __init__(self):
        """Initialize Cloudinary."""
        self.configured = False
    
    def _ensure_config(self):
        """Ensure Cloudinary is configured."""
        if not self.configured:
            cloud_name = current_app.config.get('CLOUDINARY_CLOUD_NAME')
            api_key = current_app.config.get('CLOUDINARY_API_KEY')
            api_secret = current_app.config.get('CLOUDINARY_API_SECRET')
            
            if not all([cloud_name, api_key, api_secret]):
                logger.warning("Cloudinary not configured")
                return False
            
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret,
                secure=True
            )
            self.configured = True
        return True
    
    def upload_file(self, file, folder='book-covers'):
        """
        Upload file to Cloudinary.
        
        Args:
            file: FileStorage object from Flask
            folder: Cloudinary folder name
            
        Returns:
            str: Public URL or None if failed
        """
        if not self._ensure_config():
            return None
        
        try:
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                file,
                folder=folder,
                resource_type='auto',
                format='jpg',  # Auto-convert to JPG for optimization
                quality='auto',  # Automatic quality optimization
                fetch_format='auto'  # Use best format for browser
            )
            
            url = result.get('secure_url')
            logger.info(f"Uploaded to Cloudinary: {url}")
            return url
            
        except Exception as e:
            logger.error(f"Cloudinary upload failed: {e}")
            return None
    
    def delete_file(self, url):
        """Delete file from Cloudinary."""
        if not self._ensure_config():
            return False
        
        try:
            # Extract public_id from URL
            parts = url.split('/')
            public_id = '/'.join(parts[-2:]).split('.')[0]
            
            cloudinary.uploader.destroy(public_id)
            return True
        except Exception as e:
            logger.error(f"Cloudinary delete failed: {e}")
            return False


cloudinary_service = CloudinaryService()
