from ..base import Base
from ...exceptions import NotFoundItemError

class BudgetColumns(Base):
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = "/rest/v1.0/budget_views"

    def get(self, company_id, project_id, budget_view_id):
        """
        Lists the columns in a budget view: https://developers.procore.com/reference/rest/v1/budget-detail-columns?version=1.0
        This endpoint only returns the standard/source column meta data. It does not return any calculated columns.

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
        columns : list of dict
            columns in a budget view
        """
        params = {
            "project_id": project_id
        }
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }
        columns = self.get_request(
            api_url=f"{self.endpoint}/{budget_view_id}/budget_detail_columns",
            additional_headers=headers,
            params=params
        )
        return columns

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
            key = "name"

        for column in self.get(company_id=company_id, project_id=project_id, budget_view_id=budget_view_id):
            if column[key] == identifier:
                return column

        raise NotFoundItemError(f"Could not find column {identifier}")

