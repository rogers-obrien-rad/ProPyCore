import pytest
from ProPyCore.access.rfis import RFI
from ProPyCore.exceptions import NotFoundItemError

# Fixture for RFI instance
@pytest.fixture
def rfi_instance(mocker):
    mocker.patch('ProPyCore.access.rfis.Base.__init__', return_value=None)  # Mock the base class initializer
    return RFI('mock_access_token', 'mock_server_url')

def test_get_rfies(rfi_instance, mocker):
    # Mock the get_request method to return sample RFIs with pagination
    mock_response_page_1 = [{'id': 1, 'number': 'RFI-1'}, {'id': 2, 'number': 'RFI-2'}]
    mock_response_page_2 = []

    mocker.patch.object(rfi_instance, 'get_request', side_effect=[mock_response_page_1, mock_response_page_2])

    response = rfi_instance.get(company_id=123, project_id=456)

    assert isinstance(response, list)
    assert response == mock_response_page_1

def test_show_rfi(rfi_instance, mocker):
    # Mock the get_request method to return a specific RFI
    mock_response = {'id': 1, 'number': 'RFI-1'}
    mocker.patch.object(rfi_instance, 'get_request', return_value=mock_response)

    response = rfi_instance.show(company_id=123, project_id=456, rfi_id=1)

    assert isinstance(response, dict)
    assert response == mock_response

def test_find_rfi_by_id(rfi_instance, mocker):
    # Mock the get and show methods
    mock_get_response_page_1 = [{'id': 1, 'number': 'RFI-1'}, {'id': 2, 'number': 'RFI-2'}]
    mock_get_response_page_2 = []
    mock_show_response = {'id': 1, 'number': 'RFI-1'}

    mocker.patch.object(rfi_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])
    mocker.patch.object(rfi_instance, 'show', return_value=mock_show_response)

    rfi_info = rfi_instance.find(company_id=123, project_id=456, identifier=1)

    assert isinstance(rfi_info, dict)
    assert rfi_info == mock_show_response

def test_find_rfi_by_number(rfi_instance, mocker):
    # Mock the get and show methods
    mock_get_response_page_1 = [{'id': 1, 'number': 'RFI-1'}, {'id': 2, 'number': 'RFI-2'}]
    mock_get_response_page_2 = []
    mock_show_response = {'id': 2, 'number': 'RFI-2'}

    mocker.patch.object(rfi_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])
    mocker.patch.object(rfi_instance, 'show', return_value=mock_show_response)

    rfi_info = rfi_instance.find(company_id=123, project_id=456, identifier='RFI-2')

    assert isinstance(rfi_info, dict)
    assert rfi_info == mock_show_response

def test_find_rfi_not_found(rfi_instance, mocker):
    # Mock the get method to return sample RFIs
    mock_get_response_page_1 = [{'id': 1, 'number': 'RFI-1'}, {'id': 2, 'number': 'RFI-2'}]
    mock_get_response_page_2 = []

    mocker.patch.object(rfi_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])

    with pytest.raises(NotFoundItemError):
        rfi_instance.find(company_id=123, project_id=456, identifier='Nonexistent RFI')
