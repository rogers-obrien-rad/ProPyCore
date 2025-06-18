from .base import Base
from ..exceptions import *

class Submittal(Base):
    """
    Access and working with submittals in a given project
    """
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)
        self.endpoint = "/rest" # Different version numbers for different endpoints so limited to this

    def get_statuses(self, company_id, project_id):
        """
        Gets all the available submittal statuses

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project

        Returns
        -------
        submittal_statuses : dict
            available submittal statuses
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }
        return self.get_request(
            api_url=f"{self.endpoint}/v1.0/projects/{project_id}/submittals/filter_options/status_id",
            additional_headers=headers
        )

    def get(self, company_id, project_id, page=1, per_page=100, status_ids=None):
        """
        Gets all the available submittals

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
        status_ids : list of int or str, default None
            filter by status ID

        Returns
        -------
        submittals : dict
            available rfi data
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }
        n_submittals = 1
        page = 1
        submittals = []
        while n_submittals > 0:
            params = {
                "page": page,
                "per_page": per_page
            }

            if status_ids is not None:
                if isinstance(status_ids, list):
                    params["filters[status_id]"] = [str(status_id) for status_id in status_ids]
                else:
                    params["filters[status_id]"] = [str(status_ids)]

            headers = {
                "Procore-Company-Id": f"{company_id}"
            }

            submittal_selection = self.get_request(
                api_url=f"{self.endpoint}/v1.1/projects/{project_id}/submittals",
                additional_headers=headers,
                params=params
            )

            n_submittals = len(submittal_selection)
            submittals += submittal_selection
            page += 1 

        return submittals

    def show(self, company_id, project_id, submittal_id):
        """
        Shows the Submittal info.

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        submittal_id : int
            unique identifier for the submittal

        Returns
        -------
        submittal_info : dict
            specific submittal information
        """
        headers = {"Procore-Company-Id": f"{company_id}"}
        submittal_info = self.get_request(
            api_url=f"{self.endpoint}/v1.1/projects/{project_id}/submittals/{submittal_id}",
            additional_headers=headers,
        )
        return submittal_info

    def find(self, company_id, project_id, identifier):
        """
        Finds specified submittal.

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        identifier : int or str
            identifier for Submittal

        Returns
        -------
        submittal_info : dict
            submittal data
        """
        submittals = self.get(company_id=company_id, project_id=project_id)
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "title"

        for submittal in submittals:
            if submittal[key] == identifier:
                return self.show(
                    company_id=company_id,
                    project_id=project_id,
                    submittal_id=submittal["id"]
                )

        raise NotFoundItemError(f"Could not find Submittal {identifier}")