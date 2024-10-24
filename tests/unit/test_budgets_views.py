import pytest
from ProPyCore.access.budgets.views import BudgetViews
from ProPyCore.exceptions import NotFoundItemError

# Fixture for BudgetViews instance
@pytest.fixture
def budget_views_instance(mocker):
    mocker.patch('ProPyCore.access.budgets.views.Base.__init__', return_value=None)  # Mock the base class initializer
    return BudgetViews('mock_access_token', 'mock_server_url')

def test_get_budget_views(budget_views_instance, mocker):
    # Mock the get_request method to return sample budget views
    mock_response = [{'id': 1, 'name': 'View-1'}, {'id': 2, 'name': 'View-2'}]
    mocker.patch.object(budget_views_instance, 'get_request', return_value=mock_response)

    response = budget_views_instance.get(company_id=123, project_id=456)

    assert isinstance(response, list)
    assert response == mock_response

def test_find_view_by_id(budget_views_instance, mocker):
    # Mock the get method to return a list of budget views
    mock_get_response = [{'id': 1, 'name': 'View-1'}, {'id': 2, 'name': 'View-2'}]
    mocker.patch.object(budget_views_instance, 'get', return_value=mock_get_response)

    view_info = budget_views_instance.find(company_id=123, project_id=456, identifier=1)

    assert isinstance(view_info, dict)
    assert view_info == {'id': 1, 'name': 'View-1'}

def test_find_view_by_name(budget_views_instance, mocker):
    # Mock the get method to return a list of budget views
    mock_get_response = [{'id': 1, 'name': 'View-1'}, {'id': 2, 'name': 'View-2'}]
    mocker.patch.object(budget_views_instance, 'get', return_value=mock_get_response)

    view_info = budget_views_instance.find(company_id=123, project_id=456, identifier='View-2')

    assert isinstance(view_info, dict)
    assert view_info == {'id': 2, 'name': 'View-2'}

def test_find_view_not_found(budget_views_instance, mocker):
    # Mock the get method to return a list of budget views
    mock_get_response = [{'id': 1, 'name': 'View-1'}, {'id': 2, 'name': 'View-2'}]
    mocker.patch.object(budget_views_instance, 'get', return_value=mock_get_response)

    with pytest.raises(NotFoundItemError):
        budget_views_instance.find(company_id=123, project_id=456, identifier='Nonexistent View')
