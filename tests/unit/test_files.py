import pytest
from unittest.mock import MagicMock, mock_open
from ProPyCore.access.documents.files import Files  # Adjust the import path as needed


class TestFiles:
    @pytest.fixture
    def files_instance(self, mocker):
        """
        Fixture to create an instance of the Files class with mocked dependencies.
        """
        mocker.patch("ProPyCore.access.documents.files.Base.__init__", return_value=None)  # Mock Base class init
        return Files(access_token="mock_access_token", server_url="mock_server_url")

    def test_create(self, files_instance, mocker):
        """
        Test the `create` method.
        """
        mock_file = mock_open(read_data="dummy content")
        mocker.patch("builtins.open", mock_file)
        mocker.patch.object(
            files_instance,
            "post_request",
            return_value={"id": 1, "name": "New File"}
        )

        response = files_instance.create(
            company_id=123,
            project_id=456,
            filepath="/path/to/file.txt",
            folder_id=789,
            description="Test file"
        )

        # Assertions
        assert response["id"] == 1
        assert response["name"] == "New File"

        # Verify the call to `post_request`
        files_instance.post_request.assert_called_once()
        
        # Extract the actual call arguments for comparison
        call_args = files_instance.post_request.call_args[1]

        # Validate `api_url`, `additional_headers`, `params`, and `data`
        assert call_args["api_url"] == "/rest/v1.0/files"
        assert call_args["additional_headers"] == {"Procore-Company-Id": "123"}
        assert call_args["params"] == {"project_id": 456}
        assert call_args["data"] == {
            "file[name]": "file.txt",
            "file[description]": "Test file",
            "file[parent_id]": 789,
        }

        # Validate the structure of `files` argument
        assert len(call_args["files"]) == 1
        assert call_args["files"][0][0] == "file[data]"
        assert mock_file.return_value in call_args["files"][0]

    def test_update(self, files_instance, mocker):
        """
        Test the `update` method.
        """
        mock_file = mock_open(read_data="dummy content")
        mocker.patch("builtins.open", mock_file)
        mocker.patch.object(
            files_instance,
            "patch_request",
            return_value={"id": 1, "name": "Updated File"}
        )

        response = files_instance.update(
            company_id=123,
            project_id=456,
            doc_id=1,
            filepath="/path/to/file.txt",
            folder_id=789,
            filename="Updated File.txt",
            description="Updated description"
        )

        # Assertions
        assert response["id"] == 1
        assert response["name"] == "Updated File"

        # Verify the call to `patch_request`
        files_instance.patch_request.assert_called_once()
        
        # Extract the actual call arguments for comparison
        call_args = files_instance.patch_request.call_args[1]

        # Validate `api_url`, `additional_headers`, `params`, and `data`
        assert call_args["api_url"] == "/rest/v1.0/files/1"
        assert call_args["additional_headers"] == {"Procore-Company-Id": "123"}
        assert call_args["params"] == {"project_id": 456}
        assert call_args["data"] == {
            "file[parent_id]": 789,
            "file[name]": "Updated File.txt",
            "file[description]": "Updated description",
        }

        # Validate the structure of `files` argument
        assert len(call_args["files"]) == 1
        assert call_args["files"][0][0] == "file[data]"
        assert mock_file.return_value in call_args["files"][0]

    def test_show(self, files_instance, mocker):
        """
        Test the `show` method.
        """
        mocker.patch.object(
            files_instance,
            "get_request",
            return_value={"id": 1, "name": "Test File"}
        )

        response = files_instance.show(company_id=123, project_id=456, doc_id=1)

        # Assertions
        assert response["id"] == 1
        assert response["name"] == "Test File"

        files_instance.get_request.assert_called_once_with(
            api_url="/rest/v1.0/files/1",
            additional_headers={"Procore-Company-Id": "123"},
            params={"project_id": 456}
        )

    def test_remove(self, files_instance, mocker):
        """
        Test the `remove` method.
        """
        mocker.patch.object(
            files_instance,
            "delete_request",
            return_value={"success": True}
        )

        response = files_instance.remove(company_id=123, project_id=456, doc_id=1)

        # Assertions
        assert response["success"] is True

        files_instance.delete_request.assert_called_once_with(
            api_url="/rest/v1.0/files/1",
            additional_headers={"Procore-Company-Id": "123"},
            params={"project_id": 456}
        )

    def test_get(self, files_instance, mocker):
        """
        Test the `get` method.
        """
        mocker.patch.object(
            files_instance,
            "get_request",
            side_effect=[
                [{"id": 1, "is_deleted": False}, {"id": 2, "is_deleted": False}],
                []  # To simulate pagination end
            ]
        )

        response = files_instance.get(company_id=123, project_id=456)

        # Assertions
        assert len(response) == 2
        assert response[0]["id"] == 1

        files_instance.get_request.assert_any_call(
            api_url="/rest/v1.0/projects/456/documents",
            additional_headers={"Procore-Company-Id": "123"},
            params={
                "view": "normal",
                "sort": "name",
                "page": 1,
                "per_page": 10000,
                "filters[document_type]": "file",
                "filters[is_in_recycle_bin]": False
            }
        )

    def test_search(self, files_instance, mocker):
        """
        Test the `search` method.
        """
        mocker.patch.object(
            files_instance,
            "get",
            return_value=[
                {"id": 1, "name": "Matching File", "is_deleted": False, "is_recycle_bin": False, "document_type": "file"},
                {"id": 2, "name": "Another File", "is_deleted": False, "is_recycle_bin": False, "document_type": "file"}
            ]
        )

        response = files_instance.search(company_id=123, project_id=456, value="Matching")

        # Assertions
        assert response["id"] == 1
        assert response["search_criteria"]["match"] > 0
