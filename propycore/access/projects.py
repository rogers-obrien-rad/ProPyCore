from .base import Base

class Projects(Base):
    """
    Access and working with projects from a given company
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.1/projects"

    def get(self, company_id, page=1, per_page=100):
        """
        Gets a list of all the projects from a certain company

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        page : int, default 1
            page number
        per_page : int, default 100
            number of companies to include

        Returns
        -------
        projects : list of dict
            list where each value is a dict with the project's id, active status (is_active), and name
        """
        params = {
            "company_id": company_id,
            "page": page,
            "per_page": per_page
        }
        
        projects = self.get_request(
            api_url=self.endpoint,
            params=params
        )

        return projects