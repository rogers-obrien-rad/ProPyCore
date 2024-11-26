from .base import Base
from ..exceptions import NotFoundItemError

class Projects(Base):
    """
    Access and working with projects from a given company
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.1/projects"

    def get(self, company_id, per_page=10000):
        """
        Gets a list of all the projects from a certain company

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        per_page : int, default 10000
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
    
    def get_type(self, company_id, project_id):
        """
        Gets the type for the given project

        Parameters
        ----------
        company_id : int
            The identifier for the company
        project_id : int
            The identifier for the project

        Returns
        -------
        <type_name> : str
            Project type name
        """
        headers = {
            "Procore-Company-Id": f"{company_id}"
        }
        # Get the projects from the company endpoint which has the type_name field
        company_projects = self.get_request(
            api_url=f"/rest/v1.0/companies/{company_id}/projects",
            additional_headers=headers,
            params={}
        )

        # Search for the project with the matching project_id and return the type_name
        for project in company_projects:
            if project.get("id") == project_id:
                return project.get("type_name")

        raise NotFoundItemError(f"Could not find project {project_id}")