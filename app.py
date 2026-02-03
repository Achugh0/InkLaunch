"""Main application entry point."""
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Create uploads folder
    os.makedirs('uploads', exist_ok=True)
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config['DEBUG']
    )
