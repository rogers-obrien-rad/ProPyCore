import json
import mimetypes

from .base import Base
from ..exceptions import NotFoundItemError, raise_exception

class DirectCosts(Base):
    """
    Access and working with Direct Costs with App access
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.1/projects"

    def get(self, company_id, project_id, page=1, per_page=100):
        """
        Gets all the available Direct Costs

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        page : int, default 1
            page number
        per_page : int, default 100
            number of companies to include

        Returns
        -------
        direct_costs : dict
            available rfi data
        """
        params = {
            "page": page,
            "per_page": per_page
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        direct_costs = self.get_request(
            api_url=f"{self.endpoint}/{project_id}/direct_costs",
            additional_headers=headers,
            params=params
        )

        return direct_costs
    
    def show(self, company_id, project_id, direct_cost_id):
        """
        Shows the Direct Cost info

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        direct_cost_id : int
            unique identifier for the direct cost

        Returns
        -------
        direct_cost_item : dict
            specific direct cost information
        """

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        direct_cost_item = self.get_request(
            api_url=f"{self.endpoint}/{project_id}//direct_costs/{direct_cost_id}",
            additional_headers=headers,
        )

        return direct_cost_item
    
    def find(self, company_id, project_id, identifier):
        """
        Finds specified Direct Cost and returns data - wrapper for show method

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        identifier : int or str
            identifier for Direct Cost which can be id (int)

        Returns
        -------
        direct_cost_info : dict
            Direct Cost data
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "invoice_number"

        for direct_cost in self.get(company_id=company_id, project_id=project_id):
            if direct_cost[key] == identifier:
                direct_cost_info = self.show(
                    company_id=company_id,
                    project_id=project_id,
                    direct_cost_id=direct_cost["id"]
                )
                return direct_cost_info

        raise NotFoundItemError(f"Could not find Direct Cost {identifier}")
    
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

        # Close the file objects
        for file_tuple in files:
            file_tuple[1][1].close()

        return response
    
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
