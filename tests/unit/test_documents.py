import pytest
from ProPyCore.access.documents import Folders, Files
from ProPyCore.exceptions import NotFoundItemError

class TestFolders:
    @pytest.fixture
    def folders(self, mocker):
        mocker.patch('ProPyCore.access.documents.Base.__init__', return_value=None)  # Mock the base class initializer
        return Folders('access_token', 'server_url')

    def test_root(self, folders, mocker):
        mocker.patch.object(folders, 'get_request', return_value={'some': 'data'})
        result = folders.root(123, 456)
        assert result == {'some': 'data'}
        folders.get_request.assert_called_once_with(api_url=folders.endpoint, additional_headers={'Procore-Company-Id': '123'}, params={'project_id': 456})

    def test_find_folder_success(self, folders, mocker):
        # Mock the 'get' and 'show' methods
        mocker.patch.object(folders, 'get', return_value=[{'name': 'TestFolder', 'id': 1}])
        mocker.patch.object(folders, 'show', return_value={'id': 1, 'name': 'TestFolder'})

        result = folders.find(123, 456, 'TestFolder')
        assert result == {'id': 1, 'name': 'TestFolder'}
        folders.show.assert_called_once_with(company_id=123, project_id=456, doc_id=1)

    def test_find_folder_failure(self, folders, mocker):
        # Mock the 'get' method to return an empty list
        mocker.patch.object(folders, 'get', return_value=[])

        with pytest.raises(NotFoundItemError):
            folders.find(123, 456, 'NonExistentFolder')

class TestFiles:
    @pytest.fixture
    def files(self, mocker):
        mocker.patch('ProPyCore.access.documents.Base.__init__', return_value=None)  # Mock the base class initializer
        return Files('access_token', 'server_url')
    
    def test_find_file_success(self, files, mocker):
        # Mock the 'get' and 'show' methods
        mocker.patch.object(files, 'get', return_value=[{'name': 'TestFile', 'id': 1}])
        mocker.patch.object(files, 'show', return_value={'id': 1, 'name': 'TestFile'})

        result = files.find(123, 456, 'TestFile')
        assert result == {'id': 1, 'name': 'TestFile'}
        files.show.assert_called_once_with(company_id=123, project_id=456, doc_id=1)

    def test_find_file_failure(self, files, mocker):
        # Mock the 'get' method to return an empty list
        mocker.patch.object(files, 'get', return_value=[])

        with pytest.raises(NotFoundItemError):
            files.find(123, 456, 'NonExistentFile')
