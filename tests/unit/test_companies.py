import pytest
from unittest.mock import MagicMock
from propycore.access.companies import Companies
from propycore.exceptions import NotFoundItemError

# Fixture for Companies instance
@pytest.fixture
def companies_instance():
    return Companies('mock_access_token', 'mock_server_url')

# Test for get method
def test_get_companies(companies_instance):
    # Mock the get_request method
    companies_instance.get_request = MagicMock(return_value=[{'id': 1, 'is_active': True, 'name': 'Test Company'}])

    response = companies_instance.get()

    assert isinstance(response, list)
    assert 'id' in response[0]
    assert 'is_active' in response[0]
    assert 'name' in response[0]

# Test for find method by id
def test_find_company_by_id(companies_instance):
    # Mock the get method
    companies_instance.get = MagicMock(return_value=[{'id': 1, 'name': 'Test Company'}])

    company = companies_instance.find(1)

    assert company['id'] == 1
    assert company['name'] == 'Test Company'

# Test for find method by name
def test_find_company_by_name(companies_instance):
    companies_instance.get = MagicMock(return_value=[{'id': 1, 'name': 'Test Company'}])

    company = companies_instance.find('Test Company')

    assert company['id'] == 1
    assert company['name'] == 'Test Company'

# Test for find method not found
def test_find_company_not_found(companies_instance):
    companies_instance.get = MagicMock(return_value=[])

    with pytest.raises(NotFoundItemError):
        companies_instance.find('Nonexistent Company')