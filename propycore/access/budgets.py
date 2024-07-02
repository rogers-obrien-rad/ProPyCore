from .base import Base
from ..exceptions import NotFoundItemError

class Budgets(Base):
    """
    Access and working with RFIs in a given project
    """
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)
        
        self.endpoint = "/rest/v1.0/budget_views"

    def get_views(self, company_id, project_id, page=1, per_page=100):
        """
        Lists the budget views

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
        views : list of dict
            views and their corresponding meta data
        """
        params = {
            "project_id": project_id,
            "page": page,
            "per_page": per_page
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        views = self.get_request(
            api_url=f"{self.endpoint}",
            additional_headers=headers,
            params=params
        )

        return views
    
    def find_view(self, company_id, project_id, identifier):
        """
        Finds specified budget view

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        identifier : int or str
            identifier for view which can be an id (int) or name (str)

        Returns
        -------
        view : dict
            budget view data
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "name"

        for view in self.get_views(company_id=company_id, project_id=project_id):
            if view[key] == identifier:
                return view

        raise NotFoundItemError(f"Could not find view {identifier}")
    
    def get_budget_columns(self, company_id, project_id, budget_view_id):
        """
        Lists the columns in a budget view

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
    
    def find_budget_column(self, company_id, project_id, budget_view_id, identifier):
        """
        Finds specified budget view column

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
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "name"

        for column in self.get_budget_columns(company_id=company_id, project_id=project_id, budget_view_id=budget_view_id):
            if column[key] == identifier:
                return column

        raise NotFoundItemError(f"Could not find column {identifier}")
    
    def get_budget_rows(self, company_id, project_id, budget_view_id):
        """
        Lists the rows in a budget view

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

        columns = self.get_request(
            api_url=f"{self.endpoint}/{budget_view_id}/detail_rows",
            additional_headers=headers,
            params=params
        )

        return columns
    
    def find_budget_row(self, company_id, project_id, budget_view_id, identifier):
        """
        Finds specified budget view row

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        budget_view_id : int
            unique identifier for the budget view
        identifier : int or str
            identifier for view which can be an id (int) or cost_code (str)

        Returns
        -------
        column : dict
            column data
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "cost_code"

        for column in self.get_budget_rows(company_id=company_id, project_id=project_id, budget_view_id=budget_view_id):
            if column[key] == identifier:
                return column

        raise NotFoundItemError(f"Could not find row {identifier}")
    
    def get_budget_details(self, company_id, project_id, budget_view_id):
        """
        Return a list of all rows from the Budget Detail Report for a Project and Budget View.
        
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

        details = self.get_request(
            api_url=f"{self.endpoint}/{budget_view_id}/budget_details",
            additional_headers=headers,
            params=params
        )

        return details