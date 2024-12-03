import pytest
from unittest.mock import MagicMock
from ProPyCore.access.documents.folders import Folders  # Adjust the import path as needed


class TestFolders:
    @pytest.fixture
    def folders_instance(self, mocker):
        """
        Fixture to create an instance of the Folders class with mocked dependencies.
        """
        mocker.patch("ProPyCore.access.documents.folders.Base.__init__", return_value=None)  # Mock Base class init
        return Folders(access_token="mock_access_token", server_url="mock_server_url")

    def test_show(self, folders_instance, mocker):
        """
        Test the `show` method.
        """
        mocker.patch.object(
            folders_instance,
            "get_request",
            return_value={"id": 1, "name": "Test Folder"}
        )

        response = folders_instance.show(company_id=123, project_id=456, doc_id=1)

        # Assertions
        assert response["id"] == 1
        assert response["name"] == "Test Folder"

        folders_instance.get_request.assert_called_once_with(
            api_url="/rest/v1.0/folders/1",
            additional_headers={"Procore-Company-Id": "123"},
            params={"project_id": 456}
        )

    def test_remove(self, folders_instance, mocker):
        """
        Test the `remove` method.
        """
        mocker.patch.object(
            folders_instance,
            "delete_request",
            return_value={"success": True}
        )

        response = folders_instance.remove(company_id=123, project_id=456, doc_id=1)

        # Assertions
        assert response["success"] is True

        folders_instance.delete_request.assert_called_once_with(
            api_url="/rest/v1.0/folders/1",
            additional_headers={"Procore-Company-Id": "123"},
            params={"project_id": 456}
        )

    def test_get(self, folders_instance, mocker):
        """
        Test the `get` method.
        """
        mocker.patch.object(
            folders_instance,
            "get_request",
            side_effect=[
                [{"id": 1, "is_deleted": False}, {"id": 2, "is_deleted": False}],
                []  # To simulate pagination end
            ]
        )

        response = folders_instance.get(company_id=123, project_id=456)

        # Assertions
        assert len(response) == 2
        assert response[0]["id"] == 1

        folders_instance.get_request.assert_any_call(
            api_url="/rest/v1.0/projects/456/documents",
            additional_headers={"Procore-Company-Id": "123"},
            params={
                "view": "normal",
                "sort": "name",
                "page": 1,
                "per_page": 10000,
                "filters[document_type]": "folder",
                "filters[is_in_recycle_bin]": False
            }
        )

    def test_search(self, folders_instance, mocker):
        """
        Test the `search` method.
        """
        mocker.patch.object(
            folders_instance,
            "get",
            return_value=[
                {"id": 1, "name": "Matching Folder", "is_deleted": False, "is_recycle_bin": False, "document_type": "folder"},
                {"id": 2, "name": "Another Folder", "is_deleted": False, "is_recycle_bin": False, "document_type": "folder"}
            ]
        )

        response = folders_instance.search(company_id=123, project_id=456, value="Matching")

        # Assertions
        assert response["id"] == 1
        assert response["search_criteria"]["match"] > 0

    def test_create(self, folders_instance, mocker):
        """
        Test the `create` method.
        """
        mocker.patch.object(
            folders_instance,
            "post_request",
            return_value={"id": 1, "name": "New Folder"}
        )

        response = folders_instance.create(company_id=123, project_id=456, folder_name="New Folder")

        # Assertions
        assert response["id"] == 1
        assert response["name"] == "New Folder"

        folders_instance.post_request.assert_called_once_with(
            api_url="/rest/v1.0/folders",
            additional_headers={"Procore-Company-Id": "123"},
            params={"project_id": 456},
            data={"folder": {"name": "New Folder", "explicit_permissions": False}}
        )

    def test_update(self, folders_instance, mocker):
        """
        Test the `update` method.
        """
        mocker.patch.object(
            folders_instance,
            "patch_request",
            return_value={"id": 1, "name": "Updated Folder"}
        )

        response = folders_instance.update(company_id=123, project_id=456, doc_id=1, folder_name="Updated Folder")

        # Assertions
        assert response["id"] == 1
        assert response["name"] == "Updated Folder"

        folders_instance.patch_request.assert_called_once_with(
            api_url="/rest/v1.0/folders/1",
            additional_headers={"Procore-Company-Id": "123"},
            params={"project_id": 456},
            data={"folder": {"name": "Updated Folder"}}
        )
