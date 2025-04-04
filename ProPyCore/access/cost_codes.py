from turtle import position
from .base import Base
from ..exceptions import NotFoundItemError

class CostCodes(Base):
    """
    Access and working with cost codes from
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/cost_codes"

    def get(self, company_id, project_id, per_page=100):
        """
        Gets a list of all the cost codes from a certain project

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        per_page : int, default 100
            number of companies to include

        Returns
        -------
        codes : list of dict
            list where each value is a dict with the codes's id and data
        """
        additional_headers = {
            "company_id": f"{company_id}"
        }

        codes = []
        n_codes = 1
        page = 1
        while n_codes > 0:
            params = {
                "project_id": project_id,
                "page": page,
                "per_page": per_page
            }
            
            codes_per_page = self.get_request(
                additional_headers=additional_headers,
                api_url=self.endpoint,
                params=params
            )
            n_codes = len(codes_per_page)

            codes += codes_per_page

            page += 1

        return codes

    def show(self, company_id, project_id, cost_code_id):
        """
        Shows the cost code info

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        cost_code_id : int
            unique identifier for the cost code

        Returns
        -------
        cost_code_info : dict
            specific cost code information
        """

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        params = {
            "project_id": project_id
        }

        try:
            cost_code_info = self.get_request(
                api_url=f"{self.endpoint}/{cost_code_id}",
                additional_headers=headers,
                params=params
            )
        except Exception as e:
            raise NotFoundItemError(f"Could not find Cost Code {cost_code_id}")

        return cost_code_info

    def find(self, company_id, project_id, identifier):
        """
        Finds specified cost code and returns data

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        identifier : int or str
            identifier for cost code - id (int) or name (str)

        Returns
        -------
        cost_code_info : dict
            cost code data
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "name"

        for cost_code in self.get(company_id=company_id, project_id=project_id):
            if cost_code[key] == identifier:
                cost_code_info = self.show(
                    company_id=company_id,
                    project_id=project_id,
                    cost_code_id=cost_code["id"]
                )
                return cost_code_info

        raise NotFoundItemError(f"Could not find Cost Code {identifier}")

    def create(self, company_id, project_id, name, code, position=1):
        """
        Creates a new cost code

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int
            unique identifier for the project
        name : str
            name of the cost code

        Returns
        -------
        cost_code_info : dict
            cost code data
        """

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        data = {
            "project_id": project_id,
            "cost_code": {
                "position": position,
                "code": code,
                "name": name
            }
        }

        cost_code_info = self.post_request(
            api_url=self.endpoint,
            additional_headers=headers,
            data=data
        )

        return cost_code_info