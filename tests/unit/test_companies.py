import pytest
from ProPyCore.access.companies import Companies
from ProPyCore.exceptions import NotFoundItemError

class TestCompanies:
    @pytest.fixture
    def companies(self, mocker):
        mocker.patch('ProPyCore.access.companies.Base.__init__', return_value=None)  # Mock the base class initializer
        return Companies('access_token', 'server_url')

    def test_get(self, companies, mocker):
        mocker.patch.object(companies, 'get_request', return_value=[{'id': 1, 'name': 'TestCompany'}])
        company_list = companies.get()
        assert company_list == [{'id': 1, 'name': 'TestCompany'}]
        companies.get_request.assert_called_once_with(
            api_url=companies.endpoint,
            params={'page': 1, 'per_page': 100, 'include_free_companies': True}
        )

    def test_find_success(self, companies, mocker):
        mocker.patch.object(companies, 'get', return_value=[{'id': 1, 'name': 'TestCompany'}])
        company = companies.find(identifier="TestCompany")
        assert company == {'id': 1, 'name': 'TestCompany'}

    def test_find_failure(self, companies, mocker):
        mocker.patch.object(companies, 'get', return_value=[])
        with pytest.raises(NotFoundItemError):
            companies.find(identifier="NonExistentCompany")
