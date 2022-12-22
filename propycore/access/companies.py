from .base import Base

import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).resolve().parent.parent}")

from propycore.exceptions import NotFoundItemError

class Companies(Base):
    """
    Access and working with Companies with App access
    """

    def __init__(self, access_token, server_url) -> None:
        super().__init__(access_token, server_url)

        self.endpoint = "/rest/v1.0/companies"

    def get(self, page=1, per_page=100):
        """
        Gets all companies with the app installed

        Parameters
        ----------
        per_page : int, default 100
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