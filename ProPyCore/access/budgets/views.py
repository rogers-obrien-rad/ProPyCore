from ..base import Base
from ...exceptions import NotFoundItemError

class BudgetViews(Base):
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = "/rest/v1.0/budget_views"

    def get(self, company_id, project_id, page=1, per_page=100):
        """
        Lists the budget views: https://developers.procore.com/reference/rest/v1/budget-views?version=1.0#list-budget-views

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

    def find(self, company_id, project_id, identifier):
        """
        Finds specified budget view by looping through the results from get_views()

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

        Raises
        ------
        NotFoundItemError
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "name"
        for view in self.get(company_id=company_id, project_id=project_id):
            if view[key] == identifier:
                return view
        raise NotFoundItemError(f"Could not find view {identifier}")
