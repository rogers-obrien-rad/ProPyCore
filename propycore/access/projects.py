from .base import Base
from ..exceptions import NotFoundItemError

class Projects(Base):
    """
    Access and working with projects from a given company
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.1/projects"

    def get(self, company_id, per_page=100):
        """
        Gets a list of all the projects from a certain company

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        per_page : int, default 100
            number of companies to include

        Returns
        -------
        projects : list of dict
            list where each value is a dict with the project's id, active status (is_active), and name
        """
        projects = []
        n_projects = 1
        page = 1
        while n_projects > 0:
            params = {
                "company_id": company_id,
                "page": page,
                "per_page": per_page
            }
            
            projects_per_page = self.get_request(
                api_url=self.endpoint,
                params=params
            )
            n_projects = len(projects_per_page)

            projects += projects_per_page

            page += 1

        return projects

    def find(self, company_id, identifier):
        """
        Finds a project based on the identifier

        Parameters
        ----------
        company_id : int
            company id that the project is under
        identifier : int or str
            project id number or company name
        
        Returns
        -------
        project : dict
            project-specific dictionary
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "name"

        for project in self.get(company_id=company_id):
            if project[key] == identifier:
                return project

        raise NotFoundItemError(f"Could not find project {identifier}")
