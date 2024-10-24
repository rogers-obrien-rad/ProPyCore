import pytest
from ProPyCore.access.budgets import Budgets
from ProPyCore.exceptions import NotFoundItemError

# Fixture for Budgets instance (this will initialize all submodules like views, columns, etc.)
@pytest.fixture
def budgets_instance(mocker):
    mocker.patch('ProPyCore.access.budgets.columns.Base.__init__', return_value=None)  # Mock the base class initializer
    return Budgets('mock_access_token', 'mock_server_url')

def test_get_budget_columns(budgets_instance, mocker):
    # Access BudgetColumns via the Budgets instance
    budget_columns_instance = budgets_instance.columns
    
    # Mock the get_request method to return sample columns
    mock_response = [{'id': 1, 'name': 'Column-1'}, {'id': 2, 'name': 'Column-2'}]
    mocker.patch.object(budget_columns_instance, 'get_request', return_value=mock_response)

    response = budget_columns_instance.get(company_id=123, project_id=456, budget_view_id=789)

    assert isinstance(response, list)
    assert response == mock_response

def test_find_column_by_id(budgets_instance, mocker):
    # Access BudgetColumns via the Budgets instance
    budget_columns_instance = budgets_instance.columns

    # Mock the get method to return a list of budget columns
    mock_get_response = [{'id': 1, 'name': 'Column-1'}, {'id': 2, 'name': 'Column-2'}]
    mocker.patch.object(budget_columns_instance, 'get', return_value=mock_get_response)

    column_info = budget_columns_instance.find(company_id=123, project_id=456, budget_view_id=789, identifier=1)

    assert isinstance(column_info, dict)
    assert column_info == {'id': 1, 'name': 'Column-1'}

def test_find_column_by_name(budgets_instance, mocker):
    # Access BudgetColumns via the Budgets instance
    budget_columns_instance = budgets_instance.columns

    # Mock the get method to return a list of budget columns
    mock_get_response = [{'id': 1, 'name': 'Column-1'}, {'id': 2, 'name': 'Column-2'}]
    mocker.patch.object(budget_columns_instance, 'get', return_value=mock_get_response)

    column_info = budget_columns_instance.find(company_id=123, project_id=456, budget_view_id=789, identifier='Column-2')

    assert isinstance(column_info, dict)
    assert column_info == {'id': 2, 'name': 'Column-2'}

def test_find_column_not_found(budgets_instance, mocker):
    # Access BudgetColumns via the Budgets instance
    budget_columns_instance = budgets_instance.columns

    # Mock the get method to return a list of budget columns
    mock_get_response = [{'id': 1, 'name': 'Column-1'}, {'id': 2, 'name': 'Column-2'}]
    mocker.patch.object(budget_columns_instance, 'get', return_value=mock_get_response)

    with pytest.raises(NotFoundItemError):
        budget_columns_instance.find(company_id=123, project_id=456, budget_view_id=789, identifier='Nonexistent Column')
