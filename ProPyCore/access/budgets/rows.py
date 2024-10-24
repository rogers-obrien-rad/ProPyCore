from ..base import Base
from ...exceptions import NotFoundItemError

class BudgetRows(Base):
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = "/rest/v1.0/budget_views"

    def get(self, company_id, project_id, budget_view_id):
        """
        Lists the rows in a budget view: https://developers.procore.com/reference/rest/v1/budget-view-detail-rows?version=1.0#list-budget-view-detail-rows

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
        rows : list of dict
            rows in a budget view
        """
        params = {
            "project_id": project_id,
            "budget_row_type": "all"
        }
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }
        rows = self.get_request(
            api_url=f"{self.endpoint}/{budget_view_id}/detail_rows",
            additional_headers=headers,
            params=params
        )
        return rows

    def find(self, company_id, project_id, budget_view_id, identifier):
        """
        Finds specified budget view column by looping through the results from get_budget_columns()

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        budget_view_id : int
            unique identifier for the budget view
        identifier : int or str
            identifier for view which can be an id (int) or name (str)

        Returns
        -------
        column : dict
            column data

        Raises
        ------
        NotFoundItemError
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "cost_code"
        for row in self.get(company_id=company_id, project_id=project_id, budget_view_id=budget_view_id):
            if row[key] == identifier:
                return row
        raise NotFoundItemError(f"Could not find row {identifier}")
