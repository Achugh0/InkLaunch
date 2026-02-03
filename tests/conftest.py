"""Test configuration and fixtures."""
import pytest
from app import create_app, mongo
from config import TestingConfig


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    
    with app.app_context():
        # Clear test database
        mongo.db.users.delete_many({})
        mongo.db.books.delete_many({})
        mongo.db.reviews.delete_many({})
        
        yield app
        
        # Cleanup
        mongo.db.users.delete_many({})
        mongo.db.books.delete_many({})
        mongo.db.reviews.delete_many({})


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()
