from ..base import Base
from ...exceptions import NotFoundItemError

class Vendors(Base):
    """Access vendor information on a Company and Project Level"""

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

    def get_url(self, project_id=None):
        """
        Returns the url specific to Vendors at company or project level

        Parameters
        ----------
        project_id : int, default None
            unique identifier for the project
            None specifies company-level

        Returns
        -------
        <url> : str
            url for Vendors request
        """
        if project_id is None:
            return f"/rest/v1.0/vendors"
        else:
            return f"/rest/v1.1/projects/{project_id}/vendors"

    def get(self, company_id, project_id=None, per_page=10000):
        """
        Gets a list of all vendors from a certain company

        Parameters
        ----------
        company_id : int
            unique identifier for the company
        project_id : int, default None
            unique identifier for the project
            None specifies company-level
        per_page : int, default 100
            number of companies to include

        Returns
        -------
        vendors : list of dict
            list where each value is a dict with a vendors's information
        """
        vendors = []
        n_vendors = 1
        page = 1
        while n_vendors > 0:
            params = {
                "page": page,
                "per_page": per_page,
                "company_id": company_id # this parameter is only used in Company Vendors, but including it for other requests does not seem to create any issues
            }

            headers = {
                "Procore-Company-Id": f"{company_id}"
            }

            url = self.get_url(
                project_id=project_id
            )

            vendors_per_page = self.get_request(
                api_url=url,
                additional_headers=headers,
                params=params
            )
            n_vendors = len(vendors_per_page)

            vendors += vendors_per_page
            page += 1

        return vendors

    def find(self, company_id, user_id, project_id=None,):
        """
        Finds a Vendor based on the identifier

        Parameters
        ----------
        company_id : int
            company id that the project is under
        user_id : int or str
            project id number or company name
        project_id : int, default None
            unique identifier for the project
            None specifies company-level
        
        Returns
        -------
        vendor : dict
            project-specific dictionary
        """
        if isinstance(user_id, int):
            key = "id"
        else:
            key = "name"

        for vendor in self.get(company_id=company_id, project_id=project_id):
            if vendor[key] == user_id:
                return vendor

        raise NotFoundItemError(f"Could not find Vendor {user_id}")

    