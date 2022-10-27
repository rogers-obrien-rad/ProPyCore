from .base import Base

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
        page : int, default 1
            page number
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

    def find(self, company_list, identifier):
        """
        Finds a company based on the identifier

        Parameters
        ----------
        company_list : list of dict
            companies
        identifier : int or str
            company id number or company name
        
        Returns
        -------
        company : dict
            company-specific dictionary
        """
        if isinstance(identifier, int):
            key = "id"
        else:
            key = "name"

        for company in company_list:
            if company[key] == identifier:
                return company

        return {}