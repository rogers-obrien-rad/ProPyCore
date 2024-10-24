import pytest
from ProPyCore.access.direct_costs import DirectCosts
from ProPyCore.exceptions import NotFoundItemError

## Fixture for DirectCosts instance
@pytest.fixture
def direct_costs_instance(mocker):
    # Allow Base class to initialize normally to set attributes like server_url
    mocker.patch.object(DirectCosts, 'get_request')
    mocker.patch.object(DirectCosts, 'post_request')
    mocker.patch.object(DirectCosts, 'patch_request')
    return DirectCosts('mock_access_token', 'mock_server_url')

def test_get_direct_costs(direct_costs_instance, mocker):
    # Mock the get_request method to return sample Direct Costs with pagination
    mock_response_page_1 = [{'id': 1, 'cost_code': 'DC-1'}, {'id': 2, 'cost_code': 'DC-2'}]
    mock_response_page_2 = []

    mocker.patch.object(direct_costs_instance, 'get_request', side_effect=[mock_response_page_1, mock_response_page_2])

    response = direct_costs_instance.get(company_id=123, project_id=456)

    assert isinstance(response, list)
    assert response == mock_response_page_1

def test_show_direct_cost(direct_costs_instance, mocker):
    # Mock the get_request method to return a specific Direct Cost
    mock_response = {'id': 1, 'cost_code': 'DC-1'}
    mocker.patch.object(direct_costs_instance, 'get_request', return_value=mock_response)

    response = direct_costs_instance.show(company_id=123, project_id=456, direct_cost_id=1)

    assert isinstance(response, dict)
    assert response == mock_response

def test_find_direct_cost_by_id(direct_costs_instance, mocker):
    # Mock the get and show methods
    mock_get_response_page_1 = [{'id': 1, 'cost_code': 'DC-1'}, {'id': 2, 'cost_code': 'DC-2'}]
    mock_get_response_page_2 = []
    mock_show_response = {'id': 1, 'cost_code': 'DC-1'}

    mocker.patch.object(direct_costs_instance, 'get_request', side_effect=[mock_get_response_page_1, mock_get_response_page_2])
    mocker.patch.object(direct_costs_instance, 'show', return_value=mock_show_response)

    direct_cost_info = direct_costs_instance.find(company_id=123, project_id=456, identifier=1)

    assert isinstance(direct_cost_info, dict)
    assert direct_cost_info == mock_show_response


def test_create_direct_cost(direct_costs_instance, mocker):
    # Mock the post_request method to return a created Direct Cost item
    mock_response = {
        'id': 1,
        'description': 'Invoice for April',
        'direct_cost_date': '2024-12-14',
        'employee_id': 43223,
        'invoice_number': 'Invoice # abc123',
        'origin_data': 'OD-2398273424',
        'origin_id': 'px-1990',
        'payment_date': '2025-01-10',
        'received_date': '2025-01-08',
        'status': 'approved',
        'terms': 'Net 50',
        'vendor_id': 23423,
        'direct_cost_type': 'invoice',
        'line_items': [
            {
                'manual_amount': 1000,
                'wbs_code_id': 1989,
                'description': "100' of Copper Piping",
                'direct_cost_id': 81753,
                'origin_data': 'OD-2398273424',
                'origin_id': 'px-1990',
                'quantity': 82.0201,
                'ref': 'PQRS5678',
                'unit_cost': 12.03,
                'uom': 'cubic feet'
            }
        ],
        'attachments': []
    }

    mocker.patch.object(direct_costs_instance, 'post_request', return_value=mock_response)

    direct_cost_data = {
        "description": "Invoice for April",
        "direct_cost_date": "2024-12-14",
        "employee_id": 43223,
        "invoice_number": "Invoice # abc123",
        "origin_data": "OD-2398273424",
        "origin_id": "px-1990",
        "payment_date": "2025-01-10",
        "received_date": "2025-01-08",
        "status": "approved",
        "terms": "Net 50",
        "vendor_id": 23423,
        "direct_cost_type": "invoice"
    }

    line_items = [
        {
            "manual_amount": 1000,
            "wbs_code_id": 1989,
            "description": "100' of Copper Piping",
            "direct_cost_id": 81753,
            "origin_data": "OD-2398273424",
            "origin_id": "px-1990",
            "quantity": 82.0201,
            "ref": "PQRS5678",
            "unit_cost": 12.03,
            "uom": "cubic feet"
        }
    ]

    attachments = []

    response = direct_costs_instance.create(
        company_id=123,
        project_id=456,
        direct_cost_data=direct_cost_data,
        line_items=line_items,
        attachments=attachments
    )

    assert isinstance(response, dict)
    assert response == mock_response