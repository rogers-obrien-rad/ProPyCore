from ..base import Base
from ...exceptions import NotFoundItemError

class Roles(Base):
    """Access role information on a Company and Project Level"""

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0"

    def list_all(self, company_id):
        """
        Returns a list of all the roles from the company level

        Parameters
        ----------
        company_id : int
            unique identifier for the company

        Returns
        -------
        roles : list of dict
            list where each value is a dict with a role's information
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        roles = self.get_request(
            api_url=f"{self.endpoint}/companies/{company_id}/roles",
            additional_headers=headers,
            params={}
        )

        return roles
    
    def get(self, company_id, project_id, page=1, per_page=100):
        """
        Gets all the available roles on a project

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
        roles : dict
            available roles data
        """
        roles = []
        n_roles = 1
        page = 1
        while n_roles > 0:
            params = {
                "page": page,
                "per_page": per_page,
                "project_id": project_id
            }

            headers = {
                "Procore-Company-Id": f"{company_id}"
            }

            roles_per_page = self.get_request(
                api_url=f"{self.endpoint}/project_roles",
                additional_headers=headers,
                params=params
            )
            n_roles = len(roles_per_page)

            roles += roles_per_page
            page += 1

        return roles
    
    def find(self, company_id, project_id, user_id):
        """
        Finds a person's role based on their identifier

        Parameters
        ----------
        company_id : int
            company id number
        project_id : int
            project id number
        user_id : int or str
            project id number or company name
        
        Returns
        -------
        person : dict
            role-specific dictionary
        """
        if isinstance(user_id, int):
            key = "id"
        else:
            key = "name"

        for person in self.get(company_id=company_id, project_id=project_id):
            if person[key] == user_id:
                return person

        raise NotFoundItemError(f"Could not find {user_id}")