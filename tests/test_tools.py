"""Test tools functionality."""
import pytest


def test_metadata_checker_optimal(client):
    """Test metadata checker with optimal values."""
    response = client.post('/tools/metadata-checker', data={
        'title': 'This is a great book title that is between sixty and eighty chars',
        'description': 'This is a comprehensive book description that provides detailed information about the content, themes, and what readers can expect. It is definitely longer than 150 characters.'
    })
    
    assert response.status_code == 200
    assert b'looks good' in response.data


def test_metadata_checker_short_title(client):
    """Test metadata checker with short title."""
    response = client.post('/tools/metadata-checker', data={
        'title': 'Short',
        'description': 'This is a comprehensive book description that provides detailed information about the content, themes, and what readers can expect. It is definitely longer than 150 characters.'
    })
    
    assert response.status_code == 200
    assert b'too short' in response.data


def test_isbn_validator_valid_isbn10(client):
    """Test ISBN validator with valid ISBN-10."""
    response = client.post('/tools/isbn-validator', data={
        'isbn': '0-306-40615-2'
    })
    
    assert response.status_code == 200
    assert b'Valid' in response.data


def test_isbn_validator_valid_isbn13(client):
    """Test ISBN validator with valid ISBN-13."""
    response = client.post('/tools/isbn-validator', data={
        'isbn': '978-0-306-40615-7'
    })
    
    assert response.status_code == 200
    assert b'Valid' in response.data


def test_isbn_validator_invalid(client):
    """Test ISBN validator with invalid ISBN."""
    response = client.post('/tools/isbn-validator', data={
        'isbn': '1234567890'
    })
    
    assert response.status_code == 200
    assert b'Invalid' in response.data


def test_tools_list(client):
    """Test listing available tools."""
    response = client.get('/tools/')
    assert response.status_code == 200
    assert b'Metadata Checker' in response.data
    assert b'ISBN Validator' in response.data
