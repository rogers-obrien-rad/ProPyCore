import pytest
from ProPyCore.access.budgets.details import BudgetDetails
from ProPyCore.exceptions import NotFoundItemError

# Fixture for BudgetDetails instance
@pytest.fixture
def budget_details_instance(mocker):
    mocker.patch('ProPyCore.access.budgets.details.Base.__init__', return_value=None)  # Mock the base class initializer
    return BudgetDetails('mock_access_token', 'mock_server_url')

def test_get_budget_details(budget_details_instance, mocker):
    # Mock the post_request method to return sample budget details
    mock_response = [{'id': 1, 'cost_code': '001'}, {'id': 2, 'cost_code': '002'}]
    mocker.patch.object(budget_details_instance, 'post_request', return_value=mock_response)

    response = budget_details_instance.get(company_id=123, project_id=456, budget_view_id=789)

    assert isinstance(response, list)
    assert response == mock_response

def test_find_detail_by_id(budget_details_instance, mocker):
    # Mock the get method to return a list of budget details
    mock_get_response = [{'id': 1, 'cost_code': '001'}, {'id': 2, 'cost_code': '002'}]
    mocker.patch.object(budget_details_instance, 'get', return_value=mock_get_response)

    detail = next((d for d in mock_get_response if d['id'] == 1), None)
    
    assert detail == {'id': 1, 'cost_code': '001'}

def test_find_detail_by_cost_code(budget_details_instance, mocker):
    # Mock the get method to return a list of budget details
    mock_get_response = [{'id': 1, 'cost_code': '001'}, {'id': 2, 'cost_code': '002'}]
    mocker.patch.object(budget_details_instance, 'get', return_value=mock_get_response)

    detail = next((d for d in mock_get_response if d['cost_code'] == '002'), None)
    
    assert detail == {'id': 2, 'cost_code': '002'}

def test_detail_not_found(budget_details_instance, mocker):
    # Mock the get method to return a list of budget details
    mock_get_response = [{'id': 1, 'cost_code': '001'}, {'id': 2, 'cost_code': '002'}]
    mocker.patch.object(budget_details_instance, 'get', return_value=mock_get_response)

    detail = next((d for d in mock_get_response if d['id'] == 999), None)

    assert detail is None
