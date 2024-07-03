import pytest
from ProPyCore.access.projects import Projects
from ProPyCore.exceptions import NotFoundItemError

# Fixture for Projects instance
@pytest.fixture
def projects_instance(mocker):
    mocker.patch('ProPyCore.access.projects.Base.__init__', return_value=None)  # Mock the base class initializer
    return Projects('mock_access_token', 'mock_server_url')

def test_get_projects(projects_instance, mocker):
    # Mock the get_request method to return sample projects
    mock_response_page_1 = [{'id': 1, 'name': 'Project 1'}, {'id': 2, 'name': 'Project 2'}]
    mock_response_page_2 = []

    mocker.patch.object(projects_instance, 'get_request', side_effect=[mock_response_page_1, mock_response_page_2])

    response = projects_instance.get(company_id=123)

    assert isinstance(response, list)
    assert response == mock_response_page_1

def test_find_project_by_id(projects_instance, mocker):
    # Mock the get method to return sample projects
    mock_response = [{'id': 1, 'name': 'Project 1'}, {'id': 2, 'name': 'Project 2'}]
    mocker.patch.object(projects_instance, 'get', return_value=mock_response)

    project = projects_instance.find(company_id=123, identifier=1)

    assert project == {'id': 1, 'name': 'Project 1'}

def test_find_project_by_name(projects_instance, mocker):
    # Mock the get method to return sample projects
    mock_response = [{'id': 1, 'name': 'Project 1'}, {'id': 2, 'name': 'Project 2'}]
    mocker.patch.object(projects_instance, 'get', return_value=mock_response)

    project = projects_instance.find(company_id=123, identifier='Project 2')

    assert project == {'id': 2, 'name': 'Project 2'}

def test_find_project_not_found(projects_instance, mocker):
    # Mock the get method to return sample projects
    mock_response = [{'id': 1, 'name': 'Project 1'}, {'id': 2, 'name': 'Project 2'}]
    mocker.patch.object(projects_instance, 'get', return_value=mock_response)

    with pytest.raises(NotFoundItemError):
        projects_instance.find(company_id=123, identifier='Nonexistent Project')
