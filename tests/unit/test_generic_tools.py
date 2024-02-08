import pytest
from unittest.mock import MagicMock
from propycore.access.generic_tools import GenericTool
from propycore.exceptions import NotFoundItemError

# Fixture for GenericTool instance
@pytest.fixture
def generic_tool_instance():
    return GenericTool('mock_access_token', 'mock_server_url')

# Test for get_tools method
def test_get_tools(generic_tool_instance):
    # Mock the get_request method
    mock_response = [{'id': 1, 'title': 'Tool 1'}, {'id': 2, 'title': 'Tool 2'}]
    generic_tool_instance.get_request = MagicMock(return_value=mock_response)

    response = generic_tool_instance.get_tools(123)

    assert isinstance(response, list)
    assert response == mock_response

# Test for find_tool by id
def test_find_tool_by_id(generic_tool_instance):
    # Mock the get_tools method
    mock_response = [{'id': 1, 'title': 'Tool 1'}, {'id': 2, 'title': 'Tool 2'}]
    generic_tool_instance.get_tools = MagicMock(return_value=mock_response)

    tool = generic_tool_instance.find_tool(123, 1)

    assert tool == {'id': 1, 'title': 'Tool 1'}

# Test for find_tool by title
def test_find_tool_by_title(generic_tool_instance):
    # Mock the get_tools method
    mock_response = [{'id': 1, 'title': 'Tool 1'}, {'id': 2, 'title': 'Tool 2'}]
    generic_tool_instance.get_tools = MagicMock(return_value=mock_response)

    tool = generic_tool_instance.find_tool(123, 'Tool 2')

    assert tool == {'id': 2, 'title': 'Tool 2'}