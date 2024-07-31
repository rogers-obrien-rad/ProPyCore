## DirectCosts Module

This module provides access and functionalities for working with Direct Costs using the Procore API.

### Class: `DirectCosts`

#### Description

The `DirectCosts` class allows interaction with Direct Costs in a specified project within Procore.

#### Initialization

```python
DirectCosts(access_token, server_url)
```

**Parameters:**
- `access_token` (str): Access token for Procore API.
- `server_url` (str): Base URL for the Procore API.

#### Methods

##### `get`

Retrieves all available Direct Costs for a specified project.

```python
def get(self, company_id, project_id, page=1, per_page=100)
```

**Parameters:**
- `company_id` (int): Unique identifier for the company.
- `project_id` (int): Unique identifier for the project.
- `page` (int, default 1): Page number.
- `per_page` (int, default 100): Number of direct costs to include per page.

**Returns:**
- `direct_costs` (dict): Dictionary containing available direct cost data.

##### `show`

Retrieves specific Direct Cost information.

```python
def show(self, company_id, project_id, direct_cost_id)
```

**Parameters:**
- `company_id` (int): Unique identifier for the company.
- `project_id` (int): Unique identifier for the project.
- `direct_cost_id` (int): Unique identifier for the direct cost.

**Returns:**
- `direct_cost_item` (dict): Dictionary containing specific direct cost information.

##### `find`

Finds specified Direct Cost and returns its data using the `show` method.

```python
def find(self, company_id, project_id, identifier)
```

**Parameters:**
- `company_id` (int): Unique identifier for the company.
- `project_id` (int): Unique identifier for the project.
- `identifier` (int or str): Identifier for Direct Cost which can be ID (int).

**Returns:**
- `direct_cost_info` (dict): Dictionary containing Direct Cost data.

**Raises:**
- `NotFoundItemError`: If the specified Direct Cost is not found.

##### `create`

Creates a new Direct Cost item in the specified project.

```python
def create(self, company_id, project_id, direct_cost_data, line_items, attachments=[])
```

**Parameters:**
- `company_id` (int): Unique identifier for the company.
- `project_id` (int): Unique identifier for the project.
- `direct_cost_data` (dict): Data for the new Direct Cost item.
- `line_items` (list): List of line items associated with the direct cost.
- `attachments` (list, default []): List of attachment file paths.

**Returns:**
- `response` (dict): Response from the API containing the created Direct Cost item.

### Example Usage

```python
from direct_costs import DirectCosts

# Initialize DirectCosts instance
direct_costs = DirectCosts(access_token="your_access_token", server_url="https://api.procore.com")

# Get all Direct Costs
direct_costs_data = direct_costs.get(company_id=123, project_id=456)

# Show specific Direct Cost
specific_direct_cost = direct_costs.show(company_id=123, project_id=456, direct_cost_id=789)

# Find a Direct Cost by ID
found_direct_cost = direct_costs.find(company_id=123, project_id=456, identifier=789)

# Create a new Direct Cost item
direct_cost_data = {
    "description": "Invoice for April",
    "direct_cost_date": "2024-12-14",
    "employee_id": 8780450,
    "invoice_number": "Invoice v1.1",
    "origin_data": "OD-2398273424",
    "origin_id": "px-1990",
    "payment_date": "2025-01-10",
    "received_date": "2025-01-08",
    "status": "approved",
    "terms": "Net 50",
    "vendor_id": 5181441,
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

attachments = ["path/to/attachment1.pdf", "path/to/attachment2.pdf"]

created_direct_cost = direct_costs.create(
    company_id=123,
    project_id=456,
    direct_cost_data=direct_cost_data,
    line_items=line_items,
    attachments=attachments
)
```

### Exception Handling

The following exceptions are used within this module:

- `NotFoundItemError`: Raised when a specified Direct Cost is not found.

### Notes

- Ensure the file paths provided in the `attachments` list are correct and accessible.
- This setup will correctly include the files in the `multipart/form-data` request and handle the JSON data as specified.