"""Test review functionality."""
import pytest
from app.models import User, Book, Review


def create_test_user_and_book(client, email='test@example.com'):
    """Helper to create user and book."""
    # Register and login
    client.post('/auth/register', data={
        'email': email,
        'password': 'Test123!@#',
        'full_name': 'Test User'
    })
    
    client.post('/auth/login', data={
        'email': email,
        'password': 'Test123!@#'
    })
    
    with client.application.app_context():
        user = User.find_by_email(email)
        book_id = Book.create(str(user['_id']), {
            'title': 'Test Book',
            'description': 'Test description that meets minimum length requirements',
            'genre': 'Fiction',
            'status': 'published'
        })
        return user, str(book_id)


def test_create_review(client):
    """Test creating a review."""
    # Create book owner
    user1, book_id = create_test_user_and_book(client, 'owner@example.com')
    
    # Logout and login as reviewer
    client.get('/auth/logout')
    user2, _ = create_test_user_and_book(client, 'reviewer@example.com')
    
    # Create review
    response = client.post('/reviews/create', data={
        'book_id': book_id,
        'rating': 5,
        'review_text': 'This is an excellent book with great character development and plot.'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'submitted successfully' in response.data
    
    # Verify review was created
    with client.application.app_context():
        reviews = Review.find_by_book(book_id, status=None)
        assert len(reviews) > 0
        assert reviews[0]['rating'] == 5
        assert reviews[0]['status'] == 'pending'


def test_create_review_own_book(client):
    """Test creating review for own book (should fail)."""
    user, book_id = create_test_user_and_book(client)
    
    # Try to review own book
    response = client.post('/reviews/create', data={
        'book_id': book_id,
        'rating': 5,
        'review_text': 'This is my own book and it is excellent!'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'cannot review your own book' in response.data


def test_create_review_too_short(client):
    """Test creating review with too short text."""
    user1, book_id = create_test_user_and_book(client, 'owner@example.com')
    
    # Logout and login as reviewer
    client.get('/auth/logout')
    user2, _ = create_test_user_and_book(client, 'reviewer@example.com')
    
    # Create review with short text
    response = client.post('/reviews/create', data={
        'book_id': book_id,
        'rating': 5,
        'review_text': 'Too short'  # Less than 50 characters
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'at least' in response.data


def test_approve_review_as_admin(client):
    """Test approving review as admin."""
    # Create book owner
    user1, book_id = create_test_user_and_book(client, 'owner@example.com')
    
    # Create reviewer
    client.get('/auth/logout')
    user2, _ = create_test_user_and_book(client, 'reviewer@example.com')
    
    # Create review
    with client.application.app_context():
        review_id = Review.create(book_id, str(user2['_id']), 5, 
                                 'This is an excellent book with great content.')
        review_id_str = str(review_id)
    
    # Login as admin
    client.get('/auth/logout')
    client.post('/auth/register', data={
        'email': 'ashchugh@gmail.com',
        'password': 'Admin123!@#',
        'full_name': 'Admin User'
    })
    client.post('/auth/login', data={
        'email': 'ashchugh@gmail.com',
        'password': 'Admin123!@#'
    })
    
    # Approve review
    response = client.post(f'/reviews/{review_id_str}/approve', follow_redirects=True)
    assert response.status_code == 200
    
    # Verify approval
    with client.application.app_context():
        review = Review.find_by_id(review_id_str)
        assert review['status'] == 'approved'


def test_review_average_rating(client):
    """Test calculating average rating."""
    user1, book_id = create_test_user_and_book(client, 'owner@example.com')
    
    # Create multiple reviews
    with client.application.app_context():
        # Create reviewer users
        user2_id = User.create('reviewer1@example.com', 'Test123!@#', 'Reviewer 1')
        user3_id = User.create('reviewer2@example.com', 'Test123!@#', 'Reviewer 2')
        
        # Create and approve reviews
        review1_id = Review.create(book_id, str(user2_id), 5, 
                                  'Excellent book with great content and writing style.')
        review2_id = Review.create(book_id, str(user3_id), 4, 
                                  'Very good book, enjoyed reading it thoroughly.')
        
        Review.update_status(str(review1_id), 'approved')
        Review.update_status(str(review2_id), 'approved')
        
        # Get average
        rating_info = Review.get_average_rating(book_id)
        assert rating_info['average'] == 4.5
        assert rating_info['count'] == 2
