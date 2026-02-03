"""Test book routes."""
import pytest
from app.models import User, Book
import io


def create_test_user(client, email='test@example.com'):
    """Helper to create and login a test user."""
    client.post('/auth/register', data={
        'email': email,
        'password': 'Test123!@#',
        'full_name': 'Test User',
        'bio': 'Test bio'
    })
    
    client.post('/auth/login', data={
        'email': email,
        'password': 'Test123!@#'
    })
    
    with client.application.app_context():
        return User.find_by_email(email)


def test_create_book_not_logged_in(client):
    """Test creating book without login."""
    response = client.get('/books/create')
    assert response.status_code == 302  # Redirect to login


def test_create_book_logged_in(client):
    """Test creating book while logged in."""
    create_test_user(client)
    
    response = client.get('/books/create')
    assert response.status_code == 200
    assert b'Create New Book' in response.data


def test_create_book_submit(client):
    """Test book creation."""
    user = create_test_user(client)
    
    # Create test image
    data = {
        'title': 'Test Book',
        'subtitle': 'A Test Subtitle',
        'description': 'This is a test book description that is long enough to meet the minimum requirements of 100 characters for book descriptions.',
        'genre': 'Fiction',
        'isbn': '1234567890',
        'page_count': '300',
        'price': '9.99',
        'amazon_link': 'https://amazon.com/test',
        'cover_image': (io.BytesIO(b"fake image data"), 'test.jpg')
    }
    
    response = client.post('/books/create', data=data, 
                          content_type='multipart/form-data',
                          follow_redirects=True)
    
    assert response.status_code == 200
    
    # Verify book was created
    with client.application.app_context():
        books = Book.find_by_user(str(user['_id']))
        assert len(books) > 0
        assert books[0]['title'] == 'Test Book'


def test_create_book_short_description(client):
    """Test book creation with short description."""
    create_test_user(client)
    
    data = {
        'title': 'Test Book',
        'description': 'Too short',  # Less than 100 characters
        'genre': 'Fiction',
        'cover_image': (io.BytesIO(b"fake image data"), 'test.jpg')
    }
    
    response = client.post('/books/create', data=data,
                          content_type='multipart/form-data',
                          follow_redirects=True)
    
    assert response.status_code == 200
    assert b'100 characters' in response.data


def test_list_books(client):
    """Test listing books."""
    user = create_test_user(client)
    
    # Create a book
    with client.application.app_context():
        Book.create(str(user['_id']), {
            'title': 'Test Book',
            'description': 'Test description that is long enough to meet requirements',
            'genre': 'Fiction',
            'status': 'published'
        })
    
    response = client.get('/books/')
    assert response.status_code == 200


def test_get_book_details(client):
    """Test getting book details."""
    user = create_test_user(client)
    
    # Create a book
    with client.application.app_context():
        book_id = Book.create(str(user['_id']), {
            'title': 'Test Book',
            'description': 'Test description that is long enough to meet requirements',
            'genre': 'Fiction',
            'status': 'published'
        })
        
        book_id_str = str(book_id)
    
    response = client.get(f'/books/{book_id_str}')
    assert response.status_code == 200
    assert b'Test Book' in response.data


def test_edit_book_permission(client):
    """Test editing book without permission."""
    user1 = create_test_user(client, 'user1@example.com')
    
    # Create book as user1
    with client.application.app_context():
        book_id = Book.create(str(user1['_id']), {
            'title': 'Test Book',
            'description': 'Test description',
            'genre': 'Fiction',
            'status': 'published'
        })
    
    # Logout and login as different user
    client.get('/auth/logout')
    create_test_user(client, 'user2@example.com')
    
    # Try to edit
    response = client.get(f'/books/{str(book_id)}/edit', follow_redirects=True)
    assert response.status_code == 200
    assert b'Permission denied' in response.data


def test_delete_book(client):
    """Test deleting book."""
    user = create_test_user(client)
    
    # Create book
    with client.application.app_context():
        book_id = Book.create(str(user['_id']), {
            'title': 'Test Book',
            'description': 'Test description',
            'genre': 'Fiction',
            'status': 'published'
        })
        book_id_str = str(book_id)
    
    # Delete book
    response = client.post(f'/books/{book_id_str}/delete', follow_redirects=True)
    assert response.status_code == 200
    
    # Verify deletion
    with client.application.app_context():
        book = Book.find_by_id(book_id_str)
        assert book is None
