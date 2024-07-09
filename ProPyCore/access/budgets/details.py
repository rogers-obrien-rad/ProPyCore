    
from ..base import Base
from ...exceptions import NotFoundItemError

class BudgetDetails(Base):
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = "/rest/v1.0/budget_views"

    def get(self, company_id, project_id, budget_view_id):
        """
        Return a list of all rows from the Budget Detail Report for a Project and Budget View: https://developers.procore.com/reference/rest/v1/budget-details?version=1.0#list-budget-details
        
        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        budget_view_id : int
            unique identifier for the budget view

        Returns
        -------
        """
        params = {
            "project_id": project_id
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        details = self.post_request(
            api_url=f"{self.endpoint}/{budget_view_id}/budget_details",
            additional_headers=headers,
            params=params
        )

        return details