from ..base import Base
from ...exceptions import NotFoundItemError

class Punch(Base):
    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.1"

    def get(self, company_id, project_id, page=1, per_page=100):
        """
        Gets all the available punch items

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        page : int, default 1
            page number
        per_page : int, default 100
            number of punch items to include per page

        Returns
        -------
        punch_items : dict
            available punch data
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }
        n_punch_items = 1
        page = 1
        punch_items = []
        while n_punch_items > 0:
            params = {
                "project_id": project_id,
                "page": page,
                "per_page": per_page
            }

            punch_selection = self.get_request(
                api_url=f"{self.endpoint}/punch_items",
                additional_headers=headers,
                params=params
            )

            n_punch_items = len(punch_selection)
            punch_items += punch_selection
            page += 1 

        return punch_items

    def show(self, company_id, project_id, punch_id):
        """
        Shows the punch item info

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        punch_id : int
            unique identifier for the punch item

        Returns
        -------
        punch_info : dict
            specific punch item information
        """

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        params = {
            "project_id": project_id
        }

        punch_info = self.get_request(
            api_url=f"{self.endpoint}/punch_items/{punch_id}",
            additional_headers=headers,
            params=params
        )

        return punch_info