import pytest
from ProPyCore.access.budgets.rows import BudgetRows
from ProPyCore.exceptions import NotFoundItemError

# Fixture for BudgetRows instance
@pytest.fixture
def budget_rows_instance(mocker):
    mocker.patch('ProPyCore.access.budgets.rows.Base.__init__', return_value=None)  # Mock the base class initializer
    return BudgetRows('mock_access_token', 'mock_server_url')

def test_get_budget_rows(budget_rows_instance, mocker):
    # Mock the get_request method to return sample budget rows
    mock_response = [{'id': 1, 'cost_code': '001'}, {'id': 2, 'cost_code': '002'}]
    mocker.patch.object(budget_rows_instance, 'get_request', return_value=mock_response)

    response = budget_rows_instance.get(company_id=123, project_id=456, budget_view_id=789)

    assert isinstance(response, list)
    assert response == mock_response

def test_find_row_by_id(budget_rows_instance, mocker):
    # Mock the get method to return a list of budget rows
    mock_get_response = [{'id': 1, 'cost_code': '001'}, {'id': 2, 'cost_code': '002'}]
    mocker.patch.object(budget_rows_instance, 'get', return_value=mock_get_response)

    row_info = budget_rows_instance.find(company_id=123, project_id=456, budget_view_id=789, identifier=1)

    assert isinstance(row_info, dict)
    assert row_info == {'id': 1, 'cost_code': '001'}

def test_find_row_by_cost_code(budget_rows_instance, mocker):
    # Mock the get method to return a list of budget rows
    mock_get_response = [{'id': 1, 'cost_code': '001'}, {'id': 2, 'cost_code': '002'}]
    mocker.patch.object(budget_rows_instance, 'get', return_value=mock_get_response)

    row_info = budget_rows_instance.find(company_id=123, project_id=456, budget_view_id=789, identifier='002')

    assert isinstance(row_info, dict)
    assert row_info == {'id': 2, 'cost_code': '002'}

def test_find_row_not_found(budget_rows_instance, mocker):
    # Mock the get method to return a list of budget rows
    mock_get_response = [{'id': 1, 'cost_code': '001'}, {'id': 2, 'cost_code': '002'}]
    mocker.patch.object(budget_rows_instance, 'get', return_value=mock_get_response)

    with pytest.raises(NotFoundItemError):
        budget_rows_instance.find(company_id=123, project_id=456, budget_view_id=789, identifier='Nonexistent Row')
