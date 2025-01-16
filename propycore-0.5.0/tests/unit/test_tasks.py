import pytest
from ProPyCore.access.tasks import Task
from ProPyCore.exceptions import NotFoundItemError

# Fixture for Task instance
@pytest.fixture
def task_instance(mocker):
    mocker.patch('ProPyCore.access.tasks.Base.__init__', return_value=None)  # Mock the base class initializer
    return Task('mock_access_token', 'mock_server_url')

def test_get_tasks(task_instance, mocker):
    # Mock the get_request method to return sample tasks with pagination
    mock_response_page_1 = [{'id': 1, 'name': 'Task 1'}, {'id': 2, 'name': 'Task 2'}]
    mock_response_page_2 = []

    mocker.patch.object(task_instance, 'get_request', side_effect=[mock_response_page_1, mock_response_page_2])

    response = task_instance.get(company_id=123, project_id=456)

    assert isinstance(response, list)
    assert response == mock_response_page_1

def test_show_task(task_instance, mocker):
    # Mock the get_request method to return a specific task
    mock_response = {'id': 1, 'name': 'Task 1'}
    mocker.patch.object(task_instance, 'get_request', return_value=mock_response)

    response = task_instance.show(company_id=123, project_id=456, task_id=1)

    assert isinstance(response, dict)
    assert response == mock_response

def test_find_task_by_id(task_instance, mocker):
    # Mock the get and show methods
    mock_get_response_page_1 = [{'id': 1, 'name': 'Task 1'}, {'id': 2, 'name': 'Task 2'}]
    mock_get_response_page_2 = []
    mock_show_response = {'id': 1, 'name': 'Task 1'}

    mocker.patch.object(task_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])
    mocker.patch.object(task_instance, 'show', return_value=mock_show_response)

    task_info = task_instance.find(company_id=123, project_id=456, identifier=1)

    assert isinstance(task_info, dict)
    assert task_info == mock_show_response

def test_find_task_by_name(task_instance, mocker):
    # Mock the get and show methods
    mock_get_response_page_1 = [{'id': 1, 'name': 'Task 1'}, {'id': 2, 'name': 'Task 2'}]
    mock_get_response_page_2 = []
    mock_show_response = {'id': 2, 'name': 'Task 2'}

    mocker.patch.object(task_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])
    mocker.patch.object(task_instance, 'show', return_value=mock_show_response)

    task_info = task_instance.find(company_id=123, project_id=456, identifier='Task 2')

    assert isinstance(task_info, dict)
    assert task_info == mock_show_response

def test_find_task_not_found(task_instance, mocker):
    # Mock the get method to return sample tasks
    mock_get_response_page_1 = [{'id': 1, 'name': 'Task 1'}, {'id': 2, 'name': 'Task 2'}]
    mock_get_response_page_2 = []

    mocker.patch.object(task_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])

    with pytest.raises(NotFoundItemError):
        task_instance.find(company_id=123, project_id=456, identifier='Nonexistent Task')
