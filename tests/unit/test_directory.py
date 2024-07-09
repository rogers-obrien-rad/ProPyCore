import pytest
from ProPyCore.access.directory import Users, Vendors, Trades
from ProPyCore.exceptions import NotFoundItemError

# Fixture for Users instance
@pytest.fixture
def users_instance(mocker):
    mocker.patch('ProPyCore.access.directory.Base.__init__', return_value=None)  # Mock the base class initializer
    return Users('mock_access_token', 'mock_server_url')

# Fixture for Vendors instance
@pytest.fixture
def vendors_instance(mocker):
    mocker.patch('ProPyCore.access.directory.Base.__init__', return_value=None)  # Mock the base class initializer
    return Vendors('mock_access_token', 'mock_server_url')

# Fixture for Trades instance
@pytest.fixture
def trades_instance(mocker):
    mocker.patch('ProPyCore.access.directory.Base.__init__', return_value=None)  # Mock the base class initializer
    return Trades('mock_access_token', 'mock_server_url')

def test_get_users(users_instance, mocker):
    # Mock the get_request method to return sample users with pagination
    mock_response_page_1 = [{'id': 1, 'name': 'User-1'}, {'id': 2, 'name': 'User-2'}]
    mock_response_page_2 = []

    mocker.patch.object(users_instance, 'get_request', side_effect=[mock_response_page_1, mock_response_page_2])

    response = users_instance.get(company_id=123)

    assert isinstance(response, list)
    assert response == mock_response_page_1

def test_find_user_by_id(users_instance, mocker):
    # Mock the get method
    mock_get_response_page_1 = [{'id': 1, 'name': 'User-1'}, {'id': 2, 'name': 'User-2'}]
    mock_get_response_page_2 = []

    mocker.patch.object(users_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])

    user_info = users_instance.find(company_id=123, user_id=1)

    assert isinstance(user_info, dict)
    assert user_info == {'id': 1, 'name': 'User-1'}

def test_find_user_by_name(users_instance, mocker):
    # Mock the get method
    mock_get_response_page_1 = [{'id': 1, 'name': 'User-1'}, {'id': 2, 'name': 'User-2'}]
    mock_get_response_page_2 = []

    mocker.patch.object(users_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])

    user_info = users_instance.find(company_id=123, user_id='User-2')

    assert isinstance(user_info, dict)
    assert user_info == {'id': 2, 'name': 'User-2'}

def test_find_user_not_found(users_instance, mocker):
    # Mock the get method to return sample users
    mock_get_response_page_1 = [{'id': 1, 'name': 'User-1'}, {'id': 2, 'name': 'User-2'}]
    mock_get_response_page_2 = []

    mocker.patch.object(users_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])

    with pytest.raises(NotFoundItemError):
        users_instance.find(company_id=123, user_id='Nonexistent User')

def test_add_user_to_project(users_instance, mocker):
    # Mock the post_request method
    mocker.patch.object(users_instance, 'post_request', return_value=None)

    users_instance.add(company_id=123, project_id=456, user_id=789, permission_template_id=101112)

    users_instance.post_request.assert_called_once_with(
        api_url="/rest/v1.0/projects/456/users/789/actions/add",
        additional_headers={"Procore-Company-Id": "123"},
        params={"project_id": 456},
        data={"user": {"permission_template_id": 101112}}
    )

def test_get_vendors(vendors_instance, mocker):
    # Mock the get_request method to return sample vendors with pagination
    mock_response_page_1 = [{'id': 1, 'name': 'Vendor-1'}, {'id': 2, 'name': 'Vendor-2'}]
    mock_response_page_2 = []

    mocker.patch.object(vendors_instance, 'get_request', side_effect=[mock_response_page_1, mock_response_page_2])

    response = vendors_instance.get(company_id=123)

    assert isinstance(response, list)
    assert response == mock_response_page_1

def test_find_vendor_by_id(vendors_instance, mocker):
    # Mock the get method
    mock_get_response_page_1 = [{'id': 1, 'name': 'Vendor-1'}, {'id': 2, 'name': 'Vendor-2'}]
    mock_get_response_page_2 = []

    mocker.patch.object(vendors_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])

    vendor_info = vendors_instance.find(company_id=123, user_id=1)

    assert isinstance(vendor_info, dict)
    assert vendor_info == {'id': 1, 'name': 'Vendor-1'}

def test_find_vendor_by_name(vendors_instance, mocker):
    # Mock the get method
    mock_get_response_page_1 = [{'id': 1, 'name': 'Vendor-1'}, {'id': 2, 'name': 'Vendor-2'}]
    mock_get_response_page_2 = []

    mocker.patch.object(vendors_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])

    vendor_info = vendors_instance.find(company_id=123, user_id='Vendor-2')

    assert isinstance(vendor_info, dict)
    assert vendor_info == {'id': 2, 'name': 'Vendor-2'}

def test_find_vendor_not_found(vendors_instance, mocker):
    # Mock the get method to return sample vendors
    mock_get_response_page_1 = [{'id': 1, 'name': 'Vendor-1'}, {'id': 2, 'name': 'Vendor-2'}]
    mock_get_response_page_2 = []

    mocker.patch.object(vendors_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])

    with pytest.raises(NotFoundItemError):
        vendors_instance.find(company_id=123, user_id='Nonexistent Vendor')

def test_get_trades(trades_instance, mocker):
    # Mock the get_request method to return sample trades with pagination
    mock_response_page_1 = [{'id': 1, 'name': 'Trade-1'}, {'id': 2, 'name': 'Trade-2'}]
    mock_response_page_2 = []

    mocker.patch.object(trades_instance, 'get_request', side_effect=[mock_response_page_1, mock_response_page_2])

    response = trades_instance.get(company_id=123)

    assert isinstance(response, list)
    assert response == mock_response_page_1

def test_find_trade_by_id(trades_instance, mocker):
    # Mock the get method
    mock_get_response_page_1 = [{'id': 1, 'name': 'Trade-1'}, {'id': 2, 'name': 'Trade-2'}]
    mock_get_response_page_2 = []

    mocker.patch.object(trades_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])

    trade_info = trades_instance.find(company_id=123, user_id=1)

    assert isinstance(trade_info, dict)
    assert trade_info == {'id': 1, 'name': 'Trade-1'}

def test_find_trade_by_name(trades_instance, mocker):
    # Mock the get method
    mock_get_response_page_1 = [{'id': 1, 'name': 'Trade-1'}, {'id': 2, 'name': 'Trade-2'}]
    mock_get_response_page_2 = []

    mocker.patch.object(trades_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])

    trade_info = trades_instance.find(company_id=123, user_id='Trade-2')

    assert isinstance(trade_info, dict)
    assert trade_info == {'id': 2, 'name': 'Trade-2'}

def test_find_trade_not_found(trades_instance, mocker):
    # Mock the get method to return sample trades
    mock_get_response_page_1 = [{'id': 1, 'name': 'Trade-1'}, {'id': 2, 'name': 'Trade-2'}]
    mock_get_response_page_2 = []

    mocker.patch.object(trades_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])

    with pytest.raises(NotFoundItemError):
        trades_instance.find(company_id=123, user_id='Nonexistent Trade')
