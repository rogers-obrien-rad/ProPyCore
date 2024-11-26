from .base import Base
from ..exceptions import NotFoundItemError

class Companies(Base):
    """
    Access and working with Companies with App access
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/companies"

    def get(self, page=1, per_page=10000):
        """
        Gets all companies where the data connection app is installed

        Parameters
        ----------
        per_page : int, default 10000
            number of companies to include

        Returns
        -------
        companies : list of dict
            list where each value is a dict with the company's id, active status (is_active), and name
        """
        params = {
            "page": page,
            "per_page": per_page,
            "include_free_companies": True
        }

        companies = self.get_request(
            api_url=self.endpoint,
            params=params
        )

        return companies

    def find(self, identifier):
        """
        Finds a company based on the identifier

        Parameters
        ----------
        identifier : int or str
            company id number or name
        
        Returns
        -------
        company : dict
            company-specific dictionary
        """
        # determining which identifier to search for
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "name"

        for company in self.get():
            if company[key] == identifier:
                return company

        raise NotFoundItemError(f"Could not find company {identifier}")
    
    def get_projects(self, company_id):
        """
        Gets all projects from the companies

        Parameters
        ----------
        company_id : int
            The identifier for the company

        Returns
        -------
        projects : list of dict
            list where each value is a project within the company
        """
        endpoint = f"{self.endpoint}/{company_id}/projects"

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        projects = self.get_request(
            api_url=endpoint,
            additional_headers=headers
        )

        return projects
    
    def list_regions(self, company_id, page=1, per_page=100):
        """
        Gets all regions for a specified company

        Parameters
        ----------
        company_id : int
            The identifier for the company
        per_page : int, default 100
            Number of regions to include per page

        Returns
        -------
        regions : list of dict
            List where each value is a dict with the region's details
        """
        endpoint = f"{self.endpoint}/{company_id}/project_regions"

        params = {
            "page": page,
            "per_page": per_page
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        regions = self.get_request(
            api_url=endpoint,
            additional_headers=headers,
            params=params
        )

        return regions

    def list_project_types(self, company_id, page=1, per_page=100):
        """
        Gets all project types for a specified company

        Parameters
        ----------
        company_id : int
            The identifier for the company
        per_page : int, default 100
            Number of project types to include per page

        Returns
        -------
        project_types : list of dict
            List where each value is a dict with the project type's details
        """
        endpoint = f"{self.endpoint}/{company_id}/project_types"

        params = {
            "page": page,
            "per_page": per_page
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        project_types = self.get_request(
            api_url=endpoint,
            additional_headers=headers,
            params=params
        )

        return project_types
    
    def list_project_stages(self, company_id, page=1, per_page=100):
        """
        Gets all project stages for a specified company

        Parameters
        ----------
        company_id : int
            The identifier for the company
        per_page : int, default 100
            Number of project types to include per page

        Returns
        -------
        stages : list of dict
            List where each value is a dict with the project type's details
        """
        endpoint = f"{self.endpoint}/{company_id}/project_stages"

        params = {
            "page": page,
            "per_page": per_page
        }

        headers = {
            "Procore-Company-Id": f"{company_id}"
        }

        stages = self.get_request(
            api_url=endpoint,
            additional_headers=headers,
            params=params
        )

        return stages