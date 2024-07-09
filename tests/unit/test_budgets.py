import pytest
from ProPyCore.access.budgets import Budgets
from ProPyCore.exceptions import NotFoundItemError

# Fixture for Budgets instance
@pytest.fixture
def budgets_instance(mocker):
    mocker.patch('ProPyCore.access.budgets.Base.__init__', return_value=None)  # Mock the base class initializer
    return Budgets('mock_access_token', 'mock_server_url')

def test_get_views(budgets_instance, mocker):
    # Mock the get_request method to return sample views with pagination
    mock_response_page_1 = [{'id': 1, 'name': 'View-1'}, {'id': 2, 'name': 'View-2'}]
    mock_response_page_2 = []

    mocker.patch.object(budgets_instance, 'get_request', side_effect=[mock_response_page_1, mock_response_page_2])

    response = budgets_instance.get_views(company_id=123, project_id=456)

    assert isinstance(response, list)
    assert response == mock_response_page_1

def test_find_view_by_id(budgets_instance, mocker):
    # Mock the get_views method
    mock_get_response_page_1 = [{'id': 1, 'name': 'View-1'}, {'id': 2, 'name': 'View-2'}]
    mock_get_response_page_2 = []

    mocker.patch.object(budgets_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])

    view_info = budgets_instance.find_view(company_id=123, project_id=456, identifier=1)

    assert isinstance(view_info, dict)
    assert view_info == {'id': 1, 'name': 'View-1'}

def test_find_view_by_name(budgets_instance, mocker):
    # Mock the get_views method
    mock_get_response_page_1 = [{'id': 1, 'name': 'View-1'}, {'id': 2, 'name': 'View-2'}]
    mock_get_response_page_2 = []

    mocker.patch.object(budgets_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])

    view_info = budgets_instance.find_view(company_id=123, project_id=456, identifier='View-2')

    assert isinstance(view_info, dict)
    assert view_info == {'id': 2, 'name': 'View-2'}

def test_find_view_not_found(budgets_instance, mocker):
    # Mock the get_views method to return sample views
    mock_get_response_page_1 = [{'id': 1, 'name': 'View-1'}, {'id': 2, 'name': 'View-2'}]
    mock_get_response_page_2 = []

    mocker.patch.object(budgets_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])

    with pytest.raises(NotFoundItemError):
        budgets_instance.find_view(company_id=123, project_id=456, identifier='Nonexistent View')

def test_get_budget_columns(budgets_instance, mocker):
    # Mock the get_request method to return sample columns
    mock_response = [{'id': 1, 'name': 'Column-1'}, {'id': 2, 'name': 'Column-2'}]
    mocker.patch.object(budgets_instance, 'get_request', return_value=mock_response)

    response = budgets_instance.get_budget_columns(company_id=123, project_id=456, budget_view_id=789)

    assert isinstance(response, list)
    assert response == mock_response

def test_find_budget_column_by_id(budgets_instance, mocker):
    # Mock the get_budget_columns method
    mock_get_response = [{'id': 1, 'name': 'Column-1'}, {'id': 2, 'name': 'Column-2'}]
    mocker.patch.object(budgets_instance, 'get_request', return_value=mock_get_response)

    column_info = budgets_instance.find_budget_column(company_id=123, project_id=456, budget_view_id=789, identifier=1)

    assert isinstance(column_info, dict)
    assert column_info == {'id': 1, 'name': 'Column-1'}

def test_find_budget_column_by_name(budgets_instance, mocker):
    # Mock the get_budget_columns method
    mock_get_response = [{'id': 1, 'name': 'Column-1'}, {'id': 2, 'name': 'Column-2'}]
    mocker.patch.object(budgets_instance, 'get_request', return_value=mock_get_response)

    column_info = budgets_instance.find_budget_column(company_id=123, project_id=456, budget_view_id=789, identifier='Column-2')

    assert isinstance(column_info, dict)
    assert column_info == {'id': 2, 'name': 'Column-2'}

def test_find_budget_column_not_found(budgets_instance, mocker):
    # Mock the get_budget_columns method to return sample columns
    mock_get_response = [{'id': 1, 'name': 'Column-1'}, {'id': 2, 'name': 'Column-2'}]
    mocker.patch.object(budgets_instance, 'get_request', return_value=mock_get_response)

    with pytest.raises(NotFoundItemError):
        budgets_instance.find_budget_column(company_id=123, project_id=456, budget_view_id=789, identifier='Nonexistent Column')

def test_get_budget_rows(budgets_instance, mocker):
    # Mock the get_request method to return sample rows
    mock_response = [{'id': 1, 'cost_code': '001'}, {'id': 2, 'cost_code': '002'}]
    mocker.patch.object(budgets_instance, 'get_request', return_value=mock_response)

    response = budgets_instance.get_budget_rows(company_id=123, project_id=456, budget_view_id=789)

    assert isinstance(response, list)
    assert response == mock_response

def test_find_budget_row_by_id(budgets_instance, mocker):
    # Mock the get_budget_rows method
    mock_get_response = [{'id': 1, 'cost_code': '001'}, {'id': 2, 'cost_code': '002'}]
    mocker.patch.object(budgets_instance, 'get_request', return_value=mock_get_response)

    row_info = budgets_instance.find_budget_row(company_id=123, project_id=456, budget_view_id=789, identifier=1)

    assert isinstance(row_info, dict)
    assert row_info == {'id': 1, 'cost_code': '001'}

def test_find_budget_row_by_cost_code(budgets_instance, mocker):
    # Mock the get_budget_rows method
    mock_get_response = [{'id': 1, 'cost_code': '001'}, {'id': 2, 'cost_code': '002'}]
    mocker.patch.object(budgets_instance, 'get_request', return_value=mock_get_response)

    row_info = budgets_instance.find_budget_row(company_id=123, project_id=456, budget_view_id=789, identifier='002')

    assert isinstance(row_info, dict)
    assert row_info == {'id': 2, 'cost_code': '002'}

def test_find_budget_row_not_found(budgets_instance, mocker):
    # Mock the get_budget_rows method to return sample rows
    mock_get_response = [{'id': 1, 'cost_code': '001'}, {'id': 2, 'cost_code': '002'}]
    mocker.patch.object(budgets_instance, 'get_request', return_value=mock_get_response)

    with pytest.raises(NotFoundItemError):
        budgets_instance.find_budget_row(company_id=123, project_id=456, budget_view_id=789, identifier='Nonexistent Row')

def test_get_budget_details(budgets_instance, mocker):
    # Mock the post_request method to return sample details
    mock_response = [{'id': 1, 'cost_code': '001'}, {'id': 2, 'cost_code': '002'}]
    mocker.patch.object(budgets_instance, 'post_request', return_value=mock_response)

    response = budgets_instance.get_budget_details(company_id=123, project_id=456, budget_view_id=789)

    assert isinstance(response, list)
    assert response == mock_response
