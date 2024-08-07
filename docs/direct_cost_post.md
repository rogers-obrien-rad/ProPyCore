# Procore Direct Cost Example POST/PATCH Request
[Procore Documentation](https://developers.procore.com/reference/rest/v1/direct-costs?version=1.1)

### Example URL

https://app.procore.com/rest/v1.1/projects/2783683/direct_costs

### Headers:

```json
{
    "Authorization":"Bearer <token>",
    "Procore-Company-Id":"8089",
    "Accept":"application/json"
}
```
### Data

```json
{
    "direct_cost[description]":"Invoice with attachment for April 13, 2024",
    "direct_cost[direct_cost_date]":"2024-04-13",
    "direct_cost[employee_id]":"8780450",
    "direct_cost[invoice_number]":"Attachment 2024-04-13",
    "direct_cost[origin_data]":"OD-4385814523",
    "direct_cost[origin_id]":"px-1141",
    "direct_cost[payment_date]":"2024-01-11",
    "direct_cost[received_date]":"2024-01-11",
    "direct_cost[status]":"approved",
    "direct_cost[terms]":"Net 50",
    "direct_cost[vendor_id]":"5181441",
    "direct_cost[direct_cost_type]":"invoice",
}
```

### Files

```json
[
    (
    'attachments[]',
        (
            'C:\\Users\\hfritz\\OneDrive - RO\\Documents\\packages\\ProPyCore\\snippets\\dummy\\direct_costs_module.pdf',
            <_io.BufferedReader name='C:\\Users\\hfritz\\OneDrive - RO\\Documents\\packages\\ProPyCore\\snippets\\dummy\\direct_costs_module.pdf'>,
            'application/pdf'
        )
    )
]
```

## Code Snippets

### POST: `create()`

```python
def create(self, company_id, project_id, direct_cost_data, line_items, attachments=[]):
    """
    Creates a new Direct Cost item in the specified Project.

    Parameters
    ----------
    company_id : int
        unique identifier for the company
    project_id : int
        unique identifier for the project
    direct_cost_data : dict
        the data for the new Direct Cost item
    line_items : list
        the list of line items associated with the direct cost
    attachments : list, default []
        list of attachment file paths

    Returns
    -------
    response : dict
        response from the API containing the created Direct Cost item
    """
    headers = {
        "Procore-Company-Id": f"{company_id}",
        "Accept": "application/json",
    }

    # Prepare payload
    payload = {
        f'direct_cost[{key}]': str(value)
        for key, value in direct_cost_data.items()
    }

    # Add line items to the payload
    line_item_payload = []
    for line_item in line_items:
        line_item_dict = {}
        for key, value in line_item.items():
            line_item_dict[key] = value
            
        line_item_payload.append(line_item_dict)

    payload['direct_cost[line_items]'] = line_item_payload

    # Prepare attachments
    files = []
    for attachment in attachments:
        mime_type, _ = mimetypes.guess_type(attachment)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        files.append(('attachments[]', (attachment, open(attachment, 'rb'), mime_type)))

    # Make the request
    response = self.post_request(
        api_url=f"{self.endpoint}/{project_id}/direct_costs",
        additional_headers=headers,
        data=payload,
        files=files
    )
```

### PATCH: `update()`

```python
def update(self, company_id, project_id, direct_cost_id, direct_cost_data={}, line_items=[], attachments=[]):
"""
Creates a new Direct Cost item in the specified Project.

Parameters
----------
company_id : int
    unique identifier for the company
project_id : int
    unique identifier for the project
direct_cost_id : int
    unique identifier for the direct cost
direct_cost_data : dict, default {}
    the data for the new Direct Cost item
line_items : list, default []
    the list of line items associated with the direct cost
attachments : list, default []
    list of attachment file paths

Returns
-------
response : dict
    response from the API containing the created Direct Cost item
"""
headers = {
    "Procore-Company-Id": f"{company_id}",
    "Accept": "application/json",
}

# Prepare payload
if direct_cost_data:
    payload = {
        f'direct_cost[{key}]': str(value)
        for key, value in direct_cost_data.items()
    }
else:
    payload = {}

# Add line items to the payload
line_item_payload = []
for line_item in line_items:
    line_item_dict = {}
    for key, value in line_item.items():
        line_item_dict[key] = value
        
    line_item_payload.append(line_item_dict)

payload['direct_cost[line_items]'] = line_item_payload

# Prepare attachments
files = []
for attachment in attachments:
    mime_type, _ = mimetypes.guess_type(attachment)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    files.append(('attachments[]', (attachment, open(attachment, 'rb'), mime_type)))

# Make the request
response = self.patch_request(
    api_url=f"{self.endpoint}/{project_id}/direct_costs/{direct_cost_id}",
    additional_headers=headers,
    data=payload,
    files=files
)

# Close the file objects
for file_tuple in files:
    file_tuple[1][1].close()

return response
```