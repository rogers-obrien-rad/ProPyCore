import pytest
from ProPyCore.access.direct_costs import DirectCosts
from ProPyCore.exceptions import NotFoundItemError

# Fixture for DirectCosts instance
@pytest.fixture
def direct_costs_instance(mocker):
    mocker.patch('ProPyCore.access.direct_costs.Base.__init__', return_value=None)  # Mock the base class initializer
    return DirectCosts('mock_access_token', 'mock_server_url')

def test_get_direct_costs(direct_costs_instance, mocker):
    # Mock the get_request method to return sample Direct Costs with pagination
    mock_response_page_1 = [{'id': 1, 'cost_code': 'DC-1'}, {'id': 2, 'cost_code': 'DC-2'}]
    mock_response_page_2 = []

    mocker.patch.object(direct_costs_instance, 'get_request', side_effect=[mock_response_page_1, mock_response_page_2])

    response = direct_costs_instance.get(company_id=123, project_id=456)

    assert isinstance(response, list)
    assert response == mock_response_page_1

def test_show_direct_cost(direct_costs_instance, mocker):
    # Mock the get_request method to return a specific Direct Cost
    mock_response = {'id': 1, 'cost_code': 'DC-1'}
    mocker.patch.object(direct_costs_instance, 'get_request', return_value=mock_response)

    response = direct_costs_instance.show(company_id=123, project_id=456, direct_cost_id=1)

    assert isinstance(response, dict)
    assert response == mock_response

def test_find_direct_cost_by_id(direct_costs_instance, mocker):
    # Mock the get and show methods
    mock_get_response_page_1 = [{'id': 1, 'cost_code': 'DC-1'}, {'id': 2, 'cost_code': 'DC-2'}]
    mock_get_response_page_2 = []
    mock_show_response = {'id': 1, 'cost_code': 'DC-1'}

    mocker.patch.object(direct_costs_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])
    mocker.patch.object(direct_costs_instance, 'show', return_value=mock_show_response)

    direct_cost_info = direct_costs_instance.find(company_id=123, project_id=456, identifier=1)

    assert isinstance(direct_cost_info, dict)
    assert direct_cost_info == mock_show_response
