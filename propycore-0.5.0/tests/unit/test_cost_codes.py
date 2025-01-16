import pytest
from ProPyCore.access.cost_codes import CostCodes
from ProPyCore.exceptions import NotFoundItemError

# Fixture for CostCodes instance
@pytest.fixture
def cost_codes_instance(mocker):
    mocker.patch('ProPyCore.access.cost_codes.Base.__init__', return_value=None)  # Mock the base class initializer
    return CostCodes('mock_access_token', 'mock_server_url')

def test_get_cost_codes(cost_codes_instance, mocker):
    # Mock the get_request method to return sample cost codes for different pages
    mock_response_page_1 = [{'id': 1, 'name': 'Code 1'}, {'id': 2, 'name': 'Code 2'}]
    mock_response_page_2 = []

    mocker.patch.object(cost_codes_instance, 'get_request', side_effect=[mock_response_page_1, mock_response_page_2])

    response = cost_codes_instance.get(company_id=123, project_id=456)

    assert isinstance(response, list)
    assert response == mock_response_page_1

def test_show_cost_code(cost_codes_instance, mocker):
    # Mock the get_request method to return a specific cost code
    mock_response = {'id': 1, 'name': 'Code 1'}
    mocker.patch.object(cost_codes_instance, 'get_request', return_value=mock_response)

    cost_code = cost_codes_instance.show(company_id=123, project_id=456, cost_code_id=1)

    assert isinstance(cost_code, dict)
    assert cost_code == {'id': 1, 'name': 'Code 1'}

def test_find_cost_code_by_id(cost_codes_instance, mocker):
    # Mock the get method to return a list of cost codes
    mock_get_response = [{'id': 1, 'name': 'Code 1'}, {'id': 2, 'name': 'Code 2'}]
    mock_show_response = {'id': 1, 'name': 'Code 1'}

    mocker.patch.object(cost_codes_instance, 'get', return_value=mock_get_response)
    mocker.patch.object(cost_codes_instance, 'show', return_value=mock_show_response)

    cost_code = cost_codes_instance.find(company_id=123, project_id=456, identifier=1)

    assert isinstance(cost_code, dict)
    assert cost_code == {'id': 1, 'name': 'Code 1'}

def test_find_cost_code_not_found(cost_codes_instance, mocker):
    # Mock the get method to return a list of cost codes
    mock_get_response = [{'id': 1, 'name': 'Code 1'}, {'id': 2, 'name': 'Code 2'}]
    mocker.patch.object(cost_codes_instance, 'get', return_value=mock_get_response)

    with pytest.raises(NotFoundItemError):
        cost_codes_instance.find(company_id=123, project_id=456, identifier=999)