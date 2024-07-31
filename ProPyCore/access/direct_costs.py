from .base import Base
from ..exceptions import NotFoundItemError

class DirectCosts(Base):
    """
    Access and working with Direct Costs with App access
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/projects"

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
        for direct_cost in self.get(company_id=company_id, project_id=project_id):
            if direct_cost["id"] == identifier:
                direct_cost_info = self.show(
                    company_id=company_id,
                    project_id=project_id,
                    direct_cost_id=direct_cost["id"]
                )
                return direct_cost_info

        raise NotFoundItemError(f"Could not find Direct Cost {identifier}")
    
    def create(self, company_id, project_id, direct_cost_data, attachments=[]):
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
        attachments : list, default []
            list of attachment file paths

        Returns
        -------
        response : dict
            response from the API containing the created Direct Cost item
        """
        headers = {
            "Procore-Company-Id": f"{company_id}",
            "Content-Type": "application/json"
        }

        direct_cost_payload = {
            "attachments": attachments,
            "item": direct_cost_data
        }

        # Log the request details
        print("URL:", f"{self.endpoint}/{project_id}/direct_costs")
        print("Headers:", headers)
        print("Payload:", direct_cost_payload)

        response = self.post_request(
            api_url=f"{self.endpoint}/{project_id}/direct_costs",
            additional_headers=headers,
            data=direct_cost_payload
        )

        return response