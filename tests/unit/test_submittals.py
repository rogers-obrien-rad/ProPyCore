import pytest
from ProPyCore.access.submittals import Submittal
from ProPyCore.exceptions import NotFoundItemError

# Fixture for Submittal instance
@pytest.fixture
def submittal_instance(mocker):
    mocker.patch('ProPyCore.access.submittals.Base.__init__', return_value=None)  # Mock the base class initializer
    return Submittal('mock_access_token', 'mock_server_url')

def test_get_submittals(submittal_instance, mocker):
    # Mock the get_request method to return sample submittals with pagination
    mock_response_page_1 = [{'id': 1, 'title': 'Submittal-1'}, {'id': 2, 'title': 'Submittal-2'}]
    mock_response_page_2 = []

    mocker.patch.object(submittal_instance, 'get_request', side_effect=[mock_response_page_1, mock_response_page_2])

    response = submittal_instance.get(company_id=123, project_id=456)

    assert isinstance(response, list)
    assert response == mock_response_page_1

def test_show_submittal(submittal_instance, mocker):
    # Mock the get_request method to return a specific submittal
    mock_response = {'id': 1, 'title': 'Submittal-1'}
    mocker.patch.object(submittal_instance, 'get_request', return_value=mock_response)

    response = submittal_instance.show(company_id=123, project_id=456, submittal_id=1)

    assert isinstance(response, dict)
    assert response == mock_response

def test_find_submittal_by_id(submittal_instance, mocker):
    # Mock the get and show methods
    mock_get_response_page_1 = [{'id': 1, 'title': 'Submittal-1'}, {'id': 2, 'title': 'Submittal-2'}]
    mock_get_response_page_2 = []
    mock_show_response = {'id': 1, 'title': 'Submittal-1'}

    mocker.patch.object(submittal_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])
    mocker.patch.object(submittal_instance, 'show', return_value=mock_show_response)

    submittal_info = submittal_instance.find(company_id=123, project_id=456, identifier=1)

    assert isinstance(submittal_info, dict)
    assert submittal_info == mock_show_response

def test_find_submittal_by_title(submittal_instance, mocker):
    # Mock the get and show methods
    mock_get_response_page_1 = [{'id': 1, 'title': 'Submittal-1'}, {'id': 2, 'title': 'Submittal-2'}]
    mock_get_response_page_2 = []
    mock_show_response = {'id': 2, 'title': 'Submittal-2'}

    mocker.patch.object(submittal_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])
    mocker.patch.object(submittal_instance, 'show', return_value=mock_show_response)

    submittal_info = submittal_instance.find(company_id=123, project_id=456, identifier='Submittal-2')

    assert isinstance(submittal_info, dict)
    assert submittal_info == mock_show_response

def test_find_submittal_not_found(submittal_instance, mocker):
    # Mock the get method to return sample submittals
    mock_get_response_page_1 = [{'id': 1, 'title': 'Submittal-1'}, {'id': 2, 'title': 'Submittal-2'}]
    mock_get_response_page_2 = []

    mocker.patch.object(submittal_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])

    with pytest.raises(NotFoundItemError):
        submittal_instance.find(company_id=123, project_id=456, identifier='Nonexistent Submittal')
